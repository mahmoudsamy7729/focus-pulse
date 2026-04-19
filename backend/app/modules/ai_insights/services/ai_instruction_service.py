from app.modules.ai_insights.constants import (
    AI_INSIGHT_INSTRUCTION_VERSION,
    AIInsightInstructionName,
    AIInsightTargetPeriod,
)
from app.modules.ai_insights.exceptions import InvalidAIInsightTargetPeriodError
from app.modules.ai_insights.schemas import AnalysisInstruction


class AIInstructionService:
    required_sections = [
        "output_outcome",
        "generated_at",
        "summary",
        "detected_patterns",
        "behavior_insights",
        "supporting_evidence",
        "limitations",
    ]

    def get_instruction(self, period_granularity: str) -> AnalysisInstruction:
        if period_granularity == AIInsightTargetPeriod.DAILY.value:
            name = AIInsightInstructionName.DAILY_COMBINED_ANALYSIS.value
            period_text = "one local calendar day"
        elif period_granularity == AIInsightTargetPeriod.WEEKLY.value:
            name = AIInsightInstructionName.WEEKLY_COMBINED_ANALYSIS.value
            period_text = "one Monday-to-Sunday local calendar week"
        else:
            raise InvalidAIInsightTargetPeriodError("period_granularity must be daily or weekly")

        prompt = (
            f"Generate a combined analysis for {period_text}. Use only task names, durations, "
            "categories, tags, and aggregate totals. Exclude note text. Return summary, "
            "detected_patterns, behavior_insights, supporting_evidence, limitations, generated_at, "
            "and output_outcome. Every observation must cite supporting evidence."
        )
        return AnalysisInstruction(
            instruction_name=name,
            instruction_version=AI_INSIGHT_INSTRUCTION_VERSION,
            prompt=prompt,
            required_output_sections=self.required_sections,
        )
