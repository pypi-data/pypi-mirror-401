from __future__ import annotations

import asyncio
import logging
import time
from functools import singledispatchmethod
from typing import Any

import polars as pl
from pydantic import BaseModel, Field
from veri_agents_aiware.content_intelligence.client import ContentIntelligenceClient
from veri_agents_aiware.content_intelligence.data import (
    MentionsTable,
    RecordsTable,
    SegmentsTable,
    Table,
    TargetByMention,
    TargetByWatchlist,
    TargetSelector,
    TdoTable,
    WatchlistsTable,
    coalesce_segments,
    dedupe_segments,
    format_table_delimited,
    new_mentions_table,
    new_tdo_table,
    new_watchlists_table,
)
from veri_agents_aiware.content_intelligence.ops import (
    FindTranscriptOp,
    FindFaceOp,
    FindLogoOp,
    GetOcrsOp,
    GetTranscriptsOp,
    GetFacesOp,
    GetLogosOp,
    ProjectOp,
    FilterOp,
    JoinTemporalOp,
    MergeOp,
    AggregateOp,
    OutputOp,
    SortSpec,
)
from veri_agents_aiware.content_intelligence.plan import InvalidPlanError, Plan
from veri_agents_aiware.content_intelligence.temporal import join_temporal

log = logging.getLogger(__name__)


class ErrorInfo(BaseModel):
    stage: str
    message: str


class State(BaseModel):
    """Models the state of execution for a content intelligence plan.
    
    Initially expects a query, a target and a plan.
    As execution proceeds, tables and results are populated. 
    """
    model_config = {"arbitrary_types_allowed": True}

    query: str
    target: TargetSelector
    plan: Plan | None = None
    tdo_table: TdoTable | None = None
    mentions_table: MentionsTable | None = None
    watchlists_table: WatchlistsTable | None = None
    segments_tables: dict[str, SegmentsTable] = {}
    records_tables: dict[str, RecordsTable] = {}
    answer: Any = None
    errors: list[ErrorInfo] = []
    started_at: float = Field(default_factory=time.time)


# ----------------------- EXECUTOR -----------------------


