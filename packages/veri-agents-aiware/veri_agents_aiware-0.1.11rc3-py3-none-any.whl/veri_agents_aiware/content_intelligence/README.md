# Content Intelligence Toolkit

The Content Intelligence Toolkit is a sophisticated LangGraph-based agent system that uses Large Language Models (LLMs) to create and execute plans for analyzing media content using the aiWARE platform. It provides a declarative approach to media analysis through structured execution plans.

## Overview

The system follows a **Plan → Execute → Summarize** pattern:

1. **Plan Creation**: An LLM analyzes the user's query and creates a structured execution plan using available operations
2. **Plan Execution**: The executor deterministically runs each operation in the plan, processing media data
3. **Result Summarization**: The LLM receives the execution results and provides a natural language response

## Usage

The Content Intelligence Agent requires an aiWARE client and LLMs for planning, bulk processing, and summarization.
LLMs can be passed in as LangChain BaseChatModels, which includes the LLMGateway model from this package.

Example API use:
```
    from aiware.common.auth import TokenAuth, AiwareApiKey
    from veri_agents_aiware.aiware_client.async_client import AsyncAgentsAiware
    from veri_agents_aiware.content_intelligence import create_content_intelligence_agent, TargetSelector

    from langchain_aws import ChatBedrockConverse

    # Setup aiWARE client using an aiWARE API key
    aiware_client = AsyncAgentsAiware(
        base_url=aiware_url,
        auth=TokenAuth(token=AiwareApiKey(aiware_token)),
    )

    # LLM used for planning, making decisions, tool calling
    llm = ChatBedrockConverse(
        model="arn:aws:bedrock:us-east-1:075494626733:application-inference-profile/nqd9c00141tr",
        base_model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        provider="anthropic",
        region_name="us-east-1",
    )
    # Bulk LLM used for large scale operations (e.g. summarization of transcripts)
    bulk_llm = ChatBedrockConverse(
        model="arn:aws:bedrock:us-east-1:075494626733:application-inference-profile/kl8qab6pdp97",
        base_model="us.amazon.nova-micro-v1:0",
        provider="amazon",
        region_name="us-east-1",
    )
    # LLM used to generate the final answer
    summary_llm = ChatBedrockConverse(
        max_tokens=2000,
        model="arn:aws:bedrock:us-east-1:075494626733:application-inference-profile/nhxrhd3b0en8",
        base_model="us.amazon.nova-2-lite-v1:0",
        provider="amazon",
        region_name="us-east-1",
    )

   # Default target
   target = TargetByIds(kind="tdo_ids", tdo_ids=tdo_ids)

   # Create the agent, can be done per query or once and reused
   content_agent = create_content_intelligence_agent(
      model=llm,
      summary_model=summary_llm,
      bulk_model=bulk_llm,
      aiware_client=aiware_client,
      target=target,
   )

   # Execute a query, can override target in context if desired
   result = await content_agent.ainvoke(
      {"messages": ["What's the screen time for John Doe?"]},
      context={
          "target": {"kind": "tdo_ids", "tdo_ids": ["tdo1", "tdo2"]}  # Override default target
      }
   )
```

## Evaluation

eval.py provides an evaluation framework for the Content Intelligence Agent using Langfuse and OpenEvals.

Requires the dev dependencies for veri_agents_aiware:
    `uv sync --all-groups`

Then run
    `uv run python -m veri_agents_aiware.content_intelligence.eval` 

Requires the following environment variables to be set:
   VERITONE_AIWARE_API_KEY - aiWARE API key
   VERITONE_AIWARE_BASE_URL - aiWARE base URL
   LANGFUSE_PUBLIC_KEY - Langfuse public key
   LANGFUSE_SECRET_KEY - Langfuse secret key
   LANGFUSE_URL - (optional) Langfuse base URL, defaults to https://langfuse.varp.tech

Also the IAM profile used must have access to Bedrock LLMs.


## Core Components

### 1. Plan (`plan.py`)

The planning system uses LLM tool calls to generate structured execution plans. Plans consist of a sequence of operations (ops) that will be executed against a target.

