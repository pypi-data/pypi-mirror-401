"""
Safeguards for Multi-Agent Conversations

Implements safeguards to prevent:
- Agent domination (participation balancing)
- Repetitive responses (novelty detection)
- Infinite loops (turn limits, cycle detection)
"""

from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

from aidiscuss.app.services.langgraph.state import ConversationState


class ParticipationBalancer:
    """
    Prevents agent domination and ensures balanced participation

    Features:
    - Track consecutive turns per agent
    - Calculate participation balance metrics
    - Select speakers to balance participation
    - Detect and warn about imbalance
    """

    def __init__(self, max_consecutive: int = 3, balance_threshold: float = 0.4):
        """
        Initialize participation balancer

        Args:
            max_consecutive: Maximum consecutive turns allowed per agent
            balance_threshold: Threshold for participation imbalance (0-1)
        """
        self.max_consecutive = max_consecutive
        self.balance_threshold = balance_threshold

    def check_consecutive_limit(self, state: ConversationState, agent_id: str) -> bool:
        """
        Check if agent has reached consecutive turn limit

        Args:
            state: Current conversation state
            agent_id: Agent to check

        Returns:
            True if agent has hit limit, False otherwise
        """
        if agent_id not in state["agent_participation"]:
            return False

        participation = state["agent_participation"][agent_id]
        return participation.consecutive_turns >= self.max_consecutive

    def calculate_balance_score(self, state: ConversationState) -> float:
        """
        Calculate overall participation balance score

        Uses Gini coefficient: 0 = perfect equality, 1 = maximum inequality

        Args:
            state: Current conversation state

        Returns:
            Balance score (0-1, lower is more balanced)
        """
        participation = state["agent_participation"]

        if not participation:
            return 0.0

        # Get total turns for each agent
        turns = [p.total_turns for p in participation.values()]

        if sum(turns) == 0:
            return 0.0

        # Calculate Gini coefficient
        n = len(turns)
        turns_sorted = sorted(turns)

        cumsum = 0
        for i, t in enumerate(turns_sorted):
            cumsum += (2 * (i + 1) - n - 1) * t

        gini = cumsum / (n * sum(turns)) if sum(turns) > 0 else 0.0

        return gini

    def select_balanced_speaker(self, state: ConversationState) -> str:
        """
        Select next speaker with participation balancing

        Scoring criteria:
        - Prefer agents with fewer total turns
        - Penalty for consecutive turns
        - Bonus for quality (if available)

        Args:
            state: Current conversation state

        Returns:
            Agent ID for next speaker
        """
        participation = state["agent_participation"]
        agent_ids = state["agent_ids"]

        if not agent_ids:
            raise ValueError("No agents available")

        # Calculate expected average participation
        total_turns = state["turn_number"]
        agent_count = len(agent_ids)
        expected_avg = total_turns / agent_count if agent_count > 0 else 0

        # Score each agent
        scores = {}
        for agent_id in agent_ids:
            part = participation[agent_id]

            # Base score: inverse of total turns (prefer underrepresented)
            if total_turns > 0:
                participation_score = 1.0 - (part.total_turns / total_turns)
            else:
                participation_score = 1.0

            # Penalty for overparticipation
            overparticipation_penalty = max(0, part.total_turns - expected_avg) * 0.3

            # Heavy penalty for consecutive turns
            consecutive_penalty = part.consecutive_turns * 2.0

            # Bonus for quality (if available)
            quality_bonus = part.average_quality() * 0.2

            # Final score
            scores[agent_id] = (
                participation_score
                + quality_bonus
                - overparticipation_penalty
                - consecutive_penalty
            )

        # Select agent with highest score
        return max(scores.items(), key=lambda x: x[1])[0]

    def reset_consecutive_counts(self, state: ConversationState, except_agent: str):
        """
        Reset consecutive counts for all agents except current speaker

        Args:
            state: Current conversation state
            except_agent: Agent to exclude from reset (current speaker)
        """
        for agent_id in state["agent_ids"]:
            if agent_id != except_agent:
                state["agent_participation"][agent_id].reset_consecutive()

    def get_participation_report(self, state: ConversationState) -> dict:
        """
        Generate participation report for analytics

        Args:
            state: Current conversation state

        Returns:
            Dictionary with participation metrics
        """
        participation = state["agent_participation"]
        total_turns = state["turn_number"]

        if total_turns == 0:
            return {"balance_score": 0.0, "agents": {}}

        report = {
            "balance_score": self.calculate_balance_score(state),
            "total_turns": total_turns,
            "agents": {}
        }

        for agent_id, part in participation.items():
            report["agents"][agent_id] = {
                "total_turns": part.total_turns,
                "consecutive_turns": part.consecutive_turns,
                "percentage": (part.total_turns / total_turns * 100) if total_turns > 0 else 0,
                "average_quality": part.average_quality()
            }

        return report