class Executor:
    """Deterministic executor for Plan steps with singledispatch-based handlers."""

    def __init__(self, client: ContentIntelligenceClient):
        self.client = client

    # ---------------------- public ----------------------

    async def run(self, state: State) -> State:
        """Execute the plan in the given state.
        
        Args:
            state: The current execution state containing the plan and data.
        
        Returns:
            The updated state after executing the plan.
        """
        if not state.plan:
            state.errors.append(ErrorInfo(stage="executor", message="missing plan"))
            return state
        try:
            # data gathering steps can run in parallel
            parallel_steps = []
            sequential_steps = []
            for step in state.plan.steps:
                if step.op.startswith("FIND_") or step.op.startswith("GET_"):
                    parallel_steps.append(step)
                else:
                    sequential_steps.append(step)
            
            # Execute parallel steps
            await asyncio.gather(*(self._handle(step, state) for step in parallel_steps))
            
            # Now the sequential ones
            for step in sequential_steps:
                log.info("[Executor] Executing sequential step: %s", step)
                await self._handle(step, state)  # dispatch on step type
        except Exception as e:
            log.exception("Executor error")
            state.errors.append(ErrorInfo(stage="execute", message=str(e)))
        return state

    # ---------------------- dispatch root ----------------------

    @singledispatchmethod
    async def _handle(self, step: BaseModel, state: State) -> None:
        raise NotImplementedError(f"No handler for {type(step).__name__}")

    # ---------------------- FIND handlers ----------------------

    @_handle.register
    async def _handle_find_transcript(
        self, step: FindTranscriptOp, state: State
    ) -> None:
        log.info("[Executor] Executing FIND_TRANSCRIPT: %s", step)
        segs = await self.client.find_transcript(step, state.target)
        log.info("[Executor] Completed FIND_TRANSCRIPT")
        state.segments_tables[step.output] = segs

    @_handle.register
    async def _handle_find_face(self, step: FindFaceOp, state: State) -> None:
        log.info("[Executor] Executing FIND_FACE: %s", step)
        segs = await self.client.find_face(step, state.target)
        log.info("[Executor] Completed FIND_FACE")
        state.segments_tables[step.output] = segs

    @_handle.register
    async def _handle_find_logo(self, step: FindLogoOp, state: State) -> None:
        log.info("[Executor] Executing FIND_LOGO: %s", step)
        segs = await self.client.find_logo(step, state.target)
        log.info("[Executor] Completed FIND_LOGO")
        state.segments_tables[step.output] = segs

    # ---------------------- GET_* handlers ----------------------

    @_handle.register
    async def _handle_get_transcripts(
        self, step: GetTranscriptsOp, state: State
    ) -> None:
        log.info("[Executor] Executing GET_TRANSCRIPTS: %s", step)
        match state.target:
            case TargetByMention() | TargetByWatchlist():
                segs, metadata = await self.client.get_mention_transcript(step, state.target)
                if state.mentions_table is None:
                    state.mentions_table = metadata
            case _:
                segs = await self.client.get_tdo_transcript(step, state.target)
        state.segments_tables[step.output] = segs
        log.info("[Executor] Completed GET_TRANSCRIPTS")

    @_handle.register
    async def _handle_get_faces(self, step: GetFacesOp, state: State) -> None:
        log.info("[Executor] Executing GET_FACES: %s", step)
        match state.target:
            case TargetByMention() | TargetByWatchlist():
                segs, metadata = await self.client.get_mention_faces(step, state.target)
                if state.mentions_table is None:
                    state.mentions_table = metadata
            case _:
                segs = await self.client.get_tdo_faces(step, state.target)
        state.segments_tables[step.output] = segs
        log.info("[Executor] Completed GET_FACES")

    @_handle.register
    async def _handle_get_logos(self, step: GetLogosOp, state: State) -> None:
        log.info("[Executor] Executing GET_LOGOS: %s", step)
        match state.target:
            case TargetByMention() | TargetByWatchlist():
                segs, metadata = await self.client.get_mention_logos(step, state.target)
                if state.mentions_table is None:
                    state.mentions_table = metadata
            case _:
                segs = await self.client.get_tdo_logos(step, state.target)
        state.segments_tables[step.output] = segs
        log.info("[Executor] Completed GET_LOGOS")

    @_handle.register
    async def _handle_get_ocrs(self, step: GetOcrsOp, state: State) -> None:
        log.info("[Executor] Executing GET_OCRS: %s", step)
        match state.target:
            case TargetByMention() | TargetByWatchlist():
                segs, metadata = await self.client.get_mention_ocrs(step, state.target)
                if state.mentions_table is None:
                    state.mentions_table = metadata
            case _:
                segs = await self.client.get_tdo_ocrs(step, state.target)
        state.segments_tables[step.output] = segs
        log.info("[Executor] Completed GET_OCRS")

    # ---------------------- timeline/table ops ----------------------

    @_handle.register
    async def _handle_project(self, step: ProjectOp, state: State) -> None:
        """Project selected fields from a segments table."""
        segs = state.segments_tables.get(step.input)
        if segs is None:
            raise InvalidPlanError(
                f"PROJECT input alias '{step.input}' not found in segments_tables"
            )
        
        # Build selection expressions with fallback for "_right" suffixed columns
        select_exprs = []
        for p in step.select:
            field_name = p.input_field
            
            # Check if the field exists
            if field_name in segs.columns:
                # Check if the column is all nulls and there's a "_right" version
                if (segs.height > 0 and 
                    segs[field_name].null_count() == segs.height and 
                    f"{field_name}_right" in segs.columns):
                    log.debug(f"Column '{field_name}' is all nulls, using '{field_name}_right' instead")
                    select_exprs.append(pl.col(f"{field_name}_right").alias(p.output_field))
                else:
                    select_exprs.append(pl.col(field_name).alias(p.output_field))
            elif f"{field_name}_right" in segs.columns:
                # Field doesn't exist but "_right" version does
                log.debug(f"Column '{field_name}' not found, using '{field_name}_right' instead")
                select_exprs.append(pl.col(f"{field_name}_right").alias(p.output_field))
            else:
                # Neither exists, let Polars handle the error
                select_exprs.append(pl.col(field_name).alias(p.output_field))
        
        proj = segs.select(select_exprs)
        state.records_tables[step.output] = proj

    # Not implemented yet
    # @_handle.register
    # async def _handle_filter(self, step: FilterOp, state: State) -> None:
    #     def ok(row: dict[str, Any], conds: dict[str, Any]) -> bool:
    #         for field, rule in conds.items():
    #             val = row.get(field)
    #             if isinstance(rule, dict):
    #                 if "eq" in rule and val != rule["eq"]:
    #                     return False
    #                 if "gte" in rule and not (val is not None and val >= rule["gte"]):
    #                     return False
    #                 if "lte" in rule and not (val is not None and val <= rule["lte"]):
    #                     return False
    #             else:
    #                 if val != rule:
    #                     return False
    #         return True

    #     src = state.records_tables.get(step.input, [])
    #     state.records_tables[step.output] = [r for r in src if ok(r, step.where)]

    @_handle.register
    async def _handle_join_temporal(self, step: JoinTemporalOp, state: State) -> None:
        REQUIRED_COLS = {"tdo_id", "start_s", "end_s"}

        def _ensure_cols(df: pl.DataFrame, alias: str) -> None:
            missing = REQUIRED_COLS - set(df.columns)
            if missing:
                raise InvalidPlanError(
                    f"JOIN_TEMPORAL: alias '{alias}' is missing required columns {sorted(missing)}"
                )

        left_df = state.segments_tables.get(step.left)
        if left_df is None:
            raise InvalidPlanError(
                f"JOIN_TEMPORAL left alias '{step.left}' not found in segments_tables"
            )
        right_df = state.segments_tables.get(step.right)
        if right_df is None:
            raise InvalidPlanError(
                f"JOIN_TEMPORAL right alias '{step.right}' not found in segments_tables"
            )

        _ensure_cols(left_df, step.left)
        _ensure_cols(right_df, step.right)

        # Temporal semi-join: keep only left rows that satisfy the relation with at least one right row
        matched_left = join_temporal(
            left=left_df,
            right=right_df,
            relation=step.relation,  # "BEFORE" | "AFTER" | "OVERLAPS" | "WITHIN"
            within_s=step.within_s,  # may be None
            tol=float(step.tolerance_s),  # default 0.0
            how="pairs",
        )

        # dedup exact duplicates on the core identity+time
        subset = [
            c
            for c in ("tdo_id", "start_s", "end_s", "signal", "channel", "label")
            if c in matched_left.columns
        ]
        if subset:
            matched_left = matched_left.unique(subset=subset)
        state.segments_tables[step.output] = matched_left

    @_handle.register
    async def _handle_merge(self, step: MergeOp, state: State) -> None:
        """Merge multiple segment tables, then dedupe or coalesce them."""
        dfs: list[SegmentsTable] = []
        for alias in step.inputs:
            try:
                dfs.append(state.segments_tables[alias])
            except KeyError:
                raise InvalidPlanError(
                    f"MERGE input alias '{alias}' not found in segments_tables"
                )
        if not dfs:
            raise InvalidPlanError("MERGE did not have any input data")

        merged: SegmentsTable = pl.concat(dfs, how="diagonal", rechunk=True)

        tol = step.tolerance_s if step.tolerance_s and step.tolerance_s > 0.0 else 0.0
        if step.coalesce:
            result: SegmentsTable = coalesce_segments(merged, tolerance_s=tol)
        else:
            # dedupe_segments handles its own key creation
            result: SegmentsTable = dedupe_segments(merged, tol=tol)

        state.segments_tables[step.output] = result

    async def _get_table_from_state(self, state: State, alias: str) -> Table:
        """Get a table (segments or records) from state by alias, including special tables.

        Args:
            state: The current execution state.
            alias: The alias of the table to retrieve.

        Returns:
            The requested table if found.

        Raises:
            InvalidPlanError: If the alias is not found.
        """
        # Try segments first, then records. Adjust to your State layout.
        if alias in state.segments_tables:
            return state.segments_tables[alias]
        if alias in state.records_tables:
            return state.records_tables[alias]
        # tdo metadata table?
        if alias == "_tdo_metadata":
            if state.tdo_table is None:
                tdos = await self.client.get_tdos(state.target, include_segments=False)
                state.tdo_table = new_tdo_table([tdo.to_dict() for tdo in tdos])
            return state.tdo_table
        # mention metadata table?
        if alias == "_mention_metadata":
            if state.mentions_table is None:
                # Explicitly fetch metadata since no segment operations have run yet
                match state.target:
                    case TargetByMention(mention_id=mid):
                        state.mentions_table = await self.client.get_mention_by_id(mid)
                    case TargetByWatchlist(watchlist_id=wid):
                        log.info("Fetching mentions metadata for watchlist %s", wid)
                        state.mentions_table = await self.client.get_mentions_by_watchlist(wid)
                        log.info("Fetched %d mentions for watchlist %s", len(state.mentions_table), wid)
                    case _:
                        state.mentions_table = new_mentions_table([])
            return state.mentions_table if state.mentions_table is not None else new_mentions_table([])
        if alias == "_watchlist_metadata":
            if state.watchlists_table is None:
                match state.target:
                    case TargetByWatchlist(watchlist_id=wid):
                        log.info("Fetching watchlist metadata for %s", wid)
                        state.watchlists_table = await self.client.get_watchlist_by_id(
                            wid
                        )
                        log.info("Fetched watchlist metadata for %s", wid)
                    case _:
                        state.watchlists_table = new_watchlists_table([])
            return state.watchlists_table
        raise InvalidPlanError(f"Unknown input alias '{alias}'")

    def _duration_expr(self) -> pl.Expr:
        """Duration expression helper."""
        return (pl.col("end_s") - pl.col("start_s")).cast(pl.Float64)

    def _compile_metric_expr(
        self, field: str | None, expr: str | None
    ) -> pl.Expr | None:
        """Compile a safe metric base expression.

        Supported:
        - field="score" → pl.col("score")
        - expr="duration()"  → end_s - start_s
        - expr="end_s - start_s" (alias)
        """
        if field:
            return pl.col(field)

        if expr:
            e = expr.strip().lower()
            if e == "duration()" or e == "end_s - start_s":
                return self._duration_expr()
            # (Optionally extend here with whitelisted cols / arithmetic.)
            raise ValueError(f"Unsupported expr: {expr!r}")

        # no field and no expr → allowed only for count()
        return None  # caller must handle this

    def _compile_metric_agg(self, name: str, spec: dict) -> pl.Expr:
        """Turn a single metric spec into a Polars aggregation expression with alias `name`.
        """
        fn = spec.get("fn")
        field = spec.get("field")
        expr = spec.get("expr")

        base = self._compile_metric_expr(field, expr)
        if fn == "count":
            return pl.count().alias(name)
        elif fn == "count_distinct":
            if base is None:
                raise InvalidPlanError(f"count_distinct for '{name}' needs field/expr")
            return base.n_unique().alias(name)
        elif fn == "sum":
            if base is None:
                raise InvalidPlanError(f"sum for '{name}' needs field/expr")
            return base.sum().alias(name)
        elif fn == "avg":
            if base is None:
                raise InvalidPlanError(f"avg for '{name}' needs field/expr")
            return base.mean().alias(name)
        elif fn == "min":
            if base is None:
                raise InvalidPlanError(f"min for '{name}' needs field/expr")
            return base.min().alias(name)
        elif fn == "max":
            if base is None:
                raise InvalidPlanError(f"max for '{name}' needs field/expr")
            return base.max().alias(name)

        raise InvalidPlanError(f"Unsupported fn '{fn}' for metric '{name}'")

    @_handle.register
    async def handle_aggregate(self, step: AggregateOp, state) -> None:
        df = await self._get_table_from_state(state, step.input)

        # Build aggregation expressions
        aggs = []
        for name, spec in step.metrics.items():
            aggs.append(self._compile_metric_agg(name, spec))

        if step.group_by:
            out = df.group_by(step.group_by).agg(aggs)
        else:
            out = df.select(aggs)
        state.segments_tables[step.output] = out

    async def _get_structured_table_data(
        self,
        step: OutputOp,
        state: State,
        alias: str,
        sort_spec: SortSpec | None = None,
        table: Table | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Get structured table data for output, with optional sorting and limiting.

        Args:
           step: The OutputOp step.
           state: The current State.
           alias: The alias of the table to get data for.
           sort_spec: Optional SortSpec to sort the table.
           table: Optional Table to use directly instead of looking up alias.
           limit: Optional limit on the number of rows to include, overrides step.limit.

        Returns:
           A dictionary containing structured table data.
        """
        # Check if table exists and not empty
        if table is None:
            try:
                table = await self._get_table_from_state(state, alias)
            except InvalidPlanError:
                return {
                    "alias": alias,
                    "status": "missing",
                    "data": None,
                    "shape": (0, 0),
                    "columns": [],
                }

        if table.is_empty():
            return {
                "alias": alias,
                "status": "empty",
                "data": None,
                "shape": (0, table.width),
                "columns": list(table.columns),
            }

        # Sort and limit the table
        limit = limit if limit is not None else step.limit
        processed_table = table
        original_height = table.height
        
        if sort_spec and sort_spec.field in table.columns:
            processed_table = processed_table.sort(
                sort_spec.field, descending=not sort_spec.ascending
            )

        # Apply row limit if specified and track truncation
        was_truncated = False
        if limit and limit > 0 and processed_table.height > limit:
            was_truncated = True
            processed_table = processed_table.head(limit)

        # Remove columns that are all null
        non_null_cols = [
            c
            for c in processed_table.columns
            if processed_table[c].null_count() < processed_table.height
        ]
        if non_null_cols:
            processed_table = processed_table.select(non_null_cols)

        return {
            "alias": alias,
            "status": "ok",
            "data": processed_table,
            "shape": (processed_table.height, processed_table.width),
            "columns": list(processed_table.columns),
            "original_height": original_height,
            "was_truncated": was_truncated,
            "truncation_info": f"Showing {processed_table.height} of {original_height} rows" if was_truncated else None,
        }

    async def _format_table(
        self,
        step: OutputOp,
        state: State,
        alias: str,
        sort_spec: SortSpec | None = None,
        table: Table | None = None,
        limit: int | None = None,
    ) -> str:
        """Format a table for output, with optional sorting and limiting.
        If table is provided, use it directly; otherwise look up alias in state.

        Args:
           step: The OutputOp step.
           state: The current State.
           alias: The alias of the table to format.
           sort_spec: Optional SortSpec to sort the table.
           table: Optional Table to use directly instead of looking up alias.
           limit: Optional limit on the number of rows to include, overrides step.limit.

        Returns:
           A string representation of the table.
        """
        # Get structured data and format it
        structured_data = await self._get_structured_table_data(
            step, state, alias, sort_spec, table
        )

        alias = structured_data["alias"]
        status = structured_data["status"]
        shape = structured_data["shape"]
        was_truncated = structured_data.get("was_truncated", False)
        truncation_info = structured_data.get("truncation_info")

        ret = f"{alias} ({shape[0]}, {shape[1]}) = \n"
        
        # Add truncation warning if data was limited
        if was_truncated and truncation_info:
            ret += f"⚠️  {truncation_info}\n"

        if status == "missing":
            return ret + "<missing>\n"
        elif status == "empty":
            return ret + "(empty)\n"

        table_data = structured_data["data"]
        body = format_table_delimited(
            table_data,
            delimiter="\t",
            text_preview=None,
            round_digits=4,
            add_footer=True,
            limit_rows=limit if limit is not None else step.limit,
        )
        return ret + body

    @_handle.register
    async def _handle_output(self, step: OutputOp, state: State) -> None:
        log.info("SEGMENTS TABLES:")
        for table in state.segments_tables.keys():
            log.info("\n%s", await self._format_table(step, state, table, limit=3))
        log.info("RECORDS TABLES:")
        for table in state.records_tables.keys():
            log.info("\n%s", await self._format_table(step, state, table, limit=3))

        # Return structured data instead of formatted strings
        structured_summary = []
        any_truncated = False
        for alias, sort_spec in step.summary_from:
            table_data = await self._get_structured_table_data(
                step, state, alias, sort_spec=sort_spec
            )
            structured_summary.append(table_data)
            if table_data.get("was_truncated", False):
                any_truncated = True

        state.answer = {
            "summary": structured_summary,
            "has_truncated_data": any_truncated,
        }