**Key Features:**
- `Plan` model: Contains a list of operations with version tracking and signatures
- `CreatePlanTool`: LangChain tool that uses LLM to generate plans based on user queries
- Plan validation and error handling for invalid operation sequences

### 2. Operations (`ops.py`)

Operations define the atomic actions that can be performed on media content. They fall into several categories:

#### Data Retrieval Operations
- **FIND_TRANSCRIPT**: Search for specific text within transcripts using keyword queries
- **FIND_FACE**: Find specific faces/persons by entity ID or name
- **FIND_LOGO**: Find specific logos/brands by entity ID or name
- **GET_TRANSCRIPTS**: Retrieve all speech transcripts for target media
- **GET_FACES**: Get all face occurrences in target media
- **GET_LOGOS**: Get all logo occurrences in target media
- **GET_OCRS**: Get all OCR text occurrences in target media

#### Data Processing Operations
- **PROJECT**: Select and transform specific fields from segments into records
- **AGGREGATE**: Perform grouping, counting, summing operations (e.g., screen time calculations)
- **FILTER**: Apply conditions to filter segments or records
- **MERGE**: Coalesce adjacent or overlapping segments (crucial for screen time analysis)
- **JOIN_TEMPORAL**: Join segments from different signals based on temporal relationships
- **OUTPUT**: Define which results are returned to the LLM for final processing

#### Time Constraints
Operations support both relative (`MediaTime`) and absolute (`AbsTime`) time filtering:
- `MediaTime`: Relative to media timeline (e.g., seconds 10-30 of a video)
- `AbsTime`: Wall-clock time constraints for selecting which media to analyze

### 3. Data Schemas (`data.py`)

The system operates on strongly-typed Polars DataFrames with predefined schemas:

#### Core Data Types
- **SegmentsTable**: Time-bounded annotations within media (e.g., face detection from 10-15 seconds)
- **RecordsTable**: Aggregated data derived from segments (e.g., total screen time per person)
- **TdoTable**: Metadata about Temporal Data Objects (media files)
- **MentionsTable**: Metadata about Mentions (parts of TDOs)
- **WatchlistsTable**: Metadata about watchlists (saved searched producing mentions)

#### Segment Schema
```python
SEGMENT_SCHEMA = {
    "tdo_id": pl.Utf8,           # Media file identifier
    "start_s": pl.Float64,       # Start time in seconds
    "end_s": pl.Float64,         # End time in seconds
    "channel": pl.Utf8,          # audio/video/image/text
    "signal": pl.Utf8,           # transcript/face/logo/object/etc.
    "transcript": pl.Utf8,       # Speech transcript text
    "score": pl.Float64,         # Confidence score (0.0-1.0)
    "label": pl.Utf8,            # Content for faces, logos, objects etc.
    "engine_id": pl.Utf8,        # Processing engine used
    "engine_name": pl.Utf8,      # Engine display name
    "abs_start_epoch_s": pl.Float64,  # Wall-clock start time
    "abs_end_epoch_s": pl.Float64,    # Wall-clock end time
    "bbox_json": pl.Utf8,        # Bounding box coordinates (JSON)
    "poly_json": pl.Utf8,        # Polygon coordinates (JSON)
    "meta_json": pl.Utf8,        # Additional metadata (JSON)
}
```

#### Target Selectors
Define what media content to analyze:
- `TargetByOrg`: All media in an organization
- `TargetByIds`: Specific media files by ID
- `TargetByFolder`: All media in a folder
- `TargetByWatchlist`: Media associated with a watchlist
- `TargetByMention`: Media associated with a specific mention

### 4. Executor (`executor.py`)

The executor provides deterministic execution of plans using single-dispatch pattern:

**Key Features:**
- `State` model: Tracks execution state including query, target, tables, and results
- Single-dispatch handlers for each operation type
- Error collection and reporting

**Execution Flow:**
1. Initialize state with query and target
2. Iterate through plan steps
3. Dispatch each step to appropriate handler
4. Accumulate results in state tables
5. Return final state with all results

### 5. Client (`client.py`)

