import logging
from datetime import datetime
from typing import Annotated, Any, Optional, Sequence, TypedDict, cast

from aiware.client import AsyncAiware
from langgraph.prebuilt import ToolNode
from langchain.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.messages.utils import count_tokens_approximately
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph
from langgraph.runtime import Runtime
from langgraph.store.base import BaseStore
from langgraph.types import Checkpointer
from pydantic import BaseModel, Field, TypeAdapter
from veri_agents_aiware.aiware_client.async_client import AsyncAgentsAiware
from veri_agents_aiware.content_intelligence.client import ContentIntelligenceClient
from veri_agents_aiware.content_intelligence.data import (
    TargetSelector,
    TargetByOrg,
    TargetByIds,
    TargetByFolder,
    TargetByWatchlist,
    TargetByMention,
    format_table_delimited,
)
from veri_agents_aiware.content_intelligence.executor import Executor
from veri_agents_aiware.content_intelligence.executor import State as ExecutorState
from veri_agents_aiware.content_intelligence.plan import (
    CreatePlanTool,
    InvalidPlanError,
    Plan,
)
from veri_agents_aiware.content_intelligence.prompts import (
    get_aggregate_summaries_prompt,
    get_chunk_summary_prompt,
    get_summary_prompt,
    get_system_prompt,
)

log = logging.getLogger(__name__)


class AgentState(TypedDict):
    messages: Annotated[Sequence[AnyMessage], add_messages]
    query: str | None
    plan: Plan | None
    plan_validation_errors: list[str] | None
    plan_generation_attempts: int | None
    executor_result: dict[str, Any] | None
    plan_execution_errors: list[str] | None
    plan_execution_attempts: int | None
    # For bulk processing
    context_chunks: list[str] | None
    chunk_summaries: list[str] | None
    current_chunk: str | None  # For individual chunk processing
    chunk_index: int | None  # For tracking chunk order


def format_structured_table_for_context(table_data: dict) -> str:
    """Format structured table data for LLM context."""
    alias = table_data.get("alias", "unknown")
    status = table_data.get("status", "unknown")
    shape = table_data.get("shape", (0, 0))
    was_truncated = table_data.get("was_truncated", False)
    truncation_info = table_data.get("truncation_info")

    if status == "missing":
        return f"{alias}: Table not found"
    elif status == "empty":
        return f"{alias}: Table is empty"
    elif status != "ok":
        return f"{alias}: Table status: {status}"

    # Get the actual polars DataFrame
    df = table_data.get("data")
    if df is None:
        return f"{alias}: No data available"

    formatted_table = format_table_delimited(
        df,
        delimiter="\t",
        text_preview=None,
        round_digits=4,
        add_footer=True,
        limit_rows=10000,  # Large limit for now, we'll handle chunking separately
    )

    # Build the result with truncation warning if applicable
    header = f"{alias} ({shape[0]} rows, {shape[1]} cols)"
    if was_truncated and truncation_info:
        header += f" - ⚠️ DATA TRUNCATED: {truncation_info}"

    return f"{header}:\n{formatted_table}"


def chunk_text_tables(
    formatted_tables: list[str], max_tokens_per_chunk: int = 50000
) -> list[str]:
    """
    Split pre-formatted table strings into manageable chunks for bulk processing.

    Args:
        formatted_tables: List of already formatted table strings
        max_tokens_per_chunk: Maximum tokens per chunk

    Returns:
        List of text chunks, each containing one or more tables
    """
    chunks = []
    current_chunk = ""
    current_tokens = 0
    fitting_tables = []

    # first we have to split tables that are by itself too long already
    for i, table_text in enumerate(formatted_tables):
        table_tokens = count_tokens_approximately([table_text])
        if table_tokens > max_tokens_per_chunk:
            log.warning(
                f"[Executor] Single table {i} exceeds max tokens per chunk ({table_tokens} > {max_tokens_per_chunk}), splitting it individually."
            )
            # Split this table into smaller parts by lines
            lines = table_text.splitlines()
            header = lines[0] if lines else ""
            part = header + "\n"
            part_tokens = count_tokens_approximately([part])
            for line in lines[1:]:
                line_tokens = count_tokens_approximately([line + "\n"])
                if part_tokens + line_tokens > max_tokens_per_chunk and part:
                    chunks.append(part.strip())
                    part = header + "\n"  # start new part with header
                    part += line + "\n"
                    part_tokens = count_tokens_approximately([part])
                else:
                    part += line + "\n"
                    part_tokens += line_tokens
            if part:
                chunks.append(part.strip())
        else:
            # Keep the table as is for normal processing
            fitting_tables.append(table_text)

    # process the remaining tables that fit, perhaps we can squeeze two or more into one chunk
    for table_text in fitting_tables:
        table_tokens = count_tokens_approximately([table_text])

        # If adding this table would exceed the limit, save current chunk and start new one
        if current_tokens + table_tokens > max_tokens_per_chunk and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = table_text
            current_tokens = table_tokens
        else:
            # Add table to current chunk
            if current_chunk:
                current_chunk += "\n\n" + table_text
            else:
                current_chunk = table_text
            current_tokens += table_tokens

    # Add the last chunk if it has content
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


