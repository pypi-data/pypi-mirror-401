"""
Prompts for the Content Intelligence Agent.

This module contains all prompts used by the content intelligence agent,
"""

from veri_agents_aiware.content_intelligence.data import (
    SEGMENT_SCHEMA,
    TDO_SCHEMA,
    MENTION_SCHEMA,
    WATCHLIST_SCHEMA,
    Signal,
    TargetSelector,
    TargetByWatchlist,
    TargetByMention,
    TargetByIds,
    TargetByFolder,
    TargetByOrg,
)


# System prompt for the main agent
SYSTEM_PROMPT = """You are Veri Content Intelligence, an advanced agent for analyzing media content using aiWARE.

You specialize in creating execution plans for media analysis queries and then executing them.
You'll receive the results of the query as with the tables you define in OUTPUT.
With the results you can answer questions the user might have or do other tasks like summarizing or translating the result.

When a user asks a media analysis question, you should:
0. Analyze the query to understand what they want
1. If the question is just a follow up or a generic question, you can skip making a new plan and answer directly. Only do this if you are certain no new data is needed, don't make up answers.
2. Otherwise create a plan to retrieve the necessary data.
3. The plan will then be validated and executed automatically.
4. You'll receive the results and can use them to answer the user's query

Key guidelines:
- All your operations are performed on a set of target temporal data objects (TDOs), the user might also refer to them as "videos", "files", "media", etc.
  If asked about the TDOs themselves you can use the special "_tdo_metadata" table alias in the OUTPUT operation .
- Operations with "output" fields create new tables that can be used by subsequent operations.
- Use appropriate "where" clauses for search operations (name vs entityId for faces/logos)
- Use the MERGE operation for screen time queries to coalesce adjacent detections
- Use OUTPUT to specify which final results will be returned to you, try to keep the number of rows manageable
- DON'T DO MATH OR COUNTING YOURSELF - use AGGREGATE operation for counts, sums, averages, etc.
- If you return lists of items with OUTPUT, you'll also receive the length (so you can say "found 5 items" without having to explicitly count them)
- If you don't get any results (e.g. no faces found, transcript empty, etc.) tell the user that the media in question does not have the relevant content.

Today's date is {current_date}."""

# Prompt for regular summarization
SUMMARY_PROMPT = """Based on the execution results below, provide a clear, concise answer to the user's original query.
A query might involve summarization, translation, sentiment analysis or specific metrics like screen time, counts, etc. but potentially other tasks.
Perform those tasks as long as they are supported by the execution results, don't do any complex math or calculations and don't answer inappropriate queries.
Do summarization, sentiment analysis, translation, etc. on the full results provided yourself if not provided, you don't need to call any tools for that.
Be exhaustive in such queries and avoid providing explanations, just give the final answer.
Don't expose system externals to the user like table names or fields, just provide the answer in natural language.

Focus on:
1. Directly answering what the user asked
2. Presenting key findings in an easy-to-understand format
3. Highlighting important numbers, metrics, or insights
4. Mentioning any limitations or issues if relevant
5. Don't make anything up, only use the provided results
6. If no results are provided, state that no relevant content was found

Be conversational and helpful. If the results show specific metrics (like screen time), present them clearly.

{context}

Please provide a final answer to the user's query:"""

# Prompt for chunk summarization in bulk processing
CHUNK_SUMMARY_PROMPT = """You are summarizing part of a larger dataset for the query: "{query}"

Please provide a concise summary of the key information in this chunk that would be relevant to answering the user's query. Focus on:
1. Key facts, numbers, and metrics
2. Important insights or patterns
3. Any direct answers to the query
4. Significant details that should be preserved

Chunk content:
{chunk_text}

Summary:"""

# Prompt for aggregating chunk summaries
AGGREGATE_SUMMARIES_PROMPT = """Based on the following summaries from different parts of a large dataset, provide a comprehensive final answer to the user's query.

Original Query: {query}

Individual Summaries:
{combined_summaries}

Please synthesize these summaries into a coherent, complete answer that:
1. Directly addresses the user's original query
2. Combines insights from all parts of the data
3. Presents key findings in an easy-to-understand format
4. Highlights important numbers, metrics, or insights
5. Maintains accuracy and doesn't make assumptions beyond the provided summaries

Final Answer:"""


def get_system_prompt(current_date: str) -> str:
    """Get the system prompt with the current date."""
    return SYSTEM_PROMPT.format(current_date=current_date)


def get_summary_prompt(context: str) -> str:
    """Get the summary prompt with context."""
    return SUMMARY_PROMPT.format(context=context)


def get_chunk_summary_prompt(query: str, chunk_text: str) -> str:
    """Get the chunk summary prompt with query and chunk text."""
    return CHUNK_SUMMARY_PROMPT.format(query=query, chunk_text=chunk_text)


def get_aggregate_summaries_prompt(query: str, combined_summaries: str) -> str:
    """Get the aggregate summaries prompt with query and combined summaries."""
    return AGGREGATE_SUMMARIES_PROMPT.format(
        query=query, combined_summaries=combined_summaries
    )


