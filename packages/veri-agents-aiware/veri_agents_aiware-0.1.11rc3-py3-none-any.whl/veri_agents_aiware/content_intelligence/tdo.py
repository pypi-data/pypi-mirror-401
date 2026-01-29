from datetime import datetime
import logging
import asyncio
import async_lru

from aiware.aion import Aion, AionObjectType, AionSeries, AionObject
from .data import (
    Signal,
    SegmentsTable,
    create_segment_dict,
    new_segments_table,
    TDO_SCHEMA,
)
from .parallel_downloading import adownload_all

from veri_agents_aiware.aiware_client.async_client import AsyncAgentsAiware
from veri_agents_aiware.aiware_client.client_generated.rag_get_tdo_content import (
    RAGGetTDOContentTemporalDataObject,
)

logger = logging.getLogger(__name__)


def engine_category_in_signals(engine_category: str, signals: list[Signal]) -> bool:
    """Check if the engine category corresponds to any of the requested signals."""
    # Currently this is a straight 1:1 mapping, in case this changes we can expand this function
    if engine_category in signals:
        return True
    return False


class MediaTDO:
    """Simple wrapper around aiWARE TDO data with segments.

    Uses the same field names as TDO_SCHEMA to avoid duplication.
    """

    def __init__(self, **kwargs):
        # Store all TDO fields directly using schema field names
        for field_name in TDO_SCHEMA.keys():
            setattr(self, field_name, kwargs.get(field_name))

        # Segments are separate
        self.segments: dict[str, SegmentsTable] = kwargs.get("segments", {})

    def to_dict(self) -> dict:
        """Convert to dict compatible with TDO_SCHEMA."""
        return {field: getattr(self, field, None) for field in TDO_SCHEMA.keys()}

    def to_table_row(self) -> dict:
        """Get a single row dict for creating a TDO table."""
        return self.to_dict()

    @classmethod
    # disable caching for now, we currently don't see plans fetching the same signal twice in a short time
    # and it needs a lot of memory
    #@async_lru.alru_cache(maxsize=2048, ttl=300)
    async def _fetch_segments(
        cls, aion_uris: list[str], tdo_id: str
    ) -> dict[str, SegmentsTable]:
        aion_jsons = await adownload_all(aion_uris, max_concurrent=50, timeout=120)

        # Parse them to Aion objects, populate segments
        segments_data: dict[str, list[dict]] = {}  # Signal -> list of segment dicts
        for aj in aion_jsons:
            # TODO: hack until OCR is in Aion library
            AionObjectType.OCR = "OCR"  # type: ignore

            try:
                aion = Aion.model_validate(aj, strict=False)
            except Exception as e:
                # logger.error("Failed to parse AION JSON for TDO  %s", str(tdo_id))
                continue

            if aion.series is None:
                logger.warning("Non-series AION (currently) ignored for TDO %s", tdo_id)
            else:
                for s in aion.series:
                    channel = label = confidence = transcript = None
                    signal: Signal | None = None

                    match s:
                        # Logo detections
                        case AionSeries(
                            object=AionObject(type=AionObjectType.LOGO) as obj
                        ):
                            channel = "video"
                            signal = "logo"
                            label = obj.label
                            confidence = obj.confidence

                        # Object detections
                        case AionSeries(
                            object=AionObject(type=AionObjectType.OBJECT) as obj
                        ):
                            channel = "video"
                            signal = "object"
                            label = obj.label
                            confidence = obj.confidence

                        # Face detections
                        case AionSeries(
                            object=AionObject(type=AionObjectType.FACE) as obj
                        ):
                            channel = "video"
                            signal = "face"
                            label = obj.label
                            confidence = obj.confidence

                        # OCR
                        case AionSeries(
                            object=AionObject(type=AionObjectType.OCR) as obj
                        ):
                            channel = "video"
                            signal = "ocr"
                            label = obj.text  # text instead of label
                            confidence = obj.confidence

                        # Transcript
                        case AionSeries(words=words) if words:
                            channel = "audio"
                            signal = "transcript"
                            transcript = " ".join(
                                w.word for w in words if w.word and w.best_path
                            )

                        # Unhandled cases
                        case _:
                            logger.warning(
                                "Skipping unhandled AionSeries (TDO %s)", tdo_id
                            )
                            continue

                    if signal not in segments_data:
                        segments_data[signal] = []

                    segment_dict = create_segment_dict(
                        tdo_id=tdo_id,
                        start_s=s.start_time_ms / 1000.0,
                        end_s=s.stop_time_ms / 1000.0,
                        channel=channel,
                        signal=signal or "unknown",
                        score=confidence,
                        label=label,
                        transcript=transcript,
                        engine_id=aion.source_engine_id,
                        engine_name=aion.source_engine_name,
                        # abs_start_epoch_s=None,
                        # abs_end_epoch_s=None,
                        # bbox=None,
                        # poly=None,
                        # meta={},
                    )
                    segments_data[signal].append(segment_dict)

        # Convert segment data to DataFrames
        segments: dict[str, SegmentsTable] = {}
        for signal_key, data in segments_data.items():
            segments[signal_key] = new_segments_table(data)
        return segments

    @classmethod
    async def from_tdo_ids(
        cls,
        aiware: AsyncAgentsAiware,
        tdo_ids: list[str],
        include_segments: bool = True,
        signals: list[Signal] | None = None,
    ) -> list["MediaTDO"]:
        """Fetch multiple TDOs in parallel.

        Args:
            aiware: AsyncAgentsAiware client.
            tdo_ids: List of TDO IDs to fetch.
            include_segments: Whether to download and parse segments.
            signals: Optional list of signals to filter segments by.
        """
        # make sure we're not pulling the same IDs twice:
        unique_tdo_ids = list(set(tdo_ids))
        tasks = [
            cls.from_tdo_id(aiware, tdo_id, include_segments, signals=signals)
            for tdo_id in unique_tdo_ids
        ]
        return [tdo for tdo in await asyncio.gather(*tasks) if tdo]

    @classmethod
    @async_lru.alru_cache(maxsize=1024, ttl=300)
    async def _fetch_tdo_content(
        cls, aiware: AsyncAgentsAiware, tdo_id: str
    ) -> RAGGetTDOContentTemporalDataObject | None:
        """Fetch TDO content with caching.

        Args:
            aiware: AsyncAgentsAiware client.
            tdo_id: TDO ID to fetch.

        Returns:
            RAGGetTDOContentTemporalDataObject or None if not found.
        """
        return (
            await aiware.rag_get_tdo_content(tdo_id, timeout=120)
        ).temporalDataObject

    @classmethod
    async def from_tdo_id(
        cls,
        aiware: AsyncAgentsAiware,
        tdo_id: str,
        include_segments: bool = True,
        signals: list[Signal] | None = None,
    ) -> "MediaTDO | None":
        """Fetch a TDO by ID, optionally download and parse its AION assets.

        Args:
            aiware: AsyncAgentsAiware client.
            tdo_id: TDO ID to fetch.
            include_segments: Whether to download and parse segments.
            signals: Optional list of signals to filter segments by.

        Returns:
            MediaTDO instance.
        """
        try:
            tdo = await cls._fetch_tdo_content(aiware, tdo_id)
        except Exception as e:
            logger.error("Error fetching TDO %s: %s", tdo_id, str(e))
            return None
        if tdo is None:
            raise ValueError(f"TDO with id {tdo_id} not found")

        # Extract asset type
        asset_type = None
        aion_uris = []
        if tdo.assets and tdo.assets.records:
            for a in tdo.assets.records:
                try:
                    if a and a.assetType == "vtn-standard" and a.signedUri:
                        engine_category = a.sourceData.engine.category.categoryType  # type: ignore
                        if (
                            signals is None
                            or engine_category is None
                            or engine_category_in_signals(engine_category, signals)
                        ):
                            aion_uris.append(a.signedUri)
                    elif a and a.assetType == "media":
                        asset_type = a.contentType
                except Exception as e:
                    logger.warning(
                        "Error processing asset for TDO %s: %s", tdo_id, str(e)
                    )

        segments = {}
        if include_segments:
            segments = await cls._fetch_segments(aion_uris, tdo_id)

        # Calculate duration
        duration_s = None
        if tdo.startDateTime and tdo.stopDateTime:
            duration_s = (tdo.stopDateTime - tdo.startDateTime).total_seconds()

        # Use TDO_SCHEMA field names directly
        return cls(
            tdo_id=tdo.id,
            tdo_name=tdo.name,
            created_datetime=tdo.createdDateTime,
            asset_type=asset_type,
            start_datetime=tdo.startDateTime,
            stop_datetime=tdo.stopDateTime,
            duration_s=duration_s,
            segments=segments,
        )
