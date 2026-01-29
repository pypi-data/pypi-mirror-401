"""
Memory Service for automatic fact extraction, summarization, and checkpoint creation

Implements Phase 2: Memory Enhancement
- Automatic fact extraction from conversations
- Periodic summary generation (every 10-15 turns or 4000 tokens)
- Checkpoint creation on topic changes
- Memory-aware context building for agents
"""

import asyncio
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class Fact(BaseModel):
    """Extracted fact from conversation"""
    id: str
    text: str
    importance: float = Field(ge=0, le=1)  # 0-1 scale
    source_turn: int
    timestamp: datetime


class Checkpoint(BaseModel):
    """Conversation checkpoint for topic changes"""
    id: str
    turn_number: int
    topic: str
    summary: str
    timestamp: datetime


class ConversationMemory(BaseModel):
    """Memory for a conversation"""
    conversation_id: str
    rolling_summary: str = ""
    facts: List[Fact] = Field(default_factory=list)
    checkpoints: List[Checkpoint] = Field(default_factory=list)
    last_summary_turn: int = 0
    last_checkpoint_turn: int = 0
    total_tokens: int = 0


class MemoryService:
    """
    Service for managing conversation memory with automatic extraction

    Features:
    - Fact extraction with importance scoring
    - Rolling summary generation
    - Topic change detection and checkpointing
    - Memory-aware context building
    """

    def __init__(self, llm=None):
        """
        Initialize memory service

        Args:
            llm: Language model for summarization and extraction (optional)
        """
        self.llm = llm
        self.memories: Dict[str, ConversationMemory] = {}

        # Configuration
        self.summary_interval_turns = 10  # Summarize every N turns
        self.summary_interval_tokens = 4000  # Or when tokens exceed this
        self.checkpoint_similarity_threshold = 0.3  # Topic change threshold
        self.max_facts = 50  # Maximum facts to retain
        self.fact_pruning_threshold = 0.3  # Prune facts below this importance

    def get_or_create_memory(self, conversation_id: str) -> ConversationMemory:
        """Get existing memory or create new one"""
        if conversation_id not in self.memories:
            self.memories[conversation_id] = ConversationMemory(
                conversation_id=conversation_id
            )
        return self.memories[conversation_id]

    async def extract_facts(
        self,
        conversation_id: str,
        messages: List[Dict],
        turn_number: int
    ) -> List[Fact]:
        """
        Extract facts from recent messages using LLM

        Args:
            conversation_id: Conversation ID
            messages: Recent messages to analyze
            turn_number: Current turn number

        Returns:
            List of extracted facts
        """
        if not self.llm:
            print("Warning: LLM not initialized for memory service, skipping fact extraction")
            return []

        if len(messages) < 2:
            return []

        memory = self.get_or_create_memory(conversation_id)

        # Build extraction prompt
        conversation_text = "\n".join([
            f"{msg.get('role', 'unknown')}: {msg.get('content', '')}"
            for msg in messages[-5:]  # Last 5 messages
        ])

        extraction_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a fact extraction system. Extract key facts from the conversation that should be remembered.

For each fact, provide:
1. The fact text (concise, specific)
2. Importance score (0.0-1.0):
   - 0.7-1.0: Critical decisions, commitments, specific data
   - 0.4-0.7: Preferences, opinions, context
   - 0.0-0.4: Minor details, casual mentions

Return in JSON format:
[
  {"text": "User prefers Python over JavaScript", "importance": 0.6},
  {"text": "Project deadline is March 15", "importance": 0.9}
]

Only extract facts that are:
- Specific and verifiable
- Likely to be relevant in future turns
- Not already obvious from context

