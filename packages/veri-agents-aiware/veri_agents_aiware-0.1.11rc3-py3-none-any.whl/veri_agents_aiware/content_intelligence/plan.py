from __future__ import annotations
import hashlib
import logging
from typing import Any, Type, Literal

from pydantic import BaseModel, Field, ConfigDict
from langchain_core.tools import BaseTool

from veri_agents_aiware.content_intelligence.ops import DiscriminatedOp
from veri_agents_aiware.content_intelligence.data import TargetSelector
from veri_agents_aiware.content_intelligence.prompts import get_plan_prompt

log = logging.getLogger(__name__)

class InvalidPlanError(Exception):
    pass

class Plan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    plan_version: str = "1.0"
    steps: list[DiscriminatedOp]

    def signature(self) -> str:
        body = self.model_dump_json(by_alias=True)
        return hashlib.sha256(body.encode()).hexdigest()[:16]

    def prettify(self) -> str:
        s = ""
        for step in self.steps:
            s += f"- {step.op}({', '.join(f'{k}={v}' for k, v in step.model_dump().items() if v)})\n"
        return s


class CreatePlanTool(BaseTool):
    """Tool for creating execution plans with proper validation.
       Create using the `build` method to provide target-specific context.
    """

    name: str = "create_plan"
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"

    @classmethod
    def build(cls, target: TargetSelector) -> "CreatePlanTool":
        desc = get_plan_prompt(target)
        return cls(description=desc)

    class CreatePlanInput(BaseModel):
        """Input for creating a plan."""

        plan: Plan = Field(
            description="The execution plan with a sequence of operations"
        )
        reasoning: str = Field(
            description="Brief explanation of why this plan was chosen for the query"
        )

    args_schema: Type[BaseModel] = CreatePlanInput  # pyright: ignore[reportIncompatibleVariableOverride]

    def _run(self, plan: Plan, reasoning: str) -> tuple[str, dict[str, Any]]:
        """Create and validate a plan."""
        try:
            # Handle both Plan objects and dictionaries
            if isinstance(plan, dict):
                # Convert dict to Plan object
                validated_plan = Plan.model_validate(plan)
            else:
                # Already a Plan object, validate it
                validated_plan = Plan.model_validate(plan.model_dump(by_alias=True))

            result = {
                "success": True,
                "plan": validated_plan.model_dump(by_alias=True),
                "reasoning": reasoning,
                "plan_signature": validated_plan.signature(),
                "num_steps": len(validated_plan.steps),
            }

            log.info(f"Plan created successfully: {len(validated_plan.steps)} steps")

            message = f"Created plan:\n\n{str(plan.prettify()) if plan else 'No valid plan'}.\n\nReasoning: {reasoning if reasoning else 'N/A'}."
            return message, result

        except Exception as e:
            error_result = {"success": False, "error": str(e), "reasoning": reasoning}
            log.error(f"Plan creation failed: {e}")
            return f"Error: {str(e)}", error_result