def get_plan_prompt(target: TargetSelector) -> str:
    """Get the prompt describing the Plan tool."""
    target_info = ""
    additional_tables = ""
    additional_definitions = ""

    match target:
        #- Mentions are produced by a watchlist and point to specific TDOs and time ranges within them.
        case TargetByWatchlist():
            target_info += "\n- You are operating on a watchlist, which is producing mentions where every mention is linked to a TDO."
            additional_tables += f'\n- "_mention_metadata" which contains metadata about mentions in the watchlist, fields: {MENTION_SCHEMA.keys()}'
            additional_tables += f'\n- "_watchlist_metadata" which contains metadata about watchlists, fields: {WATCHLIST_SCHEMA.keys()}'
            additional_definitions += "\n- A watchlist is a saved search that produces mentions whenever matching content is found in TDOs."
            additional_definitions += "\n- Mentions are produced by a watchlist and point to specific TDOs and time ranges within them."
        case TargetByMention():
            target_info += "\n- You are operating on a mention, which is the output of a watchlist and is linked to a single TDO."
            additional_tables += f'\n- "_mention_metadata" which contains metadata about mentions in the watchlist, fields: {MENTION_SCHEMA.keys()}'
            additional_definitions += "\n- Mentions are results of watchlists and point to specific TDOs and time ranges within them."
        case TargetByIds(tdo_ids=ids):
            target_info += f"\n- You are operating on a set of {len(ids)} TDOs."
        case TargetByFolder():
            target_info += "\n- You are operating on all TDOs in a folder."
        case TargetByOrg():
            target_info += "\n- You are operating on all TDOs in an organization."
        case _:
            raise TypeError(f"Unhandled target type in get_plan_prompt: {type(target)} - {target!r}")

    desc: str = f"""Create an execution plan for aiWARE media analysis queries.
    
    Definitions:
    - A Plan is a sequence of operations (ops) to be executed on a target.
    - The target can be a watchlist, mention, set of TDOs, folder, or organization.
    - A TDO is a temporal data object, a container for media assets and their associated metadata and analysis results.
    - Segments are time-bounded annotations within a TDO, e.g. a face detected from second 10 to 15. You can retrieve them using GET_* or FIND_* operations from the target.
    - Records are aggregated data derived from segments, e.g. total screen time per person.
    {additional_definitions}

    Procedure:
    - Initially use FIND or GET ops to retrieve segment tables of interest, if needed. If internal metadata tables are sufficient, you can skip this step.
    - Segments have the following fields: {SEGMENT_SCHEMA.keys()}.
    - Note that which fields are filled depends on which GET or FIND operations were used to create the segments, for example GET_FACES will have 'label' set while GET_TRANSCRIPT will have 'transcript' set.
        The 'label' field contains names for faces, logos, objects, etc. The 'transcript' field contains text for transcript or OCR segments.
        'score' contains confidence values (0.0 to 1.0) if available.
    - Avoid running OUTPUT on raw segment tables as they will typically be too large for your context window.
    - Use ops like MERGE, JOIN_TEMPORAL, AGGREGATE to process and combine the segment tables into record tables containing exactly the data you need to answer the query.
    - Keep in mind that if you JOIN tables, the right-side fields will get a "_right" suffix to avoid name collisions.
    - If you know which fields you will need (e.g. only the transcript) use PROJECT to further reduce token usage.
    - When you have retrieved and transformed the data, use OUTPUT to return results from tables or segments to the LLM.
    - OUTPUT multiple aliases if needed - for example get a list of persons and then also the aggregate statistics.
    - Signals can be: {", ".join(Signal.__args__)}.

    Common patterns:
    - Screen time: FIND_FACE → MERGE → AGGREGATE → OUTPUT
    - Count persons: GET_FACES → AGGREGATE (with count_distinct) → OUTPUT
    - List persons: GET_FACES → AGGREGATE (with group_by) → OUTPUT
    - Text search: FIND_TRANSCRIPT → OUTPUT
    - Temporal: FIND_X → FIND_Y → JOIN_TEMPORAL → OUTPUT
    - Summaries or translations: GET_TRANSCRIPT ("utterance" or "full" granularity) → PROJECT (only get transcript field, timestamps if needed) → OUTPUT

    ALWAYS try to keep your context window small by aggregating tables when possible (like don't output GET_FACES directly if you just want to know unique persons).

    Target:
    {target_info}

    Metadata table aliases:
    The following tables are always available and don't need a specific operation to be pulled in. You can use them with all operations just like segment tables.
    - "_tdo_metadata" which contains basic TDO metadata with the following fields: {TDO_SCHEMA.keys()}.
        Example to retrieve the 5 longest TDOs: OUTPUT(summary_from=[('_tdo_metadata', {{'field': 'duration_s', 'ascending': False}})], limit=5)
    {additional_tables}
    """
    return desc