If no significant facts, return empty array []."""),
            HumanMessage(content=f"Conversation:\n{conversation_text}")
        ])

        try:
            # Generate fact extraction
            response = await self.llm.ainvoke(extraction_prompt.format_messages())

            # Parse JSON response
            import json
            import uuid
            facts_data = json.loads(response.content)

            facts = []
            for fact_dict in facts_data:
                if isinstance(fact_dict, dict) and "text" in fact_dict:
                    fact = Fact(
                        id=str(uuid.uuid4()),
                        text=fact_dict["text"],
                        importance=fact_dict.get("importance", 0.5),
                        source_turn=turn_number,
                        timestamp=datetime.now()
                    )
                    facts.append(fact)
                    memory.facts.append(fact)

            # Prune low-importance facts if too many
            self._prune_facts(memory)

            return facts

        except Exception as e:
            print(f"Error extracting facts: {e}")
            return []

    def _prune_facts(self, memory: ConversationMemory):
        """Prune low-importance facts to maintain max_facts limit"""
        if len(memory.facts) <= self.max_facts:
            return

        # Sort by importance (descending)
        memory.facts.sort(key=lambda f: f.importance, reverse=True)

        # Keep top max_facts, but remove any below pruning threshold
        memory.facts = [
            f for i, f in enumerate(memory.facts)
            if i < self.max_facts and f.importance >= self.fact_pruning_threshold
        ]

    async def generate_summary(
        self,
        conversation_id: str,
        messages: List[Dict],
        turn_number: int
    ) -> str:
        """
        Generate rolling summary of conversation

        Uses extractive + abstractive approach:
        1. Identify key messages
        2. Summarize main themes and decisions
        3. Keep under 500 tokens

        Args:
            conversation_id: Conversation ID
            messages: All messages in conversation
            turn_number: Current turn number

        Returns:
            Summary text
        """
        if not self.llm:
            print("Warning: LLM not initialized for memory service, skipping summary generation")
            return ""

        if len(messages) < 5:
            return ""

        memory = self.get_or_create_memory(conversation_id)

        # Get messages since last summary
        new_messages = messages[memory.last_summary_turn:]

        if len(new_messages) < 3:
            return memory.rolling_summary  # Not enough new content

        # Build conversation text
        conversation_text = "\n".join([
            f"{msg.get('role', 'unknown')}: {msg.get('content', '')}"
            for msg in new_messages
        ])

        # Include previous summary for continuity
        previous_summary = memory.rolling_summary or "No previous summary."

        summary_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a conversation summarizer. Create a concise rolling summary of the conversation.

Guidelines:
- Focus on main topics, decisions, and key points
- Keep summary under 500 tokens (~2000 characters)
- Integrate with previous summary if provided
- Use bullet points for clarity
- Prioritize recent content but maintain historical context

Format:
## Main Topics
- Topic 1: Brief description
- Topic 2: Brief description

## Key Decisions/Outcomes
- Decision 1
- Decision 2

## Current Focus
Brief description of current discussion"""),
            HumanMessage(content=f"""Previous Summary:
{previous_summary}

New Messages:
{conversation_text}

Generate updated rolling summary:""")
        ])

        try:
            response = await self.llm.ainvoke(summary_prompt.format_messages())
            summary = response.content.strip()

            # Update memory
            memory.rolling_summary = summary
            memory.last_summary_turn = turn_number

            return summary

        except Exception as e:
            print(f"Error generating summary: {e}")
            return memory.rolling_summary

    async def create_checkpoint(
        self,
        conversation_id: str,
        messages: List[Dict],
        turn_number: int,
        force: bool = False
    ) -> Optional[Checkpoint]:
        """
        Create checkpoint if topic has changed significantly

        Uses cosine similarity between current and previous checkpoint topics
        to detect major topic shifts.

        Args:
            conversation_id: Conversation ID
            messages: All messages
            turn_number: Current turn number
            force: Force checkpoint creation

        Returns:
            Checkpoint if created, None otherwise
        """
        if not self.llm:
            print("Warning: LLM not initialized for memory service, skipping checkpoint creation")
            return None

        if len(messages) < 5:
            return None

        memory = self.get_or_create_memory(conversation_id)

        # Don't checkpoint too frequently
        if not force and turn_number - memory.last_checkpoint_turn < 5:
            return None

        # Get recent messages
        recent_messages = messages[-10:]  # Last 10 messages
        conversation_text = "\n".join([
            f"{msg.get('role', 'unknown')}: {msg.get('content', '')}"
            for msg in recent_messages
        ])

        # Detect current topic
        topic_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""Identify the main topic/theme of this conversation segment in 3-5 words.
