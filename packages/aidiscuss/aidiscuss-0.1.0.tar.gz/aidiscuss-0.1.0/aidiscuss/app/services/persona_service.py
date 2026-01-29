"""
Persona Consistency Service - Phase 3
Implements LLM-as-a-Judge consistency scoring, periodic reminders, and diversity enforcement
"""

import asyncio
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class ConsistencyScore(BaseModel):
    """Consistency evaluation result"""
    score: float = Field(ge=0, le=1)  # 0-1 scale
    prompt_to_line_score: float = Field(ge=0, le=1)  # Alignment with persona
    line_to_line_score: float = Field(ge=0, le=1)  # No contradictions
    feedback: str  # Explanation of score
    violations: List[str] = Field(default_factory=list)  # Specific issues


class DiversityMetrics(BaseModel):
    """Diversity analysis for conversation"""
    response_similarity: float = Field(ge=0, le=1)  # How similar recent responses are
    topic_diversity: float = Field(ge=0, le=1)  # Topic variation
    opinion_diversity: float = Field(ge=0, le=1)  # Viewpoint variation
    suggestions: List[str] = Field(default_factory=list)  # Improvement suggestions


class PersonaService:
    """
    Service for maintaining persona consistency and conversation diversity

    Features:
    - Periodic persona reminders (every N turns)
    - LLM-as-a-Judge consistency scoring
    - Diversity enforcement
    - Conversation quality metrics
    """

    def __init__(self, llm=None):
        """Initialize persona service with optional LLM"""
        self.llm = llm

        # Configuration
        self.reminder_interval = 5  # Remind agent of persona every N turns
        self.consistency_check_interval = 10  # Check consistency every N turns
        self.min_consistency_threshold = 0.7  # Alert if below this
        self.min_diversity_threshold = 0.6  # Alert if below this

        # Tracking
        self.consistency_history: Dict[str, List[ConsistencyScore]] = {}
        self.diversity_history: Dict[str, List[DiversityMetrics]] = {}

    def build_persona_reminder(
        self,
        agent_system_prompt: str,
        turn_number: int,
        recent_messages: List[Dict]
    ) -> str:
        """
        Build persona reminder to inject periodically

        Args:
            agent_system_prompt: Original agent persona/system prompt
            turn_number: Current turn number
            recent_messages: Recent conversation messages

        Returns:
            Enhanced system prompt with persona reminder
        """
        if turn_number % self.reminder_interval != 0:
            return agent_system_prompt

        # Extract key persona traits
        persona_traits = self._extract_persona_traits(agent_system_prompt)

        reminder = f"""
{agent_system_prompt}

---
**IMPORTANT PERSONA REMINDER** (Turn {turn_number}):
Remember to maintain your core characteristics:
{persona_traits}

Stay true to your defined role and perspective throughout this conversation.
Avoid contradicting your established traits, opinions, or knowledge.
---
"""
        return reminder

    def _extract_persona_traits(self, system_prompt: str) -> str:
        """Extract key traits from system prompt for reminder"""
        # Simple heuristic: look for key phrases
        traits = []

        # Common persona indicators
        indicators = [
            "You are", "Your role is", "Your personality",
            "You believe", "You prefer", "Your expertise",
            "You should", "Always", "Never"
        ]

        lines = system_prompt.split('\n')
        for line in lines:
            if any(indicator.lower() in line.lower() for indicator in indicators):
                traits.append(f"- {line.strip()}")

        return '\n'.join(traits[:5]) if traits else "- Maintain your defined persona"

    async def evaluate_consistency(
        self,
        agent_id: str,
        agent_system_prompt: str,
        recent_responses: List[str],
        conversation_history: List[Dict]
    ) -> ConsistencyScore:
        """
        Evaluate persona consistency using LLM-as-a-Judge

        Based on NeurIPS 2025 research:
        - Prompt-to-line: Alignment with initial persona
        - Line-to-line: No contradictions within conversation

        Args:
            agent_id: Agent identifier
            agent_system_prompt: Original persona definition
            recent_responses: Last N agent responses
            conversation_history: Full conversation context

        Returns:
            ConsistencyScore with detailed evaluation
        """
        if not self.llm:
            print("Warning: LLM not initialized for persona service, skipping consistency evaluation")
            return ConsistencyScore(
                score=1.0,
                prompt_to_line_score=1.0,
                line_to_line_score=1.0,
                feedback="LLM not available for evaluation"
            )

        if len(recent_responses) < 2:
            return ConsistencyScore(
                score=1.0,
                prompt_to_line_score=1.0,
                line_to_line_score=1.0,
                feedback="Insufficient data for evaluation"
            )

        # Build evaluation prompt
        responses_text = "\n\n".join([
            f"Response {i+1}: {resp}"
            for i, resp in enumerate(recent_responses[-5:])
        ])

        eval_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a persona consistency evaluator. Analyze whether an AI agent's responses align with their defined persona and remain internally consistent.

Evaluate on two dimensions:

1. **Prompt-to-Line Consistency** (0-1):
   - Does the agent stay true to their defined persona/role?
   - Are responses aligned with stated beliefs, expertise, and personality?

2. **Line-to-Line Consistency** (0-1):
   - Are responses internally consistent with each other?
   - No contradictions in facts, opinions, or behavior?

Return JSON:
{
  "prompt_to_line_score": 0.0-1.0,
  "line_to_line_score": 0.0-1.0,
  "overall_score": 0.0-1.0,
  "feedback": "Brief explanation",
  "violations": ["specific issue 1", "specific issue 2"]
}

Score Guide:
- 0.9-1.0: Excellent consistency
- 0.7-0.9: Good, minor deviations
- 0.5-0.7: Moderate issues
- Below 0.5: Significant consistency problems"""),
            HumanMessage(content=f"""**Agent Persona:**
{agent_system_prompt}

**Recent Responses:**
{responses_text}

Evaluate consistency:""")
        ])

        try:
            response = await self.llm.ainvoke(eval_prompt.format_messages())

            # Parse JSON response
            import json
            result = json.loads(response.content)

            score = ConsistencyScore(
                score=result.get("overall_score", 0.8),
                prompt_to_line_score=result.get("prompt_to_line_score", 0.8),
                line_to_line_score=result.get("line_to_line_score", 0.8),
                feedback=result.get("feedback", ""),
                violations=result.get("violations", [])
            )

            # Track history
            if agent_id not in self.consistency_history:
                self.consistency_history[agent_id] = []
            self.consistency_history[agent_id].append(score)

            return score

        except Exception as e:
            print(f"Error evaluating consistency: {e}")
            return ConsistencyScore(
                score=0.8,
                prompt_to_line_score=0.8,
                line_to_line_score=0.8,
                feedback=f"Evaluation error: {str(e)}"
            )

    async def evaluate_diversity(
        self,
        conversation_id: str,
        all_agent_responses: Dict[str, List[str]],
        conversation_history: List[Dict]
    ) -> DiversityMetrics:
        """
        Evaluate conversation diversity to prevent echo chambers

        Analyzes:
        - Response similarity between agents
        - Topic diversity over time
        - Opinion/viewpoint diversity

        Args:
            conversation_id: Conversation identifier
            all_agent_responses: Map of agent_id -> list of responses
            conversation_history: Full conversation

        Returns:
            DiversityMetrics with analysis and suggestions
        """
        if not self.llm:
            print("Warning: LLM not initialized for persona service, skipping diversity evaluation")
            return DiversityMetrics(
                response_similarity=0.5,
                topic_diversity=0.5,
                opinion_diversity=0.5,
                suggestions=["LLM not available for diversity analysis"]
            )

        if len(conversation_history) < 5:
            return DiversityMetrics(
                response_similarity=0.5,
                topic_diversity=0.5,
                opinion_diversity=0.5,
                suggestions=["Need more conversation data"]
            )

        # Prepare recent responses from all agents
        recent_responses = []
        for agent_id, responses in all_agent_responses.items():
            recent_responses.extend(responses[-3:])

        responses_text = "\n\n".join([
            f"Response {i+1}: {resp}"
            for i, resp in enumerate(recent_responses)
        ])

        diversity_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a conversation diversity analyzer. Evaluate how diverse and rich a multi-agent conversation is.

Analyze three dimensions:

1. **Response Similarity** (0 = identical, 1 = highly diverse):
   - Are agents providing different perspectives?
   - Or just echoing each other?

2. **Topic Diversity** (0 = single topic, 1 = broad range):
   - How varied are the topics discussed?
   - Are new angles being explored?

3. **Opinion Diversity** (0 = consensus, 1 = healthy disagreement):
   - Are different viewpoints represented?
   - Is there productive debate?

Return JSON:
{
  "response_similarity": 0.0-1.0,
  "topic_diversity": 0.0-1.0,
  "opinion_diversity": 0.0-1.0,
  "overall_diversity": 0.0-1.0,
  "suggestions": ["specific improvement 1", "improvement 2"]
}

High diversity (0.7+) indicates rich, engaging conversation.
Low diversity (<0.5) suggests echo chamber or repetition."""),
            HumanMessage(content=f"""**Recent Multi-Agent Responses:**
{responses_text}

Evaluate diversity:""")
        ])

        try:
            response = await self.llm.ainvoke(diversity_prompt.format_messages())

            import json
            result = json.loads(response.content)

            metrics = DiversityMetrics(
                response_similarity=result.get("response_similarity", 0.5),
                topic_diversity=result.get("topic_diversity", 0.5),
                opinion_diversity=result.get("opinion_diversity", 0.5),
                suggestions=result.get("suggestions", [])
            )

            # Track history
            if conversation_id not in self.diversity_history:
                self.diversity_history[conversation_id] = []
            self.diversity_history[conversation_id].append(metrics)

            return metrics

        except Exception as e:
            print(f"Error evaluating diversity: {e}")
            return DiversityMetrics(
                response_similarity=0.5,
                topic_diversity=0.5,
                opinion_diversity=0.5,
                suggestions=[f"Analysis error: {str(e)}"]
            )

    def generate_diversity_enforcement_prompt(
        self,
        metrics: DiversityMetrics,
        agent_system_prompt: str
    ) -> str:
        """
        Generate prompt additions to enforce diversity based on current metrics

        Args:
            metrics: Current diversity metrics
            agent_system_prompt: Base agent prompt

        Returns:
            Enhanced prompt with diversity enforcement
        """
        if metrics.response_similarity > self.min_diversity_threshold:
            return agent_system_prompt  # Diversity is good

        enforcement = "\n\n**DIVERSITY REMINDER:**\n"

        if metrics.response_similarity < 0.5:
            enforcement += "- Provide a UNIQUE perspective distinct from other agents\n"
            enforcement += "- Avoid repeating points already made\n"

        if metrics.topic_diversity < 0.5:
            enforcement += "- Explore NEW angles or aspects of the topic\n"
            enforcement += "- Introduce related but distinct considerations\n"

        if metrics.opinion_diversity < 0.5:
            enforcement += "- Express your DISTINCT viewpoint clearly\n"
            enforcement += "- Don't be afraid to respectfully disagree\n"

        return agent_system_prompt + enforcement

    async def get_conversation_quality_metrics(
        self,
        conversation_id: str,
        agent_id: Optional[str] = None
    ) -> Dict:
        """
        Get comprehensive quality metrics for conversation

        Args:
            conversation_id: Conversation to analyze
            agent_id: Specific agent (optional)

        Returns:
            Dictionary with quality metrics
        """
        metrics = {
            "conversation_id": conversation_id,
            "consistency": {},
            "diversity": {},
            "overall_quality": 0.0
        }

        # Aggregate consistency scores
        if agent_id:
            if agent_id in self.consistency_history:
                scores = self.consistency_history[agent_id]
                if scores:
                    avg_score = sum(s.score for s in scores) / len(scores)
                    metrics["consistency"][agent_id] = {
                        "average_score": avg_score,
                        "recent_score": scores[-1].score,
                        "trend": "improving" if len(scores) > 1 and scores[-1].score > scores[0].score else "stable",
                        "total_evaluations": len(scores)
                    }
        else:
            # All agents
            for aid, scores in self.consistency_history.items():
                if scores:
                    avg_score = sum(s.score for s in scores) / len(scores)
                    metrics["consistency"][aid] = {
                        "average_score": avg_score,
                        "recent_score": scores[-1].score
                    }

        # Aggregate diversity metrics
        if conversation_id in self.diversity_history:
            div_scores = self.diversity_history[conversation_id]
            if div_scores:
                latest = div_scores[-1]
                metrics["diversity"] = {
                    "response_similarity": latest.response_similarity,
                    "topic_diversity": latest.topic_diversity,
                    "opinion_diversity": latest.opinion_diversity,
                    "suggestions": latest.suggestions,
                    "total_evaluations": len(div_scores)
                }

        # Calculate overall quality (consistency + diversity)
        consistency_avg = 0.0
        if metrics["consistency"]:
            consistency_avg = sum(
                agent["average_score"]
                for agent in metrics["consistency"].values()
            ) / len(metrics["consistency"])

        diversity_avg = 0.0
        if metrics["diversity"]:
            diversity_avg = (
                metrics["diversity"].get("response_similarity", 0) +
                metrics["diversity"].get("topic_diversity", 0) +
                metrics["diversity"].get("opinion_diversity", 0)
            ) / 3

        metrics["overall_quality"] = (consistency_avg + diversity_avg) / 2

        return metrics

    def get_improvement_suggestions(
        self,
        conversation_id: str,
        agent_id: Optional[str] = None
    ) -> List[str]:
        """
        Get actionable suggestions for improving conversation quality

        Args:
            conversation_id: Conversation to analyze
            agent_id: Specific agent (optional)

        Returns:
            List of suggestions
        """
        suggestions = []

        # Check consistency issues
        if agent_id and agent_id in self.consistency_history:
            recent_scores = self.consistency_history[agent_id][-3:]
            if recent_scores:
                avg_score = sum(s.score for s in recent_scores) / len(recent_scores)
                if avg_score < self.min_consistency_threshold:
                    suggestions.append(
                        f"Agent {agent_id} showing consistency issues (score: {avg_score:.2f}). "
                        "Review persona definition and recent responses."
                    )
                    # Add specific violations
                    for score in recent_scores:
                        suggestions.extend(score.violations)

        # Check diversity issues
        if conversation_id in self.diversity_history:
            recent_diversity = self.diversity_history[conversation_id][-1]
            if recent_diversity.response_similarity < self.min_diversity_threshold:
                suggestions.append(
                    f"Low response diversity ({recent_diversity.response_similarity:.2f}). "
                    "Encourage agents to provide unique perspectives."
                )
            suggestions.extend(recent_diversity.suggestions)

        return list(set(suggestions))  # Remove duplicates


# Singleton instance
persona_service = PersonaService()