The client handles all interactions with the aiWARE platform:

**Key Responsibilities:**
- **Data Retrieval**: Fetch media content and analysis results from aiWARE
- **Search Operations**: Execute complex queries against media indexes
- **Result Conversion**: Transform aiWARE responses into standardized segment format
- **Caching**: Optimize performance with intelligent caching strategies

**Key Features:**
- Async operations for performance
- Support for both search-based and direct TDO access
- Conversion utilities for different aiWARE result formats
- Handling of cognitive engine results from mentions

### 6. LangGraph Agent (`agent.py`)

The LangGraph agent orchestrates the entire content intelligence workflow using a state machine approach. It coordinates between all the other components to provide a seamless experience from query to answer.

#### Agent Architecture

The agent is built using LangGraph's `StateGraph` and follows a multi-node workflow pattern with built-in retry mechanisms:

```
START → prepare_plan → tools → process_plan → execute_plan → summarize → END
          ↓     ↑        ↓         ↓              ↓             ↓
        done    └─ replan ←─ replan ←───── rerun ──┘       bulk_processing
                              ↓                               ↓
                             end                     route_chunks → aggregate_summaries
```

#### Key Components

**AgentState**: Tracks the complete workflow state including:
- `messages`: Conversation history with the LLM
- `query`: User's original question
- `plan`: Generated execution plan
- `executor_result`: Results from plan execution
- `plan_generation_attempts`: Counter for retry mechanism
- `plan_execution_attempts`: Counter for execution retries
- `plan_validation_errors`: List of validation errors
- `plan_execution_errors`: List of execution errors
- `context_chunks`: For handling large result sets
- `chunk_summaries`: Intermediate summaries for bulk processing

**ContentIntelligenceInput**: Runtime context containing:
- `target`: Target selector defining what media to analyze

#### Workflow Nodes

1. **prepare_plan**: 
   - Extracts query from user message
   - Adds system prompt with domain context
   - Calls LLM with `CreatePlanTool` to generate execution plan
   - Resets state for clean re-planning attempts

2. **tools** (ToolNode):
   - Executes the `CreatePlanTool` when LLM makes tool calls
   - Validates plan structure and operations
   - Returns structured plan or validation errors

3. **process_plan**:
   - Extracts generated plan from tool call results
   - Converts raw tool output to validated `Plan` object
   - Increments plan generation attempt counter
   - Handles plan parsing errors gracefully

4. **execute_plan**:
   - Creates `ExecutorState` with query, target, and plan
   - Instantiates `ContentIntelligenceClient` and `Executor`
   - Runs plan execution and collects results
   - Increments execution attempt counter
   - Converts DataFrames to serializable format for LLM processing

5. **summarize**:
   - Formats execution results for LLM context
   - Handles both regular and bulk processing scenarios
   - Generates final natural language response or prepares for bulk processing

#### Advanced Features

**Retry Mechanism**: Robust error handling with intelligent retry logic:
- **Execution Retries**: Up to 2 attempts to execute the same plan if execution fails
- **Plan Re-generation**: Up to 3 total plan generation attempts if validation fails
- **Graceful Termination**: Ends workflow after maximum attempts to prevent infinite loops
- **Error Differentiation**: Separate handling for validation vs. execution errors

**Bulk Processing**: For large result sets that exceed token limits:
- **route_chunks**: Splits large results into manageable chunks and processes sequentially
- **aggregate_summaries**: Combines chunk summaries into final answer using main model

**Error Handling & Recovery**:
- Plan validation failures trigger re-planning (with attempt tracking)
- Execution errors are captured and can trigger re-execution or re-planning
- Graceful fallbacks for missing data or API failures
- Clear error reporting when maximum attempts are reached

**Context Management**:
- Token-aware chunking prevents context overflow
- Intelligent table formatting with truncation warnings
- Separate models for planning vs. bulk processing

#### Decision Points

The agent uses conditional edges to route workflow based on state:

- **should_call_tools**: Determines if LLM made tool calls or provided direct answer
- **should_replan**: Complex decision logic that considers:
  - Plan validity and execution success
  - Number of plan generation attempts (max 3)
  - Number of execution attempts (max 2 per plan)
  - Type of errors encountered (validation vs. execution)
  - Returns: `continue`, `rerun`, `replan`, or `end`
- **should_use_bulk_processing**: Routes to bulk processing for large results

#### Usage Example

```python
# Create the agent
agent = create_content_intelligence_agent(
    model=your_llm_model,
    aiware_client=aiware_client,
    target=your_target_selector,  # Default target for all queries
    model_bulk=optional_bulk_model,  # For large contexts
    max_tokens_per_request=80000  # Context size management
)

# Execute a query
result = await agent.ainvoke(
    {"messages": [HumanMessage("What's the screen time for John Doe?")]},
    context={
        "target": {"kind": "tdo_ids", "tdo_ids": ["tdo1", "tdo2"]}  # Override default target
    }
)
```

The agent automatically:
1. Generates an execution plan: `FIND_FACE → MERGE → AGGREGATE → OUTPUT`
2. Executes the plan against the specified TDOs (with retry on failure)
3. Handles large result sets through bulk processing if needed
4. Returns a natural language answer: "John Doe appears for 2 minutes and 15 seconds total"

#### Retry Behavior Example

```python
# If plan generation fails:
# Attempt 1: LLM generates invalid plan → replan
# Attempt 2: LLM generates valid plan → execute
# If execution fails:
# Attempt 1: Execution error → rerun same plan
# Attempt 2: Execution error again → replan (generate new plan)
# Attempt 3: New plan generated → execute
# If still failing: → end (graceful termination)
```

#### Integration with Other Components

The agent serves as the orchestration layer that:
- Uses **prompts.py** for system context and domain knowledge
- Calls **plan.py** tools for structured plan generation  
- Delegates to **executor.py** for deterministic plan execution
- Leverages **client.py** for aiWARE data access
- Operates on **data.py** schemas for type safety
- Executes **ops.py** operations in sequence

This design separates concerns while providing a unified interface for complex media analysis tasks.

### 7. Background Context (`prompts.py`)

Provides domain knowledge and context to the LLM about aiWARE concepts:

#### Key Concepts Explained:

**Temporal Data Objects (TDOs)**
- Containers for media assets and their analysis results
- Include metadata like duration, creation time, asset type
- Users may refer to them as "videos", "files", or "media"

**Watchlists**
- Saved searches that continuously monitor for specific content
- Automatically generate mentions when matching content is found
- Support complex query logic with boolean operators

**Mentions**
- Results produced by watchlists when matching content is detected
- Point to specific TDOs and time ranges within them
- Include audience metrics and hit counts
- Link advertiser/brand information for commercial monitoring

**Segments vs Records**
- **Segments**: Raw time-bounded detections (e.g., face at 10-15 seconds)
- **Records**: Processed/aggregated data (e.g., total screen time = 45 seconds)

## Common Usage Patterns

### Screen Time Analysis
```
FIND_FACE (entity_id="...") → MERGE → AGGREGATE (sum duration) → OUTPUT
```

### Content Discovery
```
FIND_TRANSCRIPT (query="keyword") → PROJECT (transcript, timestamps) → OUTPUT
```

### Temporal Relationships
```
FIND_FACE → FIND_TRANSCRIPT → JOIN_TEMPORAL (overlaps) → OUTPUT
```

### Entity Counting
```
GET_FACES → AGGREGATE (count_distinct by label) → OUTPUT
```

### Content Summarization
```
GET_TRANSCRIPTS (granularity="full") → PROJECT (transcript) → OUTPUT
```

## Error Handling

The system includes comprehensive error handling:
- Plan validation before execution
- Operation-level error collection
- Graceful degradation for missing data
- Clear error messages for debugging

## Performance Considerations

- Uses Polars for efficient dataframe operations
- Async I/O for aiWARE communication
- Intelligent result chunking for large datasets
- LRU caching for repeated queries
- Token-aware truncation for LLM context limits

This toolkit enables sophisticated media analysis through natural language queries while maintaining the precision and performance required for production workloads.