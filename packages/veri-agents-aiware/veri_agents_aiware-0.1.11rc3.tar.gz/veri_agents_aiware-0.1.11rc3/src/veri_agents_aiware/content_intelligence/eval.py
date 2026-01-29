"""
Evaluation script for the Content Intelligence Agent using Langfuse and OpenEvals.
This script sets up the necessary clients, defines the evaluation prompt,
and runs the evaluation on a specified dataset.
"""

import os
from typing import cast
import asyncio
from langchain_aws import ChatBedrockConverse
from langfuse import Langfuse, get_client, Evaluation
from openevals import create_async_llm_as_judge
from openevals.types import EvaluatorResult
from pydantic import TypeAdapter

from aiware.common.auth import TokenAuth, AiwareApiKey
from veri_agents_aiware.aiware_client.async_client import AsyncAgentsAiware
from veri_agents_aiware.content_intelligence import create_content_intelligence_agent
from veri_agents_aiware.content_intelligence import TargetSelector

CORRECTNESS_PROMPT = """You are an expert data labeler evaluating model outputs for correctness.

Your task is to assign a score based on the following rubric:

<Rubric>
  A correct answer:
  - Provides accurate and complete information
  - Contains no factual errors
  - Addresses all parts of the question
  - Is logically consistent
  - Uses precise and accurate terminology

  When scoring, you should penalize:
  - Factual errors or inaccuracies
  - Incomplete or partial answers
  - Misleading or ambiguous statements
  - Incorrect terminology
  - Logical inconsistencies
  - Missing key information

Scores should be in the range of 0.0 to 1.0, with the following guidelines:
- 1.0: Perfectly correct answer meeting all criteria
- 0.8: Mostly correct with minor issues
- 0.5: Partially correct but with significant omissions or errors
- 0.2: Largely incorrect with few correct elements
- 0.0: Completely incorrect or irrelevant answer
</Rubric>

<Instructions>
  - Carefully read the input and output
  - Check for factual accuracy and completeness
  - Focus on correctness of information rather than style or verbosity
</Instructions>

<Reminder>
  The goal is to evaluate factual correctness and completeness of the response.
</Reminder>

<input>
{inputs}
</input>

<output>
{outputs}
</output>

Use the reference outputs below to help you evaluate the correctness of the response:

<reference_outputs>
{reference_outputs}
</reference_outputs>
"""


async def main():
    """Main function to set up clients and run the evaluation."""
    aiware_token = os.getenv("VERITONE_AIWARE_API_KEY")
    aiware_url = os.getenv("VERITONE_AIWARE_BASE_URL")
    langfuse_public = os.getenv("LANGFUSE_PUBLIC_KEY")
    langfuse_secret = os.getenv("LANGFUSE_SECRET_KEY")
    langfuse_url = os.getenv("LANGFUSE_URL", "https://langfuse.varp.tech")

    if not (langfuse_public and langfuse_secret):
        raise ValueError(
            "LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY environment variables must be set."
        )
    if not (aiware_token and aiware_url):
        raise ValueError(
            "VERITONE_AIWARE_API_KEY and VERITONE_AIWARE_BASE_URL environment variables must be set."
        )

    Langfuse(
        public_key=langfuse_public,
        secret_key=langfuse_secret,
        host=langfuse_url,
    )

    aiware_client = AsyncAgentsAiware(
        base_url=aiware_url,
        auth=TokenAuth(token=AiwareApiKey(aiware_token)),
    )

    bulk_llm = ChatBedrockConverse(
        model="arn:aws:bedrock:us-east-1:075494626733:application-inference-profile/kl8qab6pdp97",
        base_model="us.amazon.nova-micro-v1:0",
        provider="amazon",
        region_name="us-east-1",
    )
    summary_llm = ChatBedrockConverse(
        max_tokens=2000,
        model="arn:aws:bedrock:us-east-1:075494626733:application-inference-profile/nhxrhd3b0en8",
        base_model="us.amazon.nova-2-lite-v1:0",
        provider="amazon",
        region_name="us-east-1",
    )
    llm = ChatBedrockConverse(
        model="arn:aws:bedrock:us-east-1:075494626733:application-inference-profile/nqd9c00141tr",
        base_model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        provider="anthropic",
        region_name="us-east-1",
    )
    eval_llm = ChatBedrockConverse(
        max_tokens=2000,
        model="arn:aws:bedrock:us-east-1:075494626733:application-inference-profile/nhxrhd3b0en8",
        base_model="us.amazon.nova-2-lite-v1:0",
        provider="amazon",
        region_name="us-east-1",
    )

    async def eval_task(*, input, output, expected_output, metadata, **kwargs):
        correctness_evaluator = create_async_llm_as_judge(
            prompt=CORRECTNESS_PROMPT,
            judge=eval_llm,
            continuous=True,
        )
        results = cast(
            EvaluatorResult,
            await correctness_evaluator(
                inputs=str(input["messages"]),
                outputs=str(output["messages"]),
                reference_outputs=str(expected_output["messages"]),
            ),
        )
        return Evaluation(
            name="Correctness", value=results["score"], comment=results["comment"]
        )

    async def run_task(*, item, **kwargs):
        print(item.input)
        messages = item.input.get("messages")
        target_json = item.input.get("context", {}).get("target")
        print(target_json)
        adapter = TypeAdapter(TargetSelector)
        target = adapter.validate_python(target_json)

        content_agent = create_content_intelligence_agent(
            model=llm,
            summary_model=summary_llm,
            bulk_model=bulk_llm,
            aiware_client=aiware_client,
            target=target,
        )

        result = await content_agent.ainvoke(input={"messages": messages})  # type: ignore
        return {"messages": result["messages"][-1].text}

    # Run on dataset we retrieve from langfuse
    langfuse = get_client()
    dataset = langfuse.get_dataset("content_intelligence/veritoneinc_basic")
    dataset.run_experiment(
        name="Content Intelligence Evaluation",
        description="Regular evaluation of the content intelligence agent",
        task=run_task,
        evaluators=[eval_task],
        max_concurrency=5,
    )


if __name__ == "__main__":
    asyncio.run(main())
