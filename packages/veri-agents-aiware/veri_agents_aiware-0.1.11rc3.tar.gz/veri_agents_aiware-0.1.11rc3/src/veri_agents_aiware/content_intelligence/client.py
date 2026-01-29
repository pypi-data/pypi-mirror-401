from __future__ import annotations

import logging
from typing import Any, Iterable, Tuple
from collections.abc import Callable
from datetime import datetime
from aiware.client import AsyncAiware
import async_lru
from functools import partial

import polars as pl
from aiware.client.search_models import (
    SearchRequest,
    SliceSearchResult,
    TdoSliceMetadata,
)

from veri_agents_aiware.aiware_client.async_client import AsyncAgentsAiware
from veri_agents_aiware.content_intelligence.data import (
    new_segments_table,
    create_segment_dict,
    SegmentsTable,
    MentionsTable,
    WatchlistsTable,
    new_mentions_table,
    new_watchlists_table,
    TargetByFolder,
    TargetByIds,
    TargetByOrg,
    TargetByWatchlist,
    TargetByMention,
    TargetSelector,
    coalesce_segments,
    convert_jsondata_to_dict,
)
from veri_agents_aiware.content_intelligence.ops import (
    AbsTime,
    MediaTime,
    FindTranscriptOp,
    FindFaceOp,
    FindLogoOp,
    GetTranscriptsOp,
    GetFacesOp,
    GetLogosOp,
    GetOcrsOp,
)
from veri_agents_aiware.content_intelligence.tdo import MediaTDO

log = logging.getLogger(__name__)

TDO_LIMIT = 2000
WATCHLIST_MENTIONS_LIMIT = 2000

# Elasticsearch special characters that need to be escaped in query_string queries
# See: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html
# See: https://support.veritone.com/s/article/000003997?language=en_US#query-basics-and-syntax
ELASTICSEARCH_SPECIAL_CHARS = r'+-!(){}[]^"~*?:\/'


def _escape_elasticsearch_query(query: str) -> str:
    """Escape special characters for Elasticsearch query_string queries.
    
    Veritone Search API (backed by Elasticsearch) requires escaping special characters
    to ensure they aren't interpreted by the query parser.
    Special characters: + - ! ( ) { } [ ] ^ " ~ * ? : \\ /
    
    Args:
        query: The raw query string to escape.
        
    Returns:
        The escaped query string safe for use in query_string queries.
    """
    result = []
    for char in query:
        if char in ELASTICSEARCH_SPECIAL_CHARS:
            result.append(f"\\{char}")
        else:
            result.append(char)
    return "".join(result)


# ---------------- Helpers ----------------


def _iter_transcript_windows(
    results_obj: SliceSearchResult,
) -> Iterable[Tuple[TdoSliceMetadata, dict[str, Any]]]:
    """
    Yield (recording_metadata, window_dict) for each transcript window across all slice results.

    Args:
        results_obj: SliceSearchResult from transcript search

    Yields:
        Tuples of (TdoSliceMetadata, window_dict)
    """
    for res in results_obj.results or []:
        rec: TdoSliceMetadata | None = res.recording
        if not rec:
            continue
        for hit in res.hits or []:
            t = hit.get("transcript")
            if not t:
                continue
            for win in t.get("transcript") or []:
                yield rec, win


def transcript_windows_to_segments(results_obj: SliceSearchResult) -> SegmentsTable:
    """
    Parses search results into SegmentsTable.
    One Segment per transcript window (context span).

    Args:
        results_obj: SliceSearchResult from transcript search

    Returns:
        SegmentsTable with window-level transcript segments
    """
    rows = []
    for rec, win in _iter_transcript_windows(results_obj):
        tdo_id = str(rec.recordingId or "")
        start = float(win.get("startTime", 0.0))
        end = float(win.get("endTime", 0.0))

        meta = {
            "text": win.get("text"),
            "term_hits": win.get("hits", []),
            "slice": {
                "relativeStartTimeMs": rec.relativeStartTimeMs,
                "relativeStopTimeMs": rec.relativeStopTimeMs,
                "absoluteStartTimeMs": rec.absoluteStartTimeMs,
                "absoluteStopTimeMs": rec.absoluteStopTimeMs,
            },
            "aion": {"transcript": {"hits": win.get("hits", [])}},
        }

        rows.append(
            create_segment_dict(
                tdo_id=tdo_id,
                start_s=start,
                end_s=end,
                signal="transcript",
                channel="audio",
                label=None,
                score=0.0,
                transcript=win.get("text"),
                meta=meta,
            )
        )
    return new_segments_table(rows)


def transcript_tokens_to_segments(results_obj: SliceSearchResult) -> SegmentsTable:
    """
    Parses search results into SegmentsTable.
    One Segment per token-level hit inside each window.

    Args:
        results_obj: SliceSearchResult from transcript search

    Returns:
        SegmentsTable with token-level transcript segments
    """
    rows = []
    for rec, win in _iter_transcript_windows(results_obj):
        tdo_id = str(rec.recordingId or "")
        text = win.get("text")
        for h in win.get("hits") or []:
            start = float(h.get("startTime", 0.0))
            end = float(h.get("endTime", 0.0))

            meta = {
                "text": text,
                "term_hit": h,
                "slice": {
                    "relativeStartTimeMs": rec.relativeStartTimeMs,
                    "relativeStopTimeMs": rec.relativeStopTimeMs,
                    "absoluteStartTimeMs": rec.absoluteStartTimeMs,
                    "absoluteStopTimeMs": rec.absoluteStopTimeMs,
                },
                "aion": {"transcript": {"hit": h}},
            }

            rows.append(
                create_segment_dict(
                    tdo_id=tdo_id,
                    start_s=start,
                    end_s=end,
                    signal="transcript",
                    channel="audio",
                    label=h.get("queryTerm"),
                    score=0.0,
                    transcript=text,
                    meta=meta,
                )
            )
    return new_segments_table(rows)


def face_detections_to_segments(
    results_obj: SliceSearchResult, inject_label: str | None = None
) -> SegmentsTable:
    """
    Convert face recognition results to Segment objects.

    Args:
        results_obj: SliceSearchResult from face recognition search
        inject_label: Optional label to use for all segments instead of entityId

    Returns:
        SegmentsTable with face detection segments
    """
    rows = []
    for res in results_obj.results or []:
        rec = res.recording
        if not rec:
            continue
        tdo_id = str(rec.recordingId or "")
        for hit in res.hits or []:
            series_list = hit.get("face-recognition", {}).get("series", [])
            for series in series_list:
                entity_id = series.get("entityId")
                start = float(series.get("start", 0.0)) / 1000.0
                end = float(series.get("end", 0.0)) / 1000.0
                conf = float(series.get("confidence", 0.0))

                if end > start:  # sanity guard
                    rows.append(
                        create_segment_dict(
                            tdo_id=tdo_id,
                            start_s=start,
                            end_s=end,
                            signal="face",
                            channel="video",
                            label=inject_label or entity_id,
                            score=conf,
                            bbox=series.get("boundingBox"),
                            poly=series.get("boundingPoly"),
                        )
                    )
    return new_segments_table(rows)


def logo_detections_to_segments(results_obj: SliceSearchResult) -> SegmentsTable:
    """
    Convert logo recognition search results to SegmentsTable.
    
    Args:
        results_obj: SliceSearchResult from logo recognition search
        
    Returns:
        SegmentsTable with logo detection segments
    """
    rows = []
    for res in results_obj.results or []:
        rec = res.recording
        if not rec:
            continue
        tdo_id = str(rec.recordingId or "")
        for hit in res.hits or []:
            series_list = hit.get("logo-recognition", {}).get("series", [])
            for series in series_list:
                entity_id = series.get("entityId") or series.get(
                    "found"
                )  # Use 'found' as fallback
                start = float(series.get("start", 0.0)) / 1000.0
                end = float(series.get("end", 0.0)) / 1000.0
                conf = float(series.get("score", 0.0)) or float(
                    series.get("confidence", 0.0)
                )

                if end > start:
                    meta = {
                        "entityId": entity_id,
                        "slice": {
                            "relativeStartTimeMs": getattr(
                                rec, "relativeStartTimeMs", None
                            ),
                            "relativeStopTimeMs": getattr(
                                rec, "relativeStopTimeMs", None
                            ),
                            "absoluteStartTimeMs": getattr(
                                rec, "absoluteStartTimeMs", None
                            ),
                            "absoluteStopTimeMs": getattr(
                                rec, "absoluteStopTimeMs", None
                            ),
                        },
                        "aion": {"logo-recognition": {"series": series}},
                    }

                    rows.append(
                        create_segment_dict(
                            tdo_id=tdo_id,
                            start_s=start,
                            end_s=end,
                            signal="logo",
                            channel="video",
                            label=entity_id,
                            score=conf,
                            bbox=series.get("boundingBox"),
                            poly=series.get("boundingPoly"),
                            meta=meta,
                        )
                    )
    return new_segments_table(rows)


def _clip_by_media_time(segs: SegmentsTable, mt: MediaTime | None) -> SegmentsTable:
    """Clip segments by media time bounds.

    Args:
        segs: SegmentsTable with segments to clip
        mt: MediaTime with from_s and to_s bounds

    Returns:
        Clipped SegmentsTable
    """
    if not mt or (mt.from_s is None and mt.to_s is None):
        return segs
    if segs.is_empty():
        return segs

    f = float(mt.from_s) if mt.from_s is not None else float("-inf")
    t = float(mt.to_s) if mt.to_s is not None else float("inf")

    # Filter for overlapping segments and clip them
    overlapping = segs.filter(~((pl.col("end_s") <= f) | (pl.col("start_s") >= t)))

    if overlapping.is_empty():
        return new_segments_table([])

    # Clip the start and end times
    clipped = overlapping.with_columns(
        [
            pl.when(pl.col("start_s") < f)
            .then(f)
            .otherwise(pl.col("start_s"))
            .alias("start_s"),
            pl.when(pl.col("end_s") > t)
            .then(t)
            .otherwise(pl.col("end_s"))
            .alias("end_s"),
        ]
    )

    return clipped


def _filter_segments_by_mention_times(
    segs: SegmentsTable,
    mentions: MentionsTable,
    tdo_start_times: dict[str, datetime] | None = None,
) -> SegmentsTable:
    """Filter segments to only include those that overlap with mention time bounds.

    Args:
        segs: SegmentsTable with segments to filter (using relative times in seconds)
        mentions: MentionsTable with mention time bounds (absolute datetime)
        tdo_start_times: Optional dict mapping tdo_id to TDO start_datetime for temporal filtering

    Returns:
        Filtered SegmentsTable containing only segments within mention time bounds
    """
    if segs.is_empty() or mentions.is_empty():
        return new_segments_table([])

    # Get mentions with valid time bounds and TDO IDs
    mentions_with_times = mentions.filter(
        (pl.col("hitStartDateTime").is_not_null())
        & (pl.col("hitEndDateTime").is_not_null())
        & (pl.col("temporalDataObject_id").is_not_null())
    )

    if mentions_with_times.is_empty():
        return new_segments_table([])

    # If we don't have TDO start times, fall back to TDO-level filtering
    if not tdo_start_times:
        tdo_ids_with_mentions = (
            mentions_with_times["temporalDataObject_id"].unique().to_list()
        )
        return segs.filter(pl.col("tdo_id").is_in(tdo_ids_with_mentions))

    # Do precise temporal filtering using TDO start times
    filtered_segments = []

    def _normalize_datetime(dt: datetime) -> datetime:
        """Convert datetime to naive UTC if it has timezone info, or treat as UTC if already naive."""
        if dt.tzinfo is not None:
            # Convert to UTC and remove timezone info
            utc_dt = dt.utctimetuple()
            return datetime(*utc_dt[:6])
        return dt

    for mention_row in mentions_with_times.iter_rows(named=True):
        tdo_id = mention_row["temporalDataObject_id"]
        hit_start = mention_row["hitStartDateTime"]
        hit_end = mention_row["hitEndDateTime"]

        # Get TDO start time to convert absolute mention times to relative times
        tdo_start = tdo_start_times.get(tdo_id)
        if not tdo_start:
            # If we don't have the TDO start time, include all segments from this TDO
            tdo_segments = segs.filter(pl.col("tdo_id") == tdo_id)
            if not tdo_segments.is_empty():
                filtered_segments.append(tdo_segments)
            continue

        try:
            # Normalize datetimes to handle timezone issues
            hit_start_norm = _normalize_datetime(hit_start)
            hit_end_norm = _normalize_datetime(hit_end)
            tdo_start_norm = _normalize_datetime(tdo_start)

            # Convert mention absolute times to relative seconds within the TDO
            hit_start_relative_s = (hit_start_norm - tdo_start_norm).total_seconds()
            hit_end_relative_s = (hit_end_norm - tdo_start_norm).total_seconds()

            # Filter segments from this TDO that overlap with the mention time bounds
            tdo_segments = segs.filter(
                (pl.col("tdo_id") == tdo_id)
                &
                # Overlap condition: not (segment_end <= mention_start or segment_start >= mention_end)
                ~(
                    (pl.col("end_s") <= hit_start_relative_s)
                    | (pl.col("start_s") >= hit_end_relative_s)
                )
            )

            if not tdo_segments.is_empty():
                filtered_segments.append(tdo_segments)

        except (TypeError, AttributeError) as e:
            log.warning(
                f"Could not process mention times for TDO {tdo_id}: {e}. Using TDO-level filtering."
            )
            # Fall back to including all segments from this TDO
            tdo_segments = segs.filter(pl.col("tdo_id") == tdo_id)
            if not tdo_segments.is_empty():
                filtered_segments.append(tdo_segments)

    # Combine all filtered segments and deduplicate
    if filtered_segments:
        combined = pl.concat(filtered_segments, how="diagonal")
        # Remove exact duplicates based on core segment identity
        return combined.unique(subset=["tdo_id", "start_s", "end_s", "signal", "label"])
    else:
        return new_segments_table([])


def _build_abs_time_filters(abs_time: AbsTime | None) -> list[dict[str, Any]]:
    """
    Build search-server range filters for absolute/wall-clock time.
    NOTE: Field names may vary per index; adjust to what your deployment supports
    (e.g., "recording.absoluteStartTimeMs", "recording.createdTime", "recording.modifiedTime").
    Here we use "recording.absoluteStartTimeMs" with ISO strings when available.
    """
    if not abs_time:
        return []

    filters: list[dict[str, Any]] = []
    rng: dict[str, Any] = {}

    # Prefer ISO if provided
    if abs_time.from_iso:
        rng["gte"] = abs_time.from_iso
    if abs_time.to_iso:
        rng["lte"] = abs_time.to_iso

    # Else fall back to epoch seconds (server must accept it for that field)
    if not rng:
        if abs_time.from_epoch_s is not None:
            rng["gte"] = abs_time.from_epoch_s
        if abs_time.to_epoch_s is not None:
            rng["lte"] = abs_time.to_epoch_s

    if rng:
        filters.append(
            {"operator": "range", "field": "recording.absoluteStartTimeMs", **rng}
        )

    return filters


def _and_query(
    main: dict[str, Any],
    extra_filters: list[dict[str, Any]] | dict[str, Any] | None
) -> dict[str, Any]:
    """
    Combine main query with extra filters using AND operator.
    
    Args:
        main: Main query dict
        extra_filters: Additional filter(s) to combine with main query
    
    Returns:
        Combined query dict
    """
    if not extra_filters:
        return main
    if isinstance(extra_filters, dict):
        extra_filters = [extra_filters]
    return {
        "operator": "and",
        "conditions": [main] + extra_filters,
    }


class ContentIntelligenceClient:
    """Client class that handles all content intelligence operations for aiWARE."""

    def __init__(self, aiware_client: AsyncAiware):
        self.client: AsyncAgentsAiware = AsyncAgentsAiware.extend_async(aiware_client)
        # TODO: hack until we can set timeout in search_media
        self.client.http_client.timeout = 60

    async def _get_tdo_ids_from_target(self, target: TargetSelector) -> list[str]:
        """Get list of TDO IDs from the target selector.

        Given a TargetSelector, return the list of TDO IDs it represents, for example all TDOs in a folder.

        Args:
            target: TargetSelector to specify which TDOs to retrieve.

        Returns:
            List of TDO IDs.
        """
        match target:
            case TargetByOrg():
                # Get all TDO IDs in the org
                raise NotImplementedError("org-based search not implemented yet")
            case TargetByIds(tdo_ids=ids):
                return ids
            case TargetByFolder(folder_id=fid, folder_name=None):
                # TODO: some limit here, pagination probably does not make sense as we don't want to operate on too many TDOs
                if fid:
                    folder = await self.client.get_folder(id=fid, tdoLimit=TDO_LIMIT)
                    if (
                        folder
                        and folder.folder
                        and folder.folder.childTDOs
                        and folder.folder.childTDOs.records
                    ):
                        return list(
                            set(
                                [
                                    tdo.id
                                    for tdo in folder.folder.childTDOs.records
                                    if tdo and tdo.id
                                ]
                            )
                        )
                raise ValueError(f"Folder not found or has no TDOs: {fid}")
            case TargetByFolder(folder_id=None, folder_name=_):
                raise NotImplementedError(
                    "folder_name-based search not implemented yet"
                )
            case TargetByWatchlist(watchlist_id=wid):
                # TODO: some limit here, pagination probably does not make sense as we don't want to operate on too many TDOs
                mentions = await self.client.get_mentions(
                    watchlistid=wid, limit=WATCHLIST_MENTIONS_LIMIT
                )
                tdo_ids = []
                if mentions and mentions.mentions and mentions.mentions.records:
                    for mention in mentions.mentions.records:
                        if (
                            mention
                            and mention.temporalDataObject
                            and mention.temporalDataObject.id
                        ):
                            tdo_ids.append(mention.temporalDataObject.id)
                return tdo_ids
            case TargetByMention(mention_id=mid):
                mention = await self.client.get_mentions(id=mid, limit=1)
                if (
                    mention
                    and mention.mentions
                    and mention.mentions.records
                    and len(mention.mentions.records) > 0
                    and mention.mentions.records[0].temporalDataObject
                    and mention.mentions.records[0].temporalDataObject.id
                ):
                    return [mention.mentions.records[0].temporalDataObject.id]
                else:
                    raise ValueError(f"Mention not found or has no TDO: {mid}")
            case _:
                raise TypeError(f"Unhandled target: {target!r}")

    @async_lru.alru_cache(ttl=180)
    async def _entities_to_ids(self, library_type: str) -> dict[str, list[str]]:
        """
        Cache all entity names to IDs mapping for the org.

        Returns:
            Dict mapping lowercased entity names to list of entity IDs.

        Note: names may not be unique, hence list of IDs.
        """
        limit = 500
        cnt = limit
        offset = 0
        # TODO: build this with fuzzy search etc.
        # TODO: handle libraryTypeId='people' etc.
        # Cache name->id mapping for entities in all libraries, names might not be unique
        entity_map = {}
        libs = await self.client.get_libraries()
        if not (libs and libs.libraries and libs.libraries.records):
            return entity_map
        lib_ids = [
            lib.id
            for lib in libs.libraries.records
            if lib and lib.libraryTypeId == library_type
        ]

        while cnt >= limit:
            entities = await self.client.get_entities(
                libraryIds=lib_ids, limit=limit, offset=offset, timeout=60
            )
            if entities and entities.entities and entities.entities.records:
                cnt = len(entities.entities.records)
                for entity in entities.entities.records:
                    if entity and entity.name and entity.id:
                        entity_map.setdefault(entity.name.lower(), []).append(entity.id)
            else:
                cnt = 0
            offset += cnt
        return entity_map

    async def _find_entity_by_name(self, name: str, library_type: str) -> list[str]:
        """Find entity IDs by exact name match (case-insensitive).

        Args:
            name: Entity name to search for.
            library_type: Type of entity, e.g. "person" or "logo".

        Returns:
            List of entity IDs matching the name.

        Raises ValueError if not found.
        """
        entity_map = await self._entities_to_ids(library_type)
        log.info(
            f"Searching for entity name '{name}' in map: {len(entity_map)} entries"
        )
        entity_ids = entity_map.get(name.strip().lower())
        if not entity_ids:
            raise ValueError(f"Entity not found: {name}")
        return entity_ids

    async def search_paginated(
        self,
        req: SearchRequest,
        segments_converter: Callable[[SliceSearchResult], SegmentsTable],
    ) -> SegmentsTable:
        """Helper to do paginated search and convert results to segments.
            Handles pagination by repeatedly querying until fewer results than `limit` are returned.

        Args:
            req: SearchRequest with initial query, index, limit, offset (offset will be modified).
            segments_converter: Function to convert SliceSearchResult to SegmentsTable.

        Returns:
            SegmentsTable with all results concatenated.

        Note: modifies req.offset and req.limit
        """
        req.offset = 0
        if not req.limit:
            req.limit = 100
        cnt = req.limit
        segs_list = []
        while cnt >= req.limit:
            results: SliceSearchResult = await self.client.search_media(req)
            segs = segments_converter(results)
            segs_list.append(segs)

            if results and results.results:
                cnt = len(results.results)
            else:
                cnt = 0
            req.offset += cnt
        all_segs = pl.concat(segs_list) if segs_list else new_segments_table([])
        return all_segs

    async def _apply_mention_filtering_if_needed(
        self, segs: SegmentsTable, target: TargetSelector
    ) -> SegmentsTable:
        """Apply mention-based temporal filtering if target is a mention or watchlist.

        Args:
            segs: SegmentsTable to filter
            target: The target selector that was used for the search

        Returns:
            Filtered SegmentsTable if target is mention/watchlist, otherwise original segs
        """
        if not isinstance(target, (TargetByMention, TargetByWatchlist)):
            return segs

        if segs.is_empty():
            return segs

        # Get mentions metadata which includes the time bounds
        mentions_metadata = await self._get_mentions_metadata_for_target(target)

        if mentions_metadata.is_empty():
            return new_segments_table([])

        # Get TDO start times for precise temporal filtering
        tdo_ids = mentions_metadata["temporalDataObject_id"].to_list()
        tdo_target = TargetByIds(kind="tdo_ids", tdo_ids=tdo_ids)
        tdos = await self.get_tdos(tdo_target, include_segments=False)
        tdo_start_times = {
            getattr(tdo, "tdo_id"): getattr(tdo, "start_datetime")
            for tdo in tdos
            if getattr(tdo, "start_datetime", None)
        }

        # Filter segments to only those within mention time bounds
        return _filter_segments_by_mention_times(
            segs, mentions_metadata, tdo_start_times
        )

    async def _build_target_query(
        self, target: TargetSelector | None
    ) -> dict[str, Any] | None:
        """Build a query fragment for the target, resolving complex targets to TDO IDs."""
        if not target:
            return None

        match target:
            case TargetByOrg():
                return None
            case TargetByIds(tdo_ids=ids):
                return {"operator": "terms", "field": "recordingId", "values": ids}
            case TargetByFolder() | TargetByWatchlist() | TargetByMention():
                # Resolve complex targets to TDO IDs
                tdo_ids = await self._get_tdo_ids_from_target(target)
                return {"operator": "terms", "field": "recordingId", "values": tdo_ids}
            case _:
                raise TypeError(f"Unhandled target: {target!r}")

    async def find_transcript(
        self, op: FindTranscriptOp, target: TargetSelector
    ) -> SegmentsTable:
        """Find transcript segments matching the query and target.

        Args:
            op: FindTranscriptOp with query, abs_time, media_time, granularity.
            target: TargetSelector to limit the search scope.

        Returns:
            SegmentsTable with transcript segments matching the criteria.
        """
        escaped_query = _escape_elasticsearch_query(op.query.lower())
        base_query = {
            "operator": "query_string",
            "field": "transcript.transcript",
            "value": escaped_query,
        }
        query = _and_query(base_query, _build_abs_time_filters(op.abs_time))
        query = _and_query(query, await self._build_target_query(target))
        req = SearchRequest(index=["mine"], query=query, limit=80)

        log.info("Query: %s", query)
        log.debug("Transcript search: %s", req)
        # Use granularity from op to determine processing mode
        if op.granularity in ("window", "sentence"):
            segs = await self.search_paginated(req, transcript_windows_to_segments)
        elif op.granularity in ("token", "word"):
            segs = await self.search_paginated(req, transcript_tokens_to_segments)
        else:
            raise ValueError(f"unknown granularity {op.granularity}")

        # Apply media_time clipping
        segs = _clip_by_media_time(segs, op.media_time)

        # Apply mention filtering if needed
        segs = await self._apply_mention_filtering_if_needed(segs, target)

        return segs

    async def find_face(self, op: FindFaceOp, target: TargetSelector) -> SegmentsTable:
        """Find face segments by entityId or entity name.

        Args:
            op: FindFaceOp with where clause containing either 'entityId' or 'name'.
            target: TargetSelector to limit the search scope.

        Returns:
            SegmentsTable with face segments matching the criteria.
        """
        name = op.where.get("name")
        if "entityId" in op.where:
            entity_ids = [op.where.get("entityId")]
        else:
            if name:
                entity_ids = await self._find_entity_by_name(
                    name, library_type="people"
                )
                if not entity_ids:
                    raise ValueError(f"Entity not found: {name}")
            else:
                raise ValueError(
                    "find_face.where must include {'entityId': '...'} or {'name': '...'}"
                )

        base_query = {
            "operator": "terms",
            "field": "face-recognition.series.entityId",
            "values": entity_ids,
        }
        query = _and_query(base_query, _build_abs_time_filters(op.abs_time))
        query = _and_query(query, await self._build_target_query(target))

        req = SearchRequest(index=["mine"], query=query, limit=500)
        segs = await self.search_paginated(
            req, partial(face_detections_to_segments, inject_label=name)
        )

        # Apply media_time clipping
        segs = _clip_by_media_time(segs, op.media_time)

        # Apply mention filtering if needed
        segs = await self._apply_mention_filtering_if_needed(segs, target)

        return segs

    async def find_logo(self, op: FindLogoOp, target: TargetSelector) -> SegmentsTable:
        """Find logo segments by entityId or entity name.

        Args:
            op: FindLogoOp with where clause containing either 'entityId' or 'name'.
            target: TargetSelector to limit the search scope.

        Returns:
            SegmentsTable with logo segments matching the criteria.
        """
        # TODO: seems logos don't really use entity IDs in general
        if "entityId" in op.where:
            entity_ids = [op.where.get("entityId")]
        else:
            name = op.where.get("name")
            if name:
                entity_ids = [name]
                # TODO: fuzzy find in aggregate logo list, currently library does not seem to be used for logos

                # entity_ids = await self._find_entity_by_name(name, library_type="logos")
                # if not entity_ids:
                #    raise ValueError(f"Entity not found: {name}")
            else:
                raise ValueError(
                    "find_logo.where must include {'entityId': '...'} or {'name': '...'}"
                )

        base_query = {
            "operator": "terms",
            "field": "logo-recognition.series.found",
            "values": entity_ids,
        }
        query = _and_query(base_query, _build_abs_time_filters(op.abs_time))
        query = _and_query(query, await self._build_target_query(target))

        req = SearchRequest(index=["mine"], query=query, limit=500)
        log.debug("Logo search: %s", req)
        segs = await self.search_paginated(req, logo_detections_to_segments)

        # Apply media_time clipping
        segs = _clip_by_media_time(segs, op.media_time)

        # Apply mention filtering if needed
        segs = await self._apply_mention_filtering_if_needed(segs, target)

        return segs

    @async_lru.alru_cache(ttl=300)  # Cache for 5 minutes
    async def get_watchlists(self, limit: int = 100) -> WatchlistsTable:
        """Get all watchlists."""
        watchlists_response = await self.client.get_watchlists(limit=limit)
        rows = []

        if (
            watchlists_response
            and watchlists_response.watchlists
            and watchlists_response.watchlists.records
        ):
            for wl in watchlists_response.watchlists.records:
                if wl:
                    # Create dict directly using schema fields to avoid duplication
                    rows.append(
                        {
                            "name": wl.name,
                            "startDateTime": wl.startDateTime,
                            "stopDateTime": wl.stopDateTime,
                            "createdDateTime": wl.createdDateTime,
                            "details": convert_jsondata_to_dict(wl.details),
                            "isDisabled": wl.isDisabled,
                            "watchlistType": wl.watchlistType,
                            "advertiser": convert_jsondata_to_dict(wl.advertiser),
                            "brand": convert_jsondata_to_dict(wl.brand),
                        }
                    )

        return new_watchlists_table(rows)

    @async_lru.alru_cache(ttl=300)  # Cache for 5 minutes
    async def get_watchlist_by_id(self, watchlist_id: str) -> WatchlistsTable:
        """Get a specific watchlist by ID."""
        watchlist_response = await self.client.get_watchlists(id=watchlist_id, limit=1)
        rows = []

        if (
            watchlist_response
            and watchlist_response.watchlists
            and watchlist_response.watchlists.records
            and len(watchlist_response.watchlists.records) > 0
        ):
            wl = watchlist_response.watchlists.records[0]
            if wl:
                # Create dict directly using schema fields to avoid duplication
                rows.append(
                    {
                        "name": wl.name,
                        "startDateTime": wl.startDateTime,
                        "stopDateTime": wl.stopDateTime,
                        "createdDateTime": wl.createdDateTime,
                        "details": convert_jsondata_to_dict(wl.details),
                        "isDisabled": wl.isDisabled,
                        "watchlistType": wl.watchlistType,
                        "advertiser": convert_jsondata_to_dict(wl.advertiser),
                        "brand": convert_jsondata_to_dict(wl.brand),
                    }
                )

        return new_watchlists_table(rows)

    @async_lru.alru_cache(ttl=180)  # Cache for 3 minutes
    async def get_mentions_by_watchlist(
        self, watchlist_id: str, limit: int
    ) -> MentionsTable:
        """Get mentions metadata for a watchlist."""
        mentions_response = await self.client.get_mentions(
            watchlistid=watchlist_id, limit=limit
        )
        rows = []

        if (
            mentions_response
            and mentions_response.mentions
            and mentions_response.mentions.records
        ):
            for mention in mentions_response.mentions.records:
                if mention:
                    # Create dict directly using schema fields to avoid duplication
                    rows.append(
                        {
                            "id": mention.id,
                            "sourceId": mention.sourceId,
                            "audienceMarketCount": mention.audienceMarketCount,
                            "audienceAffiliateCount": mention.audienceAffiliateCount,
                            "mentionHitCount": mention.mentionHitCount,
                            "audience": mention.audience,
                            "advertiser": convert_jsondata_to_dict(mention.advertiser),
                            "brand": convert_jsondata_to_dict(mention.brand),
                            "metadata": convert_jsondata_to_dict(mention.metadata),
                            "temporalDataObject_id": mention.temporalDataObject.id
                            if mention.temporalDataObject
                            else None,
                            "hitStartDateTime": mention.hitStartDateTime,
                            "hitEndDateTime": mention.hitEndDateTime,
                        }
                    )

        return new_mentions_table(rows)

    @async_lru.alru_cache(ttl=180)  # Cache for 3 minutes
    async def get_mention_by_id(self, mention_id: str) -> MentionsTable:
        """Get a specific mention by ID."""
        mention_response = await self.client.get_mentions(id=mention_id, limit=1)
        rows = []

        if (
            mention_response
            and mention_response.mentions
            and mention_response.mentions.records
            and len(mention_response.mentions.records) > 0
        ):
            mention = mention_response.mentions.records[0]
            if mention:
                # Create dict directly using schema fields to avoid duplication
                rows.append(
                    {
                        "id": mention.id,
                        "sourceId": mention.sourceId,
                        "audienceMarketCount": mention.audienceMarketCount,
                        "audienceAffiliateCount": mention.audienceAffiliateCount,
                        "mentionHitCount": mention.mentionHitCount,
                        "audience": mention.audience,
                        "advertiser": convert_jsondata_to_dict(mention.advertiser),
                        "brand": convert_jsondata_to_dict(mention.brand),
                        "metadata": convert_jsondata_to_dict(mention.metadata),
                        "temporalDataObject_id": mention.temporalDataObject.id
                        if mention.temporalDataObject
                        else None,
                        "hitStartDateTime": mention.hitStartDateTime,
                        "hitEndDateTime": mention.hitEndDateTime,
                    }
                )

        return new_mentions_table(rows)

    async def get_tdos(
        self, target: TargetSelector, include_segments: bool = True
    ) -> list[MediaTDO]:
        """Get MediaTDO objects for the given target.

        Args:
            target: TargetSelector to specify which TDOs to retrieve.
            include_segments: Whether to include segments (i.e. reading AION) in the MediaTDO objects or just metadata.

        Returns:
            List of MediaTDO objects.
        """
        tdo_ids = await self._get_tdo_ids_from_target(target)
        tdos = await MediaTDO.from_tdo_ids(
            self.client, tdo_ids, include_segments=include_segments
        )
        return tdos

    async def get_tdo_transcript(
        self, op: GetTranscriptsOp, target: TargetSelector
    ) -> SegmentsTable:
        """Get transcript segments for TDOs in the target.

        Args:
            op: GetTranscriptsOp with optional media_time to clip segments.
            target: TargetSelector to specify which TDOs to retrieve transcripts for.

        Returns:
            SegmentsTable with transcript segments from the TDOs.
        """
        # Get raw segments without coalescing
        result_df = await self._get_raw_tdo_transcript_segments(target)

        if result_df.is_empty():
            return new_segments_table([])

        # Apply coalescing based on granularity
        if op.granularity == "utterance":
            return coalesce_segments(result_df, tolerance_s=0.1)
        elif op.granularity == "full":
            return coalesce_segments(result_df, tolerance_s=None)
        else:
            return result_df

    async def _get_raw_tdo_transcript_segments(
        self, target: TargetSelector
    ) -> SegmentsTable:
        """Get raw transcript segments for TDOs without any coalescing.

        Args:
            target: TargetSelector to specify which TDOs to retrieve transcripts for.

        Returns:
            SegmentsTable with raw transcript segments from the TDOs.
        """
        result_dfs = []
        tdo_ids = await self._get_tdo_ids_from_target(target)
        tdos = await MediaTDO.from_tdo_ids(self.client, tdo_ids, include_segments=True)
        for tdo in tdos:
            transcript_segments = tdo.segments.get("transcript")
            if transcript_segments is not None and not transcript_segments.is_empty():
                result_dfs.append(transcript_segments)

        if result_dfs:
            return pl.concat(result_dfs)
        return new_segments_table([])

    async def _get_tdo_segments_by_signal(
        self, signal: str, target: TargetSelector
    ) -> SegmentsTable:
        """Get segments of a specific signal type for TDOs in the target.

        Args:
            signal: The signal type to retrieve ("face", "logo", "ocr", etc.).
            target: TargetSelector to specify which TDOs to retrieve segments for.

        Returns:
            SegmentsTable with segments of the specified signal type from the TDOs.
        """
        result_dfs = []
        tdo_ids = await self._get_tdo_ids_from_target(target)
        tdos = await MediaTDO.from_tdo_ids(self.client, tdo_ids, include_segments=True)
        for tdo in tdos:
            segments = tdo.segments.get(signal)
            if segments is not None and not segments.is_empty():
                result_dfs.append(segments)

        if result_dfs:
            return pl.concat(result_dfs)
        else:
            return new_segments_table([])

    async def get_tdo_faces(
        self, op: GetFacesOp, target: TargetSelector
    ) -> SegmentsTable:
        """Get face segments for TDOs in the target.

        Args:
            op: GetFacesOp with optional media_time to clip segments.
            target: TargetSelector to specify which TDOs to retrieve faces for.

        Returns:
            SegmentsTable with face segments from the TDOs.
        """
        return await self._get_tdo_segments_by_signal("face", target)

    async def get_tdo_logos(
        self, op: GetLogosOp, target: TargetSelector
    ) -> SegmentsTable:
        """Get logo segments for TDOs in the target.

        Args:
            op: GetLogosOp with optional media_time to clip segments.
            target: TargetSelector to specify which TDOs to retrieve logos for.

        Returns:
            SegmentsTable with logo segments from the TDOs.
        """
        return await self._get_tdo_segments_by_signal("logo", target)

    async def get_tdo_ocrs(
        self, op: GetOcrsOp, target: TargetSelector
    ) -> SegmentsTable:
        """Get OCR segments for TDOs in the target.

        Args:
            op: GetOcrsOp with optional media_time to clip segments.
            target: TargetSelector to specify which TDOs to retrieve OCRs for.

        Returns:
            SegmentsTable with OCR segments from the TDOs.
        """
        return await self._get_tdo_segments_by_signal("ocr", target)

    async def get_mention_transcript(
        self, op: GetTranscriptsOp, target: TargetSelector
    ) -> tuple[SegmentsTable, MentionsTable]:
        """Get transcript segments from TDOs referenced by mentions, filtered by mention time bounds.

        Args:
            op: GetTranscriptsOp with optional media_time to clip segments.
            target: TargetSelector to specify which mentions to retrieve transcripts for.

        Returns:
            Tuple of (SegmentsTable with transcript segments, MentionsTable with metadata).
        """
        # Get mentions metadata which includes the time bounds
        mentions_metadata = await self._get_mentions_metadata_for_target(target)

        if mentions_metadata.is_empty():
            return new_segments_table([]), new_mentions_table([])

        # Get RAW segments from the TDOs referenced by these mentions (without coalescing)
        tdo_ids = mentions_metadata["temporalDataObject_id"].to_list()
        tdo_target = TargetByIds(kind="tdo_ids", tdo_ids=tdo_ids)
        all_raw_segs = await self._get_raw_tdo_transcript_segments(tdo_target)

        # Get TDO start times for precise temporal filtering
        tdos = await self.get_tdos(tdo_target, include_segments=False)
        tdo_start_times = {
            getattr(tdo, "tdo_id"): getattr(tdo, "start_datetime")
            for tdo in tdos
            if getattr(tdo, "start_datetime", None)
        }

        # Filter RAW segments to only those within mention time bounds
        filtered_segs = _filter_segments_by_mention_times(
            all_raw_segs, mentions_metadata, tdo_start_times
        )

        # NOW apply coalescing based on granularity (after filtering)
        if not filtered_segs.is_empty():
            if op.granularity == "utterance":
                filtered_segs = coalesce_segments(filtered_segs, tolerance_s=0.1)
            elif op.granularity == "full":
                filtered_segs = coalesce_segments(filtered_segs, tolerance_s=None)

        return filtered_segs, mentions_metadata

    async def _get_mention_segments_by_signal(
        self, signal: str, target: TargetSelector
    ) -> tuple[SegmentsTable, MentionsTable]:
        """Get segments of a specific signal type from TDOs referenced by mentions, filtered by mention time bounds.

        Args:
            signal: The signal type to retrieve ("face", "logo", "ocr").
            target: TargetSelector to specify which mentions to retrieve segments for.

        Returns:
            Tuple of (SegmentsTable with segments, MentionsTable with metadata).
        """
        # Get mentions metadata which includes the time bounds
        mentions_metadata = await self._get_mentions_metadata_for_target(target)

        if mentions_metadata.is_empty():
            return new_segments_table([]), new_mentions_table([])

        # Get all segments from the TDOs referenced by these mentions
        tdo_ids = mentions_metadata["temporalDataObject_id"].to_list()
        tdo_target = TargetByIds(kind="tdo_ids", tdo_ids=tdo_ids)
        all_segs = await self._get_tdo_segments_by_signal(signal, tdo_target)

        # Get TDO start times for precise temporal filtering
        tdos = await self.get_tdos(tdo_target, include_segments=False)
        tdo_start_times = {
            getattr(tdo, "tdo_id"): getattr(tdo, "start_datetime")
            for tdo in tdos
            if getattr(tdo, "start_datetime", None)
        }

        # Filter segments to only those within mention time bounds
        filtered_segs = _filter_segments_by_mention_times(
            all_segs, mentions_metadata, tdo_start_times
        )

        return filtered_segs, mentions_metadata

    async def get_mention_faces(
        self, op: GetFacesOp, target: TargetSelector
    ) -> tuple[SegmentsTable, MentionsTable]:
        """Get face segments from TDOs referenced by mentions, filtered by mention time bounds.

        Args:
            op: GetFacesOp with optional media_time to clip segments.
            target: TargetSelector to specify which mentions to retrieve faces for.

        Returns:
            Tuple of (SegmentsTable with face segments, MentionsTable with metadata).
        """
        return await self._get_mention_segments_by_signal("face", target)

    async def get_mention_logos(
        self, op: GetLogosOp, target: TargetSelector
    ) -> tuple[SegmentsTable, MentionsTable]:
        """Get logo segments from TDOs referenced by mentions, filtered by mention time bounds.

        Args:
            op: GetLogosOp with optional media_time to clip segments.
            target: TargetSelector to specify which mentions to retrieve logos for.

        Returns:
            Tuple of (SegmentsTable with logo segments, MentionsTable with metadata).
        """
        return await self._get_mention_segments_by_signal("logo", target)

    async def get_mention_ocrs(
        self, op: GetOcrsOp, target: TargetSelector
    ) -> tuple[SegmentsTable, MentionsTable]:
        """Get OCR segments from TDOs referenced by mentions, filtered by mention time bounds.

        Args:
            op: GetOcrsOp with optional media_time to clip segments.
            target: TargetSelector to specify which mentions to retrieve OCRs for.

        Returns:
            Tuple of (SegmentsTable with OCR segments, MentionsTable with metadata).
        """
        return await self._get_mention_segments_by_signal("ocr", target)

    async def _get_mentions_metadata_for_target(
        self, target: TargetSelector
    ) -> MentionsTable:
        """Get mentions metadata for a target."""
        match target:
            case TargetByMention(mention_id=mid):
                return await self.get_mention_by_id(mid)
            case TargetByWatchlist(watchlist_id=wid):
                return await self.get_mentions_by_watchlist(
                    wid, limit=WATCHLIST_MENTIONS_LIMIT
                )
            case _:
                return new_mentions_table([])
