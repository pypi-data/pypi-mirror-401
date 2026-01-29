"""
Quality Service

Provides quality assessment capabilities:
- RAG grounding validation
- LLM-as-Judge evaluation
- Novelty detection
- Citation extraction
"""

from typing import Dict, List, Optional
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from sqlalchemy.ext.asyncio import AsyncSession

from aidiscuss.app.services.llm_provider import create_llm
from aidiscuss.app.services.langgraph.safeguards import NoveltyDetector


class QualityService:
    """
    Service for assessing response quality

    Integrates multiple quality checks:
    1. RAG grounding - Validate response uses provided documents
    2. LLM-as-Judge - Assess quality, relevance, and goal alignment
    3. Novelty detection - Prevent repetitive responses
    4. Citation validation - Ensure proper sourcing
    """

    def __init__(self, judge_model: str = "gpt-4o-mini", judge_provider: str = "openai"):
        """
        Initialize quality service

        Args:
            judge_model: Model to use for LLM-as-Judge
            judge_provider: Provider for judge model
        """
        self.judge_model = judge_model
        self.judge_provider = judge_provider
        self.novelty_detector = NoveltyDetector()

    async def rag_grounding_check(
        self,
        response: str,
        rag_context: str,
        require_citations: bool = False
    ) -> float:
        """
        Check if response is grounded in RAG context

        Uses LLM to assess:
        - Does response use information from context?
        - Are claims supported by provided documents?
        - Are citations present (if required)?

        Args:
            response: Agent response to check
            rag_context: RAG knowledge base context
            require_citations: Whether citations are required

        Returns:
            Grounding score (0-1)
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Assess how well the response is grounded in the provided knowledge base context.

Knowledge Base Context:
{rag_context}

Response to Evaluate:
{response}

Evaluate based on:
1. Does the response use information from the knowledge base?
2. Are claims made in the response supported by the context?
3. Are there unsupported claims or hallucinations?
{citation_requirement}

Respond with JSON:
{{
    "grounding_score": 0.0-1.0,
    "supported_claims": ["claim1", "claim2"],
    "unsupported_claims": ["claim1"],
    "has_citations": true/false,
    "reasoning": "brief explanation"
}}

Where grounding_score:
- 1.0 = Fully grounded, all claims supported
- 0.7-0.9 = Mostly grounded, minor unsupported details
- 0.4-0.6 = Partially grounded
- 0.0-0.4 = Poorly grounded or hallucinating"""),
            ("human", "Assess grounding.")
        ])

        citation_req = ""
        if require_citations:
            citation_req = "4. Are proper citations included (e.g., [Source: ...])?"

        try:
            llm = create_llm(
                provider_name=self.judge_provider,
                model=self.judge_model,
                temperature=0.0
            )

            response_obj = await llm.ainvoke(
                prompt.format_messages(
                    rag_context=rag_context[:3000],  # Limit context size
                    response=response,
                    citation_requirement=citation_req
                )
            )

            # Parse JSON response
            import json
            result = json.loads(response_obj.content)

            grounding_score = result.get("grounding_score", 0.5)

            # Penalty if citations required but missing
            if require_citations and not result.get("has_citations", False):
                grounding_score *= 0.5

            return grounding_score

        except Exception as e:
            print(f"RAG grounding check error: {e}")
            return 0.5  # Neutral score on error

    async def llm_judge_evaluate(
        self,
        agent_id: str,
        response: str,
        conversation_context: List[BaseMessage],
        goal: str
    ) -> float:
        """
        Use LLM-as-Judge to evaluate response quality

        Evaluation criteria:
        - Relevance to conversation goal
        - Quality of reasoning
        - Coherence with conversation
        - Helpfulness and clarity

        Args:
            agent_id: ID of agent who generated response
            response: Response to evaluate
            conversation_context: Recent conversation messages
            goal: Conversation goal

        Returns:
            Quality score (0-1)
        """
        # Build context string
        context_str = "\n".join([
            f"{msg.name or 'User'}: {msg.content[:200]}"
            for msg in conversation_context[-5:]
        ])

        prompt = ChatPromptTemplate.from_messages([
            ("system", """Evaluate the quality of an agent's response in a multi-agent conversation.

Conversation Goal: {goal}

Recent Conversation:
{context}

Agent Response to Evaluate:
{response}

Evaluate on these criteria:
1. Relevance - Does it address the goal and conversation context?
2. Quality - Is the reasoning sound and well-articulated?
3. Coherence - Does it fit naturally in the conversation flow?
4. Helpfulness - Does it move the conversation forward?
5. Clarity - Is it clear and well-structured?

Respond with JSON:
{{
    "overall_score": 0.0-1.0,
    "relevance": 0.0-1.0,
    "quality": 0.0-1.0,
    "coherence": 0.0-1.0,
    "helpfulness": 0.0-1.0,
    "clarity": 0.0-1.0,
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1"],
    "reasoning": "brief explanation"
}}

Where overall_score:
- 0.9-1.0 = Excellent response
- 0.7-0.9 = Good response
- 0.5-0.7 = Acceptable response
- 0.3-0.5 = Poor response
- 0.0-0.3 = Very poor or off-topic"""),
            ("human", "Evaluate quality.")
        ])

        try:
            llm = create_llm(
                provider_name=self.judge_provider,
                model=self.judge_model,
                temperature=0.0
            )

            response_obj = await llm.ainvoke(
                prompt.format_messages(
                    goal=goal,
                    context=context_str,
                    response=response
                )
            )

            # Parse JSON response
            import json
            result = json.loads(response_obj.content)

            return result.get("overall_score", 0.5)

        except Exception as e:
            print(f"LLM judge error: {e}")
            return 0.5

    async def check_novelty(
        self,
        response: str,
        recent_embeddings: List[List[float]]
    ) -> float:
        """
        Check novelty of response (wrapper around NoveltyDetector)

        Args:
            response: Response to check
            recent_embeddings: Recent response embeddings

        Returns:
            Novelty score (0-1, higher is more novel)
        """
        return await self.novelty_detector.compute_novelty_score(response, recent_embeddings)

    async def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for text (wrapper around NoveltyDetector)

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        return await self.novelty_detector.get_embedding(text)

    def extract_citations(self, response: str) -> List[str]:
        """
        Extract citations from response

        Looks for patterns like:
        - [Source: ...]
        - (Source: ...)
        - According to [document]

        Args:
            response: Response text

        Returns:
            List of extracted citations
        """
        import re

        citations = []

        # Pattern 1: [Source: ...]
        pattern1 = r'\[Source:\s*([^\]]+)\]'
        citations.extend(re.findall(pattern1, response))

        # Pattern 2: (Source: ...)
        pattern2 = r'\(Source:\s*([^\)]+)\)'
        citations.extend(re.findall(pattern2, response))

        # Pattern 3: According to [...]
        pattern3 = r'According to\s+\[([^\]]+)\]'
        citations.extend(re.findall(pattern3, response))

        return citations

    def validate_citations(
        self,
        citations: List[str],
        rag_context: str
    ) -> tuple[int, int]:
        """
        Validate that citations actually exist in RAG context

        Args:
            citations: List of citations from response
            rag_context: RAG knowledge base context

        Returns:
            Tuple of (valid_count, total_count)
        """
        if not citations:
            return 0, 0

        valid_count = 0
        for citation in citations:
            # Simple check: is citation text found in context?
            if citation.lower() in rag_context.lower():
                valid_count += 1

        return valid_count, len(citations)

    async def aggregate_quality_score(
        self,
        scores: Dict[str, float],
        weights: Optional[Dict[str, float]] = None
    ) -> float:
        """
        Aggregate multiple quality scores into single score

        Args:
            scores: Dictionary of score_name -> score_value
            weights: Optional weights for each score type

        Returns:
            Weighted aggregate score (0-1)
        """
        if not scores:
            return 0.5

        # Default weights
        if weights is None:
            weights = {
                "rag_grounding": 0.3,
                "llm_judge": 0.4,
                "novelty": 0.2,
                "consistency": 0.1
            }

        total_weight = 0.0
        weighted_sum = 0.0

        for score_name, score_value in scores.items():
            weight = weights.get(score_name, 0.0)
            weighted_sum += score_value * weight
            total_weight += weight

        if total_weight == 0:
            return sum(scores.values()) / len(scores)

        return weighted_sum / total_weight

    async def generate_quality_feedback(
        self,
        scores: Dict[str, float],
        thresholds: Dict[str, float]
    ) -> List[str]:
        """
        Generate feedback messages based on quality scores

        Args:
            scores: Quality scores
            thresholds: Threshold for each score type

        Returns:
            List of feedback messages
        """
        feedback = []

        for score_name, score_value in scores.items():
            threshold = thresholds.get(score_name, 0.6)

            if score_value < threshold:
                if score_name == "rag_grounding":
                    feedback.append(
                        f"Response not well-grounded in provided knowledge (score: {score_value:.2f})"
                    )
                elif score_name == "llm_judge":
                    feedback.append(
                        f"Overall quality below threshold (score: {score_value:.2f})"
                    )
                elif score_name == "novelty":
                    feedback.append(
                        f"Response too similar to previous messages (novelty: {score_value:.2f})"
                    )
                elif score_name == "consistency":
                    feedback.append(
                        f"Response inconsistent with agent persona (score: {score_value:.2f})"
                    )

        return feedback