Examples: "Python web development", "Travel planning for Japan", "Machine learning optimization"

Be specific and concise."""),
            HumanMessage(content=f"Conversation:\n{conversation_text}\n\nMain topic:")
        ])

        try:
            response = await self.llm.ainvoke(topic_prompt.format_messages())
            current_topic = response.content.strip()

            # Check if topic changed from last checkpoint
            topic_changed = False
            if memory.checkpoints:
                last_topic = memory.checkpoints[-1].topic
                # Simple string similarity check (could use embeddings for better accuracy)
                topic_changed = not self._topics_similar(current_topic, last_topic)
            else:
                topic_changed = True  # First checkpoint

            if not topic_changed and not force:
                return None

            # Generate checkpoint summary
            checkpoint_summary = await self._generate_checkpoint_summary(
                messages[-20:]  # More context for checkpoint
            )

            # Create checkpoint
            import uuid
            checkpoint = Checkpoint(
                id=str(uuid.uuid4()),
                turn_number=turn_number,
                topic=current_topic,
                summary=checkpoint_summary,
                timestamp=datetime.now()
            )

            memory.checkpoints.append(checkpoint)
            memory.last_checkpoint_turn = turn_number

            # Limit checkpoints
            if len(memory.checkpoints) > 20:
                memory.checkpoints = memory.checkpoints[-20:]

            return checkpoint

        except Exception as e:
            print(f"Error creating checkpoint: {e}")
            return None

    def _topics_similar(self, topic1: str, topic2: str) -> bool:
        """Simple topic similarity check using word overlap"""
        words1 = set(topic1.lower().split())
        words2 = set(topic2.lower().split())

        if not words1 or not words2:
            return False

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        jaccard_similarity = len(intersection) / len(union)

        return jaccard_similarity >= self.checkpoint_similarity_threshold

    async def _generate_checkpoint_summary(self, messages: List[Dict]) -> str:
        """Generate brief summary for checkpoint"""
        if not self.llm:
            return ""

        conversation_text = "\n".join([
            f"{msg.get('role', 'unknown')}: {msg.get('content', '')}"
            for msg in messages
        ])

        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="Summarize this conversation segment in 1-2 sentences."),
            HumanMessage(content=conversation_text)
        ])

        try:
            response = await self.llm.ainvoke(prompt.format_messages())
            return response.content.strip()
        except Exception as e:
            print(f"Error generating checkpoint summary: {e}")
            return ""

    def build_context(
        self,
        conversation_id: str,
        messages: List[Dict],
        max_tokens: int = 4000
    ) -> Dict:
        """
        Build memory-aware context for agent prompts

        Returns dict with:
        - system_context: String with summary, facts, checkpoints
        - relevant_history: Recent messages that fit in token budget
        - facts: List of relevant facts
        - total_tokens: Estimated token count

        Args:
            conversation_id: Conversation ID
            messages: All messages
            max_tokens: Maximum tokens for context

        Returns:
            Context dictionary
        """
        memory = self.get_or_create_memory(conversation_id)

        # Build system context from memory
        context_parts = []

        # Add rolling summary
        if memory.rolling_summary:
            context_parts.append(f"## Conversation Summary\n{memory.rolling_summary}\n")

        # Add top facts
        if memory.facts:
            top_facts = sorted(memory.facts, key=lambda f: f.importance, reverse=True)[:10]
            facts_text = "\n".join([f"- {fact.text}" for fact in top_facts])
            context_parts.append(f"## Key Facts\n{facts_text}\n")

        # Add recent checkpoint if available
        if memory.checkpoints:
            latest_checkpoint = memory.checkpoints[-1]
            context_parts.append(
                f"## Current Topic\n{latest_checkpoint.topic}\n{latest_checkpoint.summary}\n"
            )

        system_context = "\n".join(context_parts)
        system_tokens = self._estimate_tokens(system_context)

        # Calculate remaining tokens for message history
        available_tokens = max_tokens - system_tokens - 500  # Reserve 500 for safety

        # Select recent messages that fit
        relevant_history = []
        used_tokens = 0

        for msg in reversed(messages):
            msg_tokens = self._estimate_tokens(msg.get("content", ""))
            if used_tokens + msg_tokens > available_tokens:
                break
            relevant_history.insert(0, msg)
            used_tokens += msg_tokens

        return {
            "system_context": system_context,
            "relevant_history": relevant_history,
            "facts": memory.facts[:10],
            "total_tokens": system_tokens + used_tokens,
        }

    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ≈ 4 characters)"""
        return max(1, len(text) // 4)

    async def process_conversation_turn(
        self,
        conversation_id: str,
        messages: List[Dict],
        turn_number: int,
        force_summary: bool = False,
        force_checkpoint: bool = False
    ) -> Dict:
        """
        Process a conversation turn: extract facts, update summary, create checkpoints

        This is the main method to call after each turn in orchestration.

        Args:
            conversation_id: Conversation ID
            messages: All messages in conversation
            turn_number: Current turn number
            force_summary: Force summary generation
            force_checkpoint: Force checkpoint creation

        Returns:
            Dict with updates: {facts, summary, checkpoint}
        """
        memory = self.get_or_create_memory(conversation_id)

        # Estimate total tokens
        total_tokens = sum(self._estimate_tokens(msg.get("content", "")) for msg in messages)
        memory.total_tokens = total_tokens

        updates = {
            "facts": [],
            "summary": None,
            "checkpoint": None
        }

        # Extract facts asynchronously (non-blocking)
        if self.llm:
            facts_task = self.extract_facts(conversation_id, messages, turn_number)
        else:
            facts_task = None

        # Check if summary needed
        turns_since_summary = turn_number - memory.last_summary_turn
        tokens_since_summary = total_tokens  # Simplified

        should_summarize = (
            force_summary or
            turns_since_summary >= self.summary_interval_turns or
            tokens_since_summary >= self.summary_interval_tokens
        )

        # Check if checkpoint needed
        should_checkpoint = (
            force_checkpoint or
            turn_number % 10 == 0  # Every 10 turns, check for topic change
        )

        # Run tasks
        tasks = []

        if facts_task:
            tasks.append(facts_task)

        if should_summarize and self.llm:
            tasks.append(self.generate_summary(conversation_id, messages, turn_number))

        if should_checkpoint and self.llm:
            tasks.append(self.create_checkpoint(conversation_id, messages, turn_number, force_checkpoint))

        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Parse results
            result_idx = 0

            if facts_task:
                if not isinstance(results[result_idx], Exception):
                    updates["facts"] = results[result_idx]
                result_idx += 1

            if should_summarize and self.llm:
                if not isinstance(results[result_idx], Exception):
                    updates["summary"] = results[result_idx]
                result_idx += 1

            if should_checkpoint and self.llm:
                if not isinstance(results[result_idx], Exception):
                    updates["checkpoint"] = results[result_idx]

        return updates

    def get_memory_stats(self, conversation_id: str) -> Dict:
        """Get memory statistics for conversation"""
        memory = self.get_or_create_memory(conversation_id)

        return {
            "conversation_id": conversation_id,
            "facts_count": len(memory.facts),
            "checkpoints_count": len(memory.checkpoints),
            "has_summary": bool(memory.rolling_summary),
            "last_summary_turn": memory.last_summary_turn,
            "last_checkpoint_turn": memory.last_checkpoint_turn,
            "total_tokens": memory.total_tokens,
        }


# Singleton instance
memory_service = MemoryService()
