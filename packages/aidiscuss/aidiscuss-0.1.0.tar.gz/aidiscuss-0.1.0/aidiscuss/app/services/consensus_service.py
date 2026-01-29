"""
Consensus Detection Service

Analyzes conversation for consensus and agreement patterns.
Used to automatically detect when conversation goals are achieved.
"""

from typing import Dict, List, Optional, Tuple
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from sqlalchemy.ext.asyncio import AsyncSession

from aidiscuss.app.services.llm_provider import create_llm
from aidiscuss.app.models.consensus_tracking import ConsensusSnapshot


class ConsensusService:
    """
    Service for detecting consensus in multi-agent conversations

    Methods:
    - Analyze recent messages for agreement/disagreement
    - Calculate consensus scores
    - Track consensus trends over time
    - Identify agreement and disagreement topics
    """

    def __init__(self, analysis_model: str = "gpt-4o-mini", analysis_provider: str = "openai"):
        """
        Initialize consensus service

        Args:
            analysis_model: Model to use for consensus analysis
            analysis_provider: Provider for analysis model
        """
        self.analysis_model = analysis_model
        self.analysis_provider = analysis_provider

    async def calculate_consensus_score(
        self,
        conversation_id: str,
        turn_number: int,
        recent_messages: List[BaseMessage],
        conversation_goal: str,
        agent_ids: List[str],
        window_size: int = 5
    ) -> ConsensusSnapshot:
        """
        Calculate consensus score for recent conversation segment

        Uses LLM to analyze:
        - Level of agreement among agents
        - Topics of agreement vs. disagreement
        - Agent alignments and coalitions
        - Trend direction

        Args:
            conversation_id: Conversation identifier
            turn_number: Current turn number
            recent_messages: Recent messages to analyze
            conversation_goal: Goal of conversation
            agent_ids: IDs of participating agents
            window_size: Number of messages to analyze

        Returns:
            ConsensusSnapshot with consensus metrics
        """
        # Get the most recent messages
        messages_to_analyze = recent_messages[-window_size:] if len(recent_messages) > window_size else recent_messages

        if len(messages_to_analyze) < 2:
            # Not enough data for consensus analysis
            return ConsensusSnapshot(
                conversation_id=conversation_id,
                turn_number=turn_number,
                consensus_score=0.0,
                confidence=0.0,
                analysis_method="insufficient_data"
            )

        # Build conversation text
        conversation_text = "\n".join([
            f"{msg.name or 'User'}: {msg.content}"
            for msg in messages_to_analyze
        ])

        # Analyze consensus using LLM
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Analyze the following conversation segment for consensus among participants.

Conversation Goal: {goal}

Participating Agents: {agents}

Recent Conversation:
{conversation}

Analyze the conversation and provide:
1. Overall consensus score (0.0 to 1.0)
   - 1.0 = Complete agreement, decision reached
   - 0.7-0.9 = Strong consensus, minor details remain
   - 0.4-0.7 = Partial agreement, key disagreements exist
   - 0.0-0.4 = Significant disagreement or no conclusion

2. Topics where agents agree
3. Topics where agents disagree
4. Agent alignments (which agents share similar views)
5. Consensus trend (increasing, decreasing, or stable)
6. Confidence in your assessment (0.0-1.0)

Respond with JSON:
{{
    "consensus_score": 0.0-1.0,
    "agreement_topics": ["topic1", "topic2"],
    "disagreement_topics": ["topic1", "topic2"],
    "agent_alignments": {{
        "viewpoint1": ["agent1", "agent2"],
        "viewpoint2": ["agent3"]
    }},
    "consensus_trend": "increasing|decreasing|stable",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation of consensus assessment"
}}"""),
            ("human", "Analyze consensus.")
        ])

        try:
            llm = create_llm(
                provider_name=self.analysis_provider,
                model=self.analysis_model,
                temperature=0.0
            )

            response = await llm.ainvoke(
                prompt.format_messages(
                    goal=conversation_goal,
                    agents=", ".join(agent_ids),
                    conversation=conversation_text
                )
            )

            # Parse JSON response
            import json
            result = json.loads(response.content)

            # Create consensus snapshot
            snapshot = ConsensusSnapshot(
                conversation_id=conversation_id,
                turn_number=turn_number,
                consensus_score=result.get("consensus_score", 0.0),
                agreement_topics=result.get("agreement_topics", []),
                disagreement_topics=result.get("disagreement_topics", []),
                agent_alignments=result.get("agent_alignments", {}),
                analysis_method="llm_judge",
                confidence=result.get("confidence", 0.5),
                consensus_trend=result.get("consensus_trend", "stable")
            )

            return snapshot

        except Exception as e:
            print(f"Consensus analysis error: {e}")
            # Return neutral consensus on error
            return ConsensusSnapshot(
                conversation_id=conversation_id,
                turn_number=turn_number,
                consensus_score=0.5,
                confidence=0.0,
                analysis_method="error"
            )

    async def detect_decision_point(
        self,
        recent_messages: List[BaseMessage],
        goal: str
    ) -> Tuple[bool, str]:
        """
        Detect if a decision or conclusion has been reached

        Looks for:
        - Explicit decision statements
        - Agreement phrases
        - Conclusion markers

        Args:
            recent_messages: Recent conversation messages
            goal: Conversation goal

        Returns:
            Tuple of (decision_reached, decision_summary)
        """
        if not recent_messages:
            return False, ""

        # Get last few messages
        last_messages = recent_messages[-3:]
        conversation_text = "\n".join([
            f"{msg.name or 'User'}: {msg.content}"
            for msg in last_messages
        ])

        # Check for decision markers
        decision_markers = [
            "we agree", "consensus", "decided", "conclusion",
            "in summary", "to summarize", "final decision",
            "we've concluded", "agreed upon", "settled"
        ]

        has_decision_marker = any(
            marker in conversation_text.lower()
            for marker in decision_markers
        )

        if has_decision_marker:
            # Use LLM to extract decision summary
            prompt = ChatPromptTemplate.from_messages([
                ("system", """Extract the decision or conclusion from this conversation segment.