class ContentIntelligenceInput(BaseModel):
    """Input schema for the content intelligence agent

    Can be passed through the runtime context to override the default target.

    Example:
    ```
    graph.invoke(
        {"messages": [HumanMessage("What's the screen time for John?")]},
        context={
            "target": {"kind": "tdo_ids", "tdo_ids": ["tdo1", "tdo2"]}}
        }
    )
    ```
    """

    target: TargetSelector | None = Field(
        description="Selector for target media (by folder or list of TDO IDs)"
    )


def create_content_intelligence_agent(
    model: BaseChatModel,
    aiware_client: AsyncAiware,
    target: TargetSelector | None = None,
    model_summary: BaseChatModel | None = None,
    model_bulk: BaseChatModel | None = None,
    checkpointer: Checkpointer | None = None,
    store: BaseStore | None = None,
    interrupt_before: list[str] | None = None,
    interrupt_after: list[str] | None = None,
    debug: bool = False,
    name: str | None = None,
    max_tokens_per_request: int = 80000,
    **kwargs,
) -> CompiledStateGraph[AgentState, ContentIntelligenceInput, AgentState, AgentState]:
    """Create a content intelligence agent workflow for media analysis queries.

    The agent uses an LLM to create an execution plan, executes it against aiWARE, and summarizes the results.

    Args:
        model: Language model to use for planning and summarization.
        aiware_client: Initialized AsyncAgentsAiware client for aiWARE access.
        target: TargetSelector defining the media to analyze, either pass in here or through runtime context.
        model_summary: Optional language model for summarization tasks.
        model_bulk: Optional language model for bulk operations on large contexts (>100k tokens).
                   If not provided, the main model will be used for all operations.
        checkpointer: Optional checkpointer for workflow state.
        store: Optional store for persisting workflow state.
        interrupt_before: Optional list of node names to interrupt before execution.
        interrupt_after: Optional list of node names to interrupt after execution.
        debug: Whether to enable debug mode.
        name: Optional name for the workflow.

    Returns:
        CompiledStateGraph: The compiled workflow LangGraph graph.
    """
    aiware_client = AsyncAgentsAiware.extend_async(aiware_client)
    if model_summary is None:
        model_summary = model
    if model_bulk is None:
        model_bulk = model_summary

    def _get_target(runtime: Runtime[ContentIntelligenceInput]) -> TargetSelector:
        """Helper to get the current target from runtime or default."""
        local_target = (
            runtime.context.target
            if (runtime.context and runtime.context.target)
            else target
        )
        if not local_target:
            raise ValueError("No target specified for content intelligence agent.")
        if isinstance(local_target, dict):
            local_target = TypeAdapter(TargetSelector).validate_python(local_target)
        if not isinstance(local_target, (TargetByOrg, TargetByIds, TargetByFolder, TargetByWatchlist, TargetByMention)):
            raise ValueError(f"Invalid target type: {type(local_target)}. Expected a TargetSelector.")
        return local_target

    async def prepare_plan(
        state: AgentState, runtime: Runtime[ContentIntelligenceInput]
    ):
        """Use LLM with tools to create an execution plan."""
        messages = state["messages"]

        # Extract the query from the last human message
        query: Optional[str] = None
        for msg in reversed(messages):
            if hasattr(msg, "type") and msg.type == "human":
                content = msg.content
                if isinstance(content, str):
                    query = content
                    break

        if not query:
            query = state.get("query") or ""

        log.info(f"Preparing plan for query: {query}")

        try:
            current_target = _get_target(runtime)
            plan_tool = CreatePlanTool.build(target=current_target)
            tools = [plan_tool]

            # Bind tools to model
            model_with_tools = model.bind_tools(tools)

            # Add system prompt if not already present
            system_present = any(
                hasattr(msg, "type") and msg.type == "system" for msg in messages
            )
            if not system_present:
                messages_with_system = [
                    SystemMessage(content=get_system_prompt(str(datetime.now().date())))
                ] + list(messages)
            else:
                messages_with_system = list(messages)

            # LLM will decide if we shall prepare a plan, this is not always required if it can answer directly
            response = await model_with_tools.ainvoke(messages_with_system)

            # when preparing a new plan, we want a new clean state
            return {
                "messages": [response],
                "query": query,
                "plan": None,
                "plan_validation_errors": None,
                "plan_generation_attempts": (
                    state.get("plan_generation_attempts") or 0
                ),
                "plan_execution_attempts": 0,
                "plan_execution_errors": None,
                "executor_result": None,
                "context_chunks": None,
                "chunk_summaries": None,
                "current_chunk": None,
                "chunk_index": None,
            }

        except Exception as e:
            log.error(f"Failed to prepare plan: {e}")
            # TODO: this is an issue calling the LLM, we might want to bubble this up instead
            return {
                "query": query,
                "plan": None,
                "plan_validation_errors": [str(e)],
            }

    async def call_tools(state: AgentState, runtime: Runtime[ContentIntelligenceInput]):
        """Custom tool calling node that dynamically creates tools with current target."""
        current_target = _get_target(runtime)
        plan_tool = CreatePlanTool.build(target=current_target)
        tool_node = ToolNode([plan_tool])
        response = tool_node.invoke(state)
        return response

    async def should_call_tools(state: AgentState) -> str:
        """Decide if we should call tools or answer without making a plan."""
        messages = state["messages"]

        # Check if the last message has tool calls
        if messages:
            last_msg = messages[-1]
            if hasattr(last_msg, "tool_calls") and getattr(
                last_msg, "tool_calls", None
            ):
                return "tools"

        return "done"

    async def process_plan(state: AgentState):
        """Process the tool call results to extract and validate the plan."""
        messages = state["messages"]

        # Increment attempt counter at the start so should_replan sees the updated count
        current_generation_attempts = (state.get("plan_generation_attempts") or 0) + 1

        # Find the last tool message and pull out the plan, validate it
        plan = None
        validation_errors = []
        for msg in reversed(messages):
            if hasattr(msg, "type") and msg.type == "tool":
                try:
                    tool_msg = cast(ToolMessage, msg)
                    if tool_msg.artifact and tool_msg.artifact.get("success"):
                        plan = Plan.model_validate(tool_msg.artifact.get("plan"))
                        log.info(
                            f"Plan extracted from tool result: {len(plan.steps)} steps"
                        )
                        break
                    else:
                        validation_errors.append(
                            f"Tool failed: {tool_msg.artifact.get('error')}"
                        )
                except Exception as e:
                    validation_errors.append(f"Failed to parse tool result: {str(e)}")

        if plan is None and not validation_errors:
            validation_errors.append("No plan was created by the LLM")

        return {
            "plan": plan,
            "plan_generation_attempts": current_generation_attempts,
            "plan_validation_errors": validation_errors,
        }

    async def should_replan(state: AgentState) -> str:
        """Decide if we should replan, or end based on validation results."""
        plan = state.get("plan")
        plan_errors = state.get("plan_validation_errors", [])
        execution_errors = state.get("plan_execution_errors", [])
        num_plan_attempts = state.get("plan_generation_attempts") or 0
        num_execution_attempts = state.get("plan_execution_attempts") or 0

        # if we have an invalid plan, we replan, otherwise execute
        # we retry execution up to 2 times, if that fails we try a new plan
        # if we fail the whole process 3 times, we end
        if plan and not plan_errors and not execution_errors:
            return "continue"
        if num_execution_attempts >= 2:
            return "replan"
        if num_plan_attempts >= 3:
            return "end"
        if plan_errors:
            return "replan"
        if execution_errors:
            return "rerun"
        else:
            return "replan"

    async def execute_plan(
        state: AgentState, runtime: Runtime[ContentIntelligenceInput]
    ):
        """Execute the validated plan using the Executor."""
        state_target = _get_target(runtime)
        plan = cast(Plan, state.get("plan"))  # has to be non-None as per should_replan
        query = state.get("query") or ""

        # Increment attempt counter at the start so should_replan sees the updated count
        current_attempts = (state.get("plan_execution_attempts") or 0) + 1

        try:
            log.info(f"[Agent] Executing plan with {len(plan.steps)} steps")
            executor_state = ExecutorState(target=state_target, query=query, plan=plan)
            ci_client = ContentIntelligenceClient(aiware_client)
            executor = Executor(client=ci_client)
            result_state = await executor.run(executor_state)
            executor_result = result_state.answer

            # Convert DataFrames to serializable format
            if executor_result and "summary" in executor_result:
                log.info("[Agent] Plan execution completed successfully")
                # Convert structured data to text format for agent state
                summary_data = executor_result["summary"]
                formatted_tables = []
                for table_data in summary_data:
                    formatted_table = format_structured_table_for_context(table_data)
                    formatted_tables.append(formatted_table)

                # Store formatted text instead of DataFrames
                serializable_result = {
                    "summary_text": formatted_tables,
                }

                return {
                    "plan_execution_errors": None,
                    "plan_validation_errors": None,
                    "executor_result": serializable_result,
                    "plan_execution_attempts": current_attempts,
                }

            error_msg = "Plan execution failed: No execution results"
            log.error(error_msg)
            return {
                "plan_execution_errors": [error_msg],
                "plan_execution_attempts": current_attempts,
            }
        except InvalidPlanError as ipe:
            error_msg = f"Plan execution failed due to invalid plan: {str(ipe)}"
            log.error(error_msg)
            return {
                "plan_validation_errors": [error_msg],
                "plan_execution_attempts": current_attempts,
            }
        except Exception as e:
            error_msg = f"Plan execution failed: {str(e)}"
            log.error(error_msg)
            return {
                "plan_execution_errors": [error_msg],
                "plan_execution_attempts": current_attempts,
            }

    async def summarize(state: AgentState):
        """Use LLM to generate a final answer based on execution results."""
        query = state.get("query", "") or ""
        executor_result = state.get("executor_result")

        if not executor_result:
            error_msg = "Cannot summarize: No execution results available"
            log.error(error_msg)
            return {
                "messages": [AIMessage(content=error_msg)],
            }

        try:
            # Prepare context for the LLM
            context_parts = []
            context_parts.append(f"Original Query: {query}")

            # Get formatted table text from executor
            summary_tables = executor_result.get("summary_text", [])

            if not summary_tables:
                context_parts.append("Raw Results: No results found")
            else:
                context_parts.append("Raw Results:\n" + "\n\n".join(summary_tables))

                # Check if we need bulk processing based on total context size
                full_context = "\n\n".join(context_parts)
                total_tokens = count_tokens_approximately([full_context])

                if total_tokens > max_tokens_per_request:
                    log.info(
                        f"[Agent] Context has {total_tokens} tokens, using text-based bulk processing"
                    )

                    # Use text-based chunking for already formatted tables
                    chunks = chunk_text_tables(
                        summary_tables, max_tokens_per_chunk=max_tokens_per_request
                    )

                    # Add query context to each chunk
                    query_context = f"Original Query: {query}\n\n"
                    chunks_with_context = [query_context + chunk for chunk in chunks]

                    return {
                        "context_chunks": chunks_with_context,
                    }

            # For smaller contexts or no results, use regular model to give an answer
            context = "\n\n".join(context_parts)
            return await _regular_summarize(context, query, model_summary)

        except Exception as e:
            error_msg = f"Summary generation failed: {str(e)}"
            log.error(error_msg)
            fallback_content = (
                "Summary generation failed. Please check the execution results."
            )
            return {
                "messages": [AIMessage(content=fallback_content)],
            }

    async def _regular_summarize(
        context: str, query: str, llm_model: BaseChatModel
    ):
        """Regular summarization for smaller contexts."""
        summary_prompt = get_summary_prompt(context)
        log.info("[Agent] Summarizing")
        response = await llm_model.ainvoke([HumanMessage(content=summary_prompt)])
        log.info("[Agent] Summary generated successfully")
        return {
            "messages": [response],
        }

    async def _bulk_summarize_chunk(chunk: str, query: str) -> str:
        """Summarize a single chunk using the bulk model."""
        if not chunk:
            return "No content to summarize"
        try:
            chunk_prompt = get_chunk_summary_prompt(query, chunk)
            response = await model_bulk.ainvoke([HumanMessage(content=chunk_prompt)])
            if hasattr(response, "content"):
                summary = getattr(response, "content")
            else:
                summary = str(response)
            log.info(f"[Agent] Generated chunk summary of length: {len(summary)}")
            return summary
        except Exception as e:
            log.error(f"[Agent] Chunk summarization failed: {e}")
            return f"Error summarizing chunk: {str(e)}"

    async def should_use_bulk_processing(state: AgentState) -> str:
        """Decide whether to use bulk processing or regular summarization."""
        context_chunks = state.get("context_chunks")

        log.info(
            "[Agent] Deciding on bulk processing, we got %d chunks",
            len(context_chunks) if context_chunks else 0,
        )
        if context_chunks:
            return "bulk"
        else:
            return "regular"

    async def route_chunks_for_processing(state: AgentState):
        """Route chunks to bulk processing by processing them sequentially."""
        chunks = state.get("context_chunks", [])
        query = state.get("query", "")

        if not chunks:
            return {"chunk_summaries": []}
        # Process chunks sequentially for now (TODO: can be parallelized later)
        summaries = []
        for i, chunk in enumerate(chunks):
            try:
                result = await _bulk_summarize_chunk(chunk, query or "")
                summaries.append(result)
                log.info(f"[Agent] Processed chunk {i + 1}/{len(chunks)}")
            except Exception as e:
                log.error(f"[Agent] Failed to process chunk {i}: {e}")
                summaries.append(f"Error processing chunk: {str(e)}")
        log.info(f"[Agent] Completed bulk processing of {len(chunks)} chunks")
        return {"chunk_summaries": summaries}

    async def aggregate_summaries(state: AgentState):
        """Aggregate chunk summaries using the main model."""
        query = state.get("query", "")
        chunk_summaries = state.get("chunk_summaries", [])

        if not chunk_summaries:
            error_msg = "Cannot aggregate: No chunk summaries available"
            log.error(error_msg)
            return {
                "messages": [AIMessage(content=error_msg)],
            }

        try:
            # Combine all chunk summaries
            combined_summaries = "\n\n".join(
                [
                    f"Summary {i + 1}:\n{summary}"
                    for i, summary in enumerate(chunk_summaries)
                ]
            )

            aggregate_prompt = get_aggregate_summaries_prompt(
                query or "", combined_summaries
            )
            response = await model_summary.ainvoke(
                [HumanMessage(content=aggregate_prompt)]
            )

            log.info("[Agent] Successfully aggregated chunk summaries")
            return {
                "messages": [response],
            }

        except Exception as e:
            error_msg = f"Summary aggregation failed: {str(e)}"
            log.error(error_msg)
            return {
                "messages": [AIMessage(content=error_msg)],
            }

    # Workflow setup
    workflow = StateGraph(
        state_schema=AgentState, context_schema=ContentIntelligenceInput
    )
    workflow.add_node("prepare_plan", prepare_plan)
    workflow.add_node("tools", call_tools)
    workflow.add_node("process_plan", process_plan)
    workflow.add_node("execute_plan", execute_plan)
    workflow.add_node("summarize", summarize)
    workflow.add_node("route_chunks", route_chunks_for_processing)
    workflow.add_node("aggregate_summaries", aggregate_summaries)

    # prepare plan through a tool call to the create plan tool
    workflow.add_edge(START, "prepare_plan")
    workflow.add_conditional_edges(
        "prepare_plan",
        should_call_tools,
        {
            "tools": "tools",
            "done": END,
        },
    )

    # Process the generated plan and verify if it can be executed
    workflow.add_edge("tools", "process_plan")

    # After verification, decide if we need to re-plan or execute
    workflow.add_conditional_edges(
        "process_plan",
        should_replan,
        {
            "continue": "execute_plan",
            "rerun": "execute_plan",
            "replan": "prepare_plan",
            "end": END,
        },
    )

    # After execution, we again check if the plan was invalid or execution failed
    workflow.add_conditional_edges(
        "execute_plan",
        should_replan,
        {
            "continue": "summarize",
            "rerun": "execute_plan",
            "replan": "prepare_plan",
            "end": END,
        },
    )

    # From summarize, check if we need bulk processing or if we're done
    workflow.add_conditional_edges(
        "summarize",
        should_use_bulk_processing,
        {
            "bulk": "route_chunks",
            "regular": END,
        },
    )

    # Process chunks and aggregate results
    workflow.add_edge("route_chunks", "aggregate_summaries")
    workflow.add_edge("aggregate_summaries", END)
    return workflow.compile(
        checkpointer=checkpointer,
        store=store,
        interrupt_before=interrupt_before,
        interrupt_after=interrupt_after,
        debug=debug,
        name=name,
    )