class NoveltyDetector:
    """
    Detects and prevents repetitive responses using embedding similarity

    Features:
    - Generate embeddings for responses
    - Compare with recent response history
    - Calculate novelty scores
    - Flag repetitive content
    """

    def __init__(
        self,
        threshold: float = 0.3,
        model_name: str = "all-MiniLM-L6-v2",
        max_history: int = 20
    ):
        """
        Initialize novelty detector

        Args:
            threshold: Minimum novelty score (1.0 - similarity) required
            model_name: Sentence transformer model for embeddings
            max_history: Maximum number of embeddings to keep in history
        """
        self.threshold = threshold
        self.max_history = max_history
        self._model: Optional[SentenceTransformer] = None
        self.model_name = model_name

    @property
    def model(self) -> SentenceTransformer:
        """Lazy load the embedding model"""
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    async def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text

        Args:
            text: Text to embed

        Returns:
            Embedding vector as list of floats
        """
        # Run in executor to avoid blocking
        import asyncio
        loop = asyncio.get_event_loop()

        embedding = await loop.run_in_executor(
            None,
            self.model.encode,
            text
        )

        return embedding.tolist()

    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings

        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector

        Returns:
            Similarity score (0-1)
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        # Cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)

        if norm_product == 0:
            return 0.0

        similarity = dot_product / norm_product
        return float(similarity)

    async def compute_novelty_score(
        self,
        response: str,
        recent_embeddings: List[List[float]]
    ) -> float:
        """
        Compute novelty score for response

        Novelty = 1.0 - max_similarity with recent responses
        - 1.0 = completely novel
        - 0.0 = duplicate of previous response

        Args:
            response: Response text to evaluate
            recent_embeddings: List of recent response embeddings

        Returns:
            Novelty score (0-1)
        """
        if not recent_embeddings:
            return 1.0  # First response is always novel

        # Generate embedding for new response
        new_embedding = await self.get_embedding(response)

        # Compare with recent embeddings
        max_similarity = 0.0
        for old_embedding in recent_embeddings[-10:]:  # Check last 10
            similarity = self.compute_similarity(new_embedding, old_embedding)
            max_similarity = max(max_similarity, similarity)

        novelty = 1.0 - max_similarity
        return novelty

    async def check_and_update(
        self,
        state: ConversationState,
        response: str
    ) -> tuple[bool, float]:
        """
        Check novelty and update embeddings history

        Args:
            state: Current conversation state
            response: Response to check

        Returns:
            Tuple of (is_novel_enough, novelty_score)
        """
        # Compute novelty score
        recent_embeddings = state.get("recent_response_embeddings", [])
        novelty_score = await self.compute_novelty_score(response, recent_embeddings)

        # Update embeddings history
        new_embedding = await self.get_embedding(response)

        if "recent_response_embeddings" not in state:
            state["recent_response_embeddings"] = []

        state["recent_response_embeddings"].append(new_embedding)

        # Keep only recent history
        if len(state["recent_response_embeddings"]) > self.max_history:
            state["recent_response_embeddings"] = state["recent_response_embeddings"][-self.max_history:]

        # Check threshold
        is_novel = novelty_score >= self.threshold

        return is_novel, novelty_score

    def get_duplicate_candidates(
        self,
        state: ConversationState,
        similarity_threshold: float = 0.8
    ) -> List[tuple[int, int, float]]:
        """
        Find pairs of messages that are likely duplicates

        Args:
            state: Current conversation state
            similarity_threshold: Minimum similarity to flag as duplicate

        Returns:
            List of (index1, index2, similarity) tuples
        """
        embeddings = state.get("recent_response_embeddings", [])

        if len(embeddings) < 2:
            return []

        duplicates = []

        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                similarity = self.compute_similarity(embeddings[i], embeddings[j])

                if similarity >= similarity_threshold:
                    duplicates.append((i, j, similarity))

        return duplicates


class CycleDetector:
    """
    Detects infinite loops and repetitive patterns in conversation

    Features:
    - Detect when conversation is stuck in a loop
    - Track topic changes
    - Identify when no progress is being made
    """

    def __init__(self, window_size: int = 5):
        """
        Initialize cycle detector

        Args:
            window_size: Number of recent turns to analyze
        """
        self.window_size = window_size

    def detect_stuck_conversation(self, state: ConversationState) -> tuple[bool, str]:
        """
        Detect if conversation is stuck (no progress)

        Indicators:
        - Very high similarity in recent messages
        - Same agents going back and forth
        - No new information being added

        Args:
            state: Current conversation state

        Returns:
            Tuple of (is_stuck, reason)
        """
        messages = state.get("messages", [])

        if len(messages) < self.window_size:
            return False, ""

        recent = messages[-self.window_size:]

        # Check if only 2 agents talking
        agents = set(msg.name for msg in recent if msg.name)
        if len(agents) == 2 and len(state["agent_ids"]) > 2:
            return True, "Only 2 agents engaging while others are silent"

        # Check for repetitive patterns
        # This is a simplified check - could be enhanced with embedding comparison
        contents = [msg.content[:100].lower() for msg in recent]
        unique_contents = len(set(contents))

        if unique_contents <= 2:
            return True, "Highly repetitive content in recent messages"

        return False, ""

    def should_inject_variety(self, state: ConversationState) -> bool:
        """
        Determine if variety injection is needed

        Args:
            state: Current conversation state

        Returns:
            True if variety injection recommended
        """
        is_stuck, _ = self.detect_stuck_conversation(state)
        return is_stuck