Goal: {goal}

Conversation:
{conversation}

If a decision or conclusion has been reached, summarize it in 1-2 sentences.
If no clear decision, respond with "No decision reached."

Decision summary:"""),
                ("human", "Extract decision.")
            ])

            try:
                llm = create_llm(
                    provider_name=self.analysis_provider,
                    model=self.analysis_model,
                    temperature=0.0
                )

                response = await llm.ainvoke(
                    prompt.format_messages(
                        goal=goal,
                        conversation=conversation_text
                    )
                )

                decision_summary = response.content.strip()

                if "no decision" not in decision_summary.lower():
                    return True, decision_summary

            except Exception as e:
                print(f"Decision detection error: {e}")

        return False, ""

    async def track_topic_coverage(
        self,
        messages: List[BaseMessage],
        planned_topics: List[str]
    ) -> Dict[str, bool]:
        """
        Track which planned topics have been covered

        Args:
            messages: Conversation messages
            planned_topics: List of topics to cover

        Returns:
            Dictionary mapping topic -> covered (bool)
        """
        if not planned_topics or not messages:
            return {}

        conversation_text = "\n".join([
            f"{msg.name or 'User'}: {msg.content}"
            for msg in messages
        ])

        coverage = {}

        for topic in planned_topics:
            # Simple keyword check
            topic_lower = topic.lower()
            conversation_lower = conversation_text.lower()

            # Check if topic or related keywords appear
            covered = topic_lower in conversation_lower

            coverage[topic] = covered

        return coverage

    async def identify_conflict_areas(
        self,
        recent_messages: List[BaseMessage]
    ) -> List[str]:
        """
        Identify areas of disagreement or conflict

        Args:
            recent_messages: Recent conversation messages

        Returns:
            List of conflict areas/topics
        """
        if len(recent_messages) < 3:
            return []

        conversation_text = "\n".join([
            f"{msg.name or 'User'}: {msg.content}"
            for msg in recent_messages[-5:]
        ])

        # Use LLM to identify conflicts
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Identify areas of disagreement or conflict in this conversation.

Conversation:
{conversation}

List the specific topics or points where participants disagree.
If there are no disagreements, respond with an empty JSON array.

Respond with JSON:
{{
    "conflicts": ["conflict area 1", "conflict area 2"]
}}"""),
            ("human", "Identify conflicts.")
        ])

        try:
            llm = create_llm(
                provider_name=self.analysis_provider,
                model=self.analysis_model,
                temperature=0.0
            )

            response = await llm.ainvoke(
                prompt.format_messages(conversation=conversation_text)
            )

            # Parse JSON response
            import json
            result = json.loads(response.content)

            return result.get("conflicts", [])

        except Exception as e:
            print(f"Conflict identification error: {e}")
            return []

    def calculate_trend(
        self,
        current_score: float,
        previous_scores: List[float]
    ) -> str:
        """
        Calculate consensus trend based on score history

        Args:
            current_score: Current consensus score
            previous_scores: List of previous scores (oldest to newest)

        Returns:
            Trend: "increasing", "decreasing", or "stable"
        """
        if not previous_scores:
            return "stable"

        # Get recent scores (last 3)
        recent_scores = previous_scores[-3:] if len(previous_scores) >= 3 else previous_scores

        # Calculate average of recent vs current
        avg_recent = sum(recent_scores) / len(recent_scores)

        # Determine trend
        diff = current_score - avg_recent

        if diff > 0.1:
            return "increasing"
        elif diff < -0.1:
            return "decreasing"
        else:
            return "stable"

    async def save_consensus_snapshot(
        self,
        snapshot: ConsensusSnapshot,
        db: AsyncSession
    ):
        """
        Save consensus snapshot to database

        Args:
            snapshot: Consensus snapshot to save
            db: Database session
        """
        from aidiscuss.app.models.consensus_tracking import ConsensusTracking
        from nanoid import generate

        # Create database model
        tracking = ConsensusTracking.from_schema(
            schema=snapshot,
            tracking_id=generate(size=12)
        )

        db.add(tracking)
        await db.commit()
