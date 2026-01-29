"""
Optimized Multi-Agent Orchestrator with Parallel Processing
Enhanced with Memory Service integration (Phase 2)
"""

import asyncio
import random
from typing import AsyncIterator, Optional, Dict, List
from datetime import datetime, timedelta
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from pydantic import BaseModel, Field
from aidiscuss.app.models.agent import Agent
from aidiscuss.app.models.provider import Provider
from aidiscuss.app.services.llm_provider import ProviderService
from aidiscuss.app.services.memory_service import memory_service
from aidiscuss.app.services.persona_service import persona_service
from aidiscuss.app.services.tool_service import tool_service


class ConversationState(BaseModel):
    """State for multi-agent conversation"""

    messages: list[BaseMessage] = Field(default_factory=list)
    current_speaker: str | None = None
    turn_number: int = 0
    max_turns: int = 20
    agent_ids: list[str] = Field(default_factory=list)
    orchestration_strategy: str = "round-robin"


class ParallelOrchestratorService:
    """
    Optimized orchestrator with parallel processing capabilities
    """

    def __init__(
        self,
        agents: list[Agent],
        providers: dict[str, Provider],
        orchestration_strategy: str = "round-robin",
        max_turns: int = 20,
        enable_parallel: bool = True,
        rag_context: str | None = None,
        conversation_id: Optional[str] = None,
        enable_memory: bool = True,
        enable_persona_consistency: bool = True,
        enable_tools: bool = True,
    ):
        """
        Initialize orchestrator with optimization features

        Args:
            agents: List of agents participating
            providers: Dict of provider_id -> Provider
            orchestration_strategy: Strategy for turn-taking
            max_turns: Maximum number of turns
            enable_parallel: Whether to enable parallel agent execution
            rag_context: Optional RAG context to inject into prompts
            conversation_id: Conversation ID for memory tracking
            enable_memory: Enable automatic memory features (facts, summaries, checkpoints)
            enable_persona_consistency: Enable persona reminders and consistency checks (Phase 3)
            enable_tools: Enable tool use for agents (Phase 4)
        """
        self.agents = {agent.id: agent for agent in agents}
        self.providers = providers
        self.orchestration_strategy = orchestration_strategy
        self.max_turns = max_turns
        self.enable_parallel = enable_parallel
        self.rag_context = rag_context
        self.conversation_id = conversation_id
        self.enable_memory = enable_memory
        self.enable_persona_consistency = enable_persona_consistency
        self.enable_tools = enable_tools

        # Track agent responses for consistency/diversity evaluation
        self.agent_responses: Dict[str, List[str]] = {agent.id: [] for agent in agents}

        # Create LLM instances (cached)
        self.llms = {}
        for agent in agents:
            if agent.provider_id not in providers:
                raise ValueError(f"Provider '{agent.provider_id}' not found")

            provider = providers[agent.provider_id]
            llm = ProviderService.create_chat_model(provider, agent)

            # Bind tools to LLM if enabled AND agent has specific tools enabled
            agent_tools = getattr(agent, 'tools', []) or []
            if not isinstance(agent_tools, list):
                agent_tools = []

            # Check for any tool-using capability (calculator only for now)
            tool_ids = {'calculator'}
            agent_has_tools = bool(tool_ids & set(agent_tools))

            if self.enable_tools and agent_has_tools:
                # Get only the tools this agent has enabled
                tools = tool_service.get_tools_for_llm(enabled_tools=agent_tools)
                if tools and hasattr(llm, 'bind_tools'):
                    try:
                        llm = llm.bind_tools(tools)
                    except Exception as e:
                        print(f"Warning: Could not bind tools to agent {agent.id}: {e}")

            self.llms[agent.id] = llm

        # Initialize memory service with first available LLM
        if self.enable_memory and self.llms and not memory_service.llm:
            memory_service.llm = next(iter(self.llms.values()))

        # Initialize persona service with first available LLM
        if self.enable_persona_consistency and self.llms and not persona_service.llm:
            persona_service.llm = next(iter(self.llms.values()))

    async def select_next_speaker_intelligent(
        self,
        messages: list[BaseMessage],
        agent_consecutive_counts: Dict[str, int],
        agent_last_spoke_time: Dict[str, datetime]
    ) -> str:
        """
        Intelligently select next speaker using LLM based on conversation context.
        Can select an agent ID or "HUMAN" to wait for human input.
        Enforces rules: max 2 consecutive messages, 3-minute timeout override.
        When human speaks, all agents become eligible again.

        Args:
            messages: Conversation history
            agent_consecutive_counts: Map of agent_id -> consecutive message count
            agent_last_spoke_time: Map of agent_id -> last message timestamp

        Returns:
            Selected agent_id or "HUMAN" to wait for human input
        """
        # Check if last message was from human - if so, reset all consecutive counts
        if messages and isinstance(messages[-1], HumanMessage):
            # Human just spoke, all agents should be eligible
            eligible_agents = list(self.agents.keys())
        else:
            # Get eligible agents (not at consecutive limit)
            eligible_agents = []
            for agent_id, agent in self.agents.items():
                consecutive = agent_consecutive_counts.get(agent_id, 0)
                last_spoke = agent_last_spoke_time.get(agent_id)

                # Allow if under 2 consecutive OR if 3+ minutes since last spoke
                if consecutive < 2:
                    eligible_agents.append(agent_id)
                elif last_spoke and (datetime.now() - last_spoke) >= timedelta(minutes=3):
                    eligible_agents.append(agent_id)

        # Fallback if no eligible agents (shouldn't happen)
        if not eligible_agents:
            eligible_agents = list(self.agents.keys())

        # Build LLM prompt for speaker selection
        agent_info = []
        for agent_id in eligible_agents:
            agent = self.agents[agent_id]
            consecutive = agent_consecutive_counts.get(agent_id, 0)
            agent_info.append(f"- {agent.name} (ID: {agent_id}, consecutive messages: {consecutive})")

        # Add HUMAN as an option
        agent_info.append(f"- HUMAN (ID: HUMAN) - Select this if the conversation naturally needs human input")

        # Get last few messages for context
        recent_messages = messages[-6:] if len(messages) > 6 else messages
        conversation_context = "\n".join([
            f"{msg.__class__.__name__.replace('Message', '')}: {msg.content[:200]}"
            for msg in recent_messages
        ])

        # Check if human just spoke
        human_just_spoke = messages and isinstance(messages[-1], HumanMessage)
        human_context = "\n- The HUMAN just spoke, so all agents are now eligible to respond" if human_just_spoke else ""

        selection_prompt = f"""You are a conversation orchestrator for a multi-agent discussion.

Eligible speakers to choose from:
{chr(10).join(agent_info)}{human_context}

Recent conversation:
{conversation_context}

Based on the conversation flow, who should speak next? Choose the agent whose expertise or perspective would be most valuable for the current discussion point, OR select HUMAN if the conversation naturally needs human input (e.g., agents are asking questions, need clarification, or the discussion has reached a natural pause point).

Rules:
- Consider conversation context and natural flow
- If the human just contributed, prefer an agent who can directly address their point
- If agents are asking questions or seeking input, consider selecting HUMAN
- If conversation has been going for a while without human input, occasionally select HUMAN
- Avoid letting agents with high consecutive counts dominate
- Enable diverse perspectives
- Respond with ONLY the speaker ID: either an agent ID or "HUMAN" (nothing else)

Selected speaker ID:"""

        try:
            # Use first available LLM for selection
            selection_llm = next(iter(self.llms.values()))
            response = await selection_llm.ainvoke([HumanMessage(content=selection_prompt)])
            selected_id = response.content.strip()

            # Validate selection
            if selected_id == "HUMAN":
                return "HUMAN"
            elif selected_id in eligible_agents:
                return selected_id
        except Exception as e:
            print(f"Error in intelligent speaker selection: {e}")

        # Fallback: prefer agent with lowest consecutive count
        return min(eligible_agents, key=lambda aid: agent_consecutive_counts.get(aid, 0))

    def select_next_speaker(self, state: ConversationState) -> str:
        """Select next speaker based on strategy (legacy for non-intelligent modes)"""
        if self.orchestration_strategy == "parallel":
            return "all"
        elif self.orchestration_strategy == "random":
            return random.choice(state.agent_ids)
        else:
            # Default: round-robin
            current_index = state.turn_number % len(state.agent_ids)
            return state.agent_ids[current_index]

    async def generate_response(
        self, agent_id: str, messages: list[BaseMessage], turn_number: int = 0
    ) -> tuple[str, str]:
        """
        Generate response from specific agent (with memory + persona consistency)

        Args:
            agent_id: ID of agent
            messages: Conversation history
            turn_number: Current turn number

        Returns:
            Tuple of (agent_id, response_text)
        """
        agent = self.agents[agent_id]
        llm = self.llms[agent_id]

        # Build system prompt with multi-agent context
        system_content = agent.system_prompt

        # Add multi-agent conversation context
        agent_names = [self.agents[aid].name for aid in self.agents.keys()]
        other_agent_names = [name for name in agent_names if name != agent.name]

        system_content += f"\n\n# Multi-Agent Conversation Context"
        system_content += f"\nYou are {agent.name}, an AI agent in a multi-agent conversation."
        system_content += f"\nOther AI agents: {', '.join(other_agent_names)}"
        system_content += f"\n\n**CRITICAL INSTRUCTIONS:**"
        system_content += f"\n- Messages labeled 'human' or 'user' are from the User or HUMAN (the human participant)"
        system_content += f"\n- The User is an OBSERVER who may occasionally contribute to the discussion"
        system_content += f"\n- Your primary conversation is with OTHER AGENTS: {', '.join(other_agent_names)}"
        system_content += f"\n- When addressing the User, call them 'HUMAN' or 'Human' (not 'user' or anything else)"
        system_content += f"\n- If HUMAN contributes, acknowledge them briefly then continue discussing with agents"
        system_content += f"\n\n**CONVERSATION DYNAMICS:**"
        system_content += f"\n- You have been selected to speak because your perspective is valuable right now"
        system_content += f"\n- Engage naturally with other agents' and HUMAN's points - build on, question, or challenge their ideas"
        system_content += f"\n- Direct your responses to OTHER AGENTS by name, and if really needed to the user as 'HUMAN'"
        system_content += f"\n- Let the conversation flow naturally - you don't need to dominate"
        system_content += f"\n- If another agent should respond to a point, you can yield the floor"
        system_content += f"\n\nStay in character as {agent.name}. Address other AGENTS by their names, and the User as 'HUMAN'."

        # Add persona reminders (Phase 3)
        if self.enable_persona_consistency:
            messages_dict = [
                {"role": msg.__class__.__name__.replace("Message", "").lower(),
                 "content": msg.content}
                for msg in messages
            ]
            system_content = persona_service.build_persona_reminder(
                system_content,
                turn_number,
                messages_dict[-5:]
            )

        # Add memory context if enabled
        if self.enable_memory and self.conversation_id:
            # Convert BaseMessage to dict for memory service
            messages_dict = [
                {"role": msg.__class__.__name__.replace("Message", "").lower(),
                 "content": msg.content}
                for msg in messages
            ]
            memory_context = memory_service.build_context(
                self.conversation_id,
                messages_dict,
                max_tokens=4000
            )
            if memory_context["system_context"]:
                system_content = f"{system_content}\n\n# Conversation Memory\n{memory_context['system_context']}"

        # Add RAG context if available
        if self.rag_context:
            system_content = f"{system_content}\n\n# Relevant Knowledge\n{self.rag_context}"

        # Add system message with agent's persona
        full_messages = [SystemMessage(content=system_content)] + messages

        # Generate response asynchronously
        try:
            response = await llm.ainvoke(full_messages)

            # Handle tool calls if present AND agent has tools enabled
            agent_tools = getattr(agent, 'tools', []) or []
            if not isinstance(agent_tools, list):
                agent_tools = []
            tool_ids = {'calculator'}
            agent_has_tools = bool(tool_ids & set(agent_tools))

            if self.enable_tools and agent_has_tools and hasattr(response, 'tool_calls') and response.tool_calls:
                tool_results = []
                for tool_call in response.tool_calls:
                    tool_name = tool_call.get('name')
                    tool_args = tool_call.get('args', {})

                    # Execute tool
                    result = await tool_service.execute_tool(
                        tool_name=tool_name,
                        parameters=tool_args,
                        agent_id=agent_id
                    )

                    if result.success:
                        tool_results.append(f"[Tool: {tool_name}] {result.result}")
                    else:
                        tool_results.append(f"[Tool Error: {tool_name}] {result.error}")

                # Combine tool results with response
                final_response = response.content
                if tool_results:
                    tool_output = "\n".join(tool_results)
                    final_response = f"{final_response}\n\n{tool_output}" if final_response else tool_output

                return (agent_id, final_response)

            return (agent_id, response.content)
        except Exception as e:
            print(f"Error generating response from {agent_id}: {e}")
            return (agent_id, f"[Error: {str(e)}]")

    async def stream_response(
        self, agent_id: str, messages: list[BaseMessage], turn_number: int = 0
    ) -> AsyncIterator[tuple[str, str]]:
        """
        Stream response from specific agent (with memory + persona consistency)

        Args:
            agent_id: ID of agent
            messages: Conversation history
            turn_number: Current turn number

        Yields:
            Tuples of (agent_id, token)
        """
        agent = self.agents[agent_id]
        llm = self.llms[agent_id]

        # Build system prompt with multi-agent context
        system_content = agent.system_prompt

        # Add multi-agent conversation context
        agent_names = [self.agents[aid].name for aid in self.agents.keys()]
        other_agent_names = [name for name in agent_names if name != agent.name]

        system_content += f"\n\n# Multi-Agent Conversation Context"
        system_content += f"\nYou are {agent.name}, an AI agent in a multi-agent conversation."
        system_content += f"\nOther AI agents: {', '.join(other_agent_names)}"
        system_content += f"\n\n**CRITICAL INSTRUCTIONS:**"
        system_content += f"\n- Messages labeled 'human' or 'user' are from the User (the human participant)"
        system_content += f"\n- The User is an OBSERVER who may occasionally contribute to the discussion"
        system_content += f"\n- Your primary conversation is with OTHER AGENTS: {', '.join(other_agent_names)}"
        system_content += f"\n- When addressing the User, call them 'User' (not 'human' or anything else)"
        system_content += f"\n- If User contributes, acknowledge them briefly then continue discussing with agents"
        system_content += f"\n\n**CONVERSATION DYNAMICS:**"
        system_content += f"\n- You have been selected to speak because your perspective is valuable right now"
        system_content += f"\n- Engage naturally with other agents' points - build on, question, or challenge their ideas"
        system_content += f"\n- Direct your responses to OTHER AGENTS by name, not to the User"
        system_content += f"\n- Let the conversation flow naturally - you don't need to dominate"
        system_content += f"\n- If another agent should respond to a point, you can yield the floor"
        system_content += f"\n\nStay in character as {agent.name}. Address other AGENTS by their names, and the User as 'User'."

        # Add persona reminders (Phase 3)
        if self.enable_persona_consistency:
            messages_dict = [
                {"role": msg.__class__.__name__.replace("Message", "").lower(),
                 "content": msg.content}
                for msg in messages
            ]
            system_content = persona_service.build_persona_reminder(
                system_content,
                turn_number,
                messages_dict[-5:]
            )

        # Add memory context if enabled
        if self.enable_memory and self.conversation_id:
            # Convert BaseMessage to dict for memory service
            messages_dict = [
                {"role": msg.__class__.__name__.replace("Message", "").lower(),
                 "content": msg.content}
                for msg in messages
            ]
            memory_context = memory_service.build_context(
                self.conversation_id,
                messages_dict,
                max_tokens=4000
            )
            if memory_context["system_context"]:
                system_content = f"{system_content}\n\n# Conversation Memory\n{memory_context['system_context']}"

        # Add RAG context if available
        if self.rag_context:
            system_content = f"{system_content}\n\n# Relevant Knowledge\n{self.rag_context}"

        # Add system message
        full_messages = [SystemMessage(content=system_content)] + messages

        try:
            # Stream response
            tool_calls = []
            content_buffer = ""

            async for chunk in llm.astream(full_messages):
                # Collect tool calls
                if hasattr(chunk, "tool_calls") and chunk.tool_calls:
                    tool_calls.extend(chunk.tool_calls)

                # Stream content
                if hasattr(chunk, "content") and chunk.content:
                    content_buffer += chunk.content
                    yield (agent_id, chunk.content)

            # Execute tools after streaming completes AND agent has "tools" in their tools array
            agent_tools = getattr(agent, 'tools', []) or []
            agent_has_tools = 'tools' in agent_tools if isinstance(agent_tools, list) else False
            if self.enable_tools and agent_has_tools and tool_calls:
                for tool_call in tool_calls:
                    tool_name = tool_call.get('name')
                    tool_args = tool_call.get('args', {})

                    # Execute tool
                    result = await tool_service.execute_tool(
                        tool_name=tool_name,
                        parameters=tool_args,
                        agent_id=agent_id
                    )

                    if result.success:
                        tool_output = f"\n[Tool: {tool_name}] {result.result}"
                    else:
                        tool_output = f"\n[Tool Error: {tool_name}] {result.error}"

                    yield (agent_id, tool_output)

        except Exception as e:
            print(f"Error streaming from {agent_id}: {e}")
            yield (agent_id, f"[Error: {str(e)}]")

    async def run_parallel_agents(
        self, agent_ids: list[str], messages: list[BaseMessage]
    ) -> dict[str, str]:
        """
        Run multiple agents in parallel for the same prompt

        Args:
            agent_ids: List of agent IDs to run
            messages: Shared conversation history

        Returns:
            Dict of agent_id -> response
        """
        # Create tasks for all agents
        tasks = [
            self.generate_response(agent_id, messages) for agent_id in agent_ids
        ]

        # Run all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Build response dict
        responses = {}
        for result in results:
            if isinstance(result, Exception):
                print(f"Agent failed: {result}")
                continue
            agent_id, response = result
            responses[agent_id] = response

        return responses

    async def stream_parallel_agents(
        self, agent_ids: list[str], messages: list[BaseMessage]
    ) -> AsyncIterator[dict[str, any]]:
        """
        Stream responses from multiple agents in parallel

        Args:
            agent_ids: List of agent IDs
            messages: Shared conversation history

        Yields:
            Events with parallel agent updates
        """
        # Create async generators for each agent
        agent_streams = {
            agent_id: self.stream_response(agent_id, messages)
            for agent_id in agent_ids
        }

        # Track completion and responses
        active_agents = set(agent_ids)
        responses = {agent_id: "" for agent_id in agent_ids}

        # Stream tokens from all agents concurrently
        while active_agents:
            # Create tasks for next token from each active agent
            tasks = {}
            for agent_id in list(active_agents):
                stream = agent_streams[agent_id]
                tasks[agent_id] = asyncio.create_task(anext(stream, None))

            # Wait for any agent to produce a token
            done, pending = await asyncio.wait(
                tasks.values(), return_when=asyncio.FIRST_COMPLETED
            )

            # Process completed tokens
            for agent_id, task in tasks.items():
                if task in done:
                    result = await task
                    if result is None:
                        # Agent finished
                        active_agents.remove(agent_id)
                        yield {
                            "type": "agent_done",
                            "agent_id": agent_id,
                            "content": responses[agent_id],
                        }
                    else:
                        # Got token
                        _, token = result
                        responses[agent_id] += token
                        yield {
                            "type": "token",
                            "agent_id": agent_id,
                            "content": token,
                        }

    async def run_conversation(
        self, initial_message: str
    ) -> AsyncIterator[dict[str, any]]:
        """
        Run optimized multi-agent conversation with parallel support

        Args:
            initial_message: Initial user message

        Yields:
            Event dictionaries
        """
        messages: list[BaseMessage] = [HumanMessage(content=initial_message, name="human")]
        agent_ids = list(self.agents.keys())

        # Track consecutive turns per agent and last spoke time
        agent_consecutive_turns = {agent_id: 0 for agent_id in agent_ids}
        agent_last_spoke_time = {agent_id: None for agent_id in agent_ids}

        yield {
            "type": "start",
            "agent_ids": agent_ids,
            "orchestration_strategy": self.orchestration_strategy,
            "parallel_enabled": self.enable_parallel,
        }

        for turn in range(self.max_turns):
            # Check if last message was from human and reset consecutive counts
            if messages and isinstance(messages[-1], HumanMessage) and messages[-1].content != initial_message:
                # Human just spoke (not the initial message), reset all consecutive counts
                for agent_id in agent_ids:
                    agent_consecutive_turns[agent_id] = 0

            # Use intelligent speaker selection
            speaker_id = await self.select_next_speaker_intelligent(
                messages,
                agent_consecutive_turns,
                agent_last_spoke_time
            )

            # Handle HUMAN turn - wait for human input
            if speaker_id == "HUMAN":
                yield {
                    "type": "wait_for_human_turn",
                    "message": "The orchestrator selected HUMAN to speak next. Waiting for your input...",
                    "turn": turn,
                }
                # Don't update consecutive counts, conversation pauses here
                # The frontend/caller should handle this by breaking the loop and waiting for human input
                break

            # Update consecutive turn tracking (only for agent speakers)
            for agent_id in agent_ids:
                if agent_id == speaker_id:
                    agent_consecutive_turns[agent_id] += 1
                    agent_last_spoke_time[agent_id] = datetime.now()
                else:
                    agent_consecutive_turns[agent_id] = 0

            # Parallel mode: all agents respond simultaneously
            if speaker_id == "all" and self.enable_parallel:
                yield {
                    "type": "parallel_start",
                    "agent_ids": agent_ids,
                    "turn": turn,
                }

                # Stream from all agents in parallel
                async for event in self.stream_parallel_agents(agent_ids, messages):
                    yield event

                    # If agent finished, add to messages
                    if event["type"] == "agent_done":
                        messages.append(
                            AIMessage(
                                content=event["content"], name=event["agent_id"]
                            )
                        )

                yield {"type": "parallel_done", "turn": turn}

            # Sequential mode: one agent at a time
            else:
                agent = self.agents[speaker_id]

                yield {
                    "type": "agent_start",
                    "agent_id": speaker_id,
                    "agent_name": agent.name,
                    "turn": turn,
                }

                # Stream response
                response_text = ""
                async for agent_id, token in self.stream_response(
                    speaker_id, messages, turn
                ):
                    response_text += token
                    yield {"type": "token", "agent_id": agent_id, "content": token}

                # Track response for persona consistency (Phase 3)
                if self.enable_persona_consistency:
                    self.agent_responses[speaker_id].append(response_text)

                # Add to messages with agent name
                agent_name = self.agents[speaker_id].name
                messages.append(AIMessage(content=response_text, name=agent_name))

                yield {
                    "type": "agent_done",
                    "agent_id": speaker_id,
                    "content": response_text,
                    "turn": turn,
                }

                # Simulate reading time for other agents to process this message
                # This creates realistic pacing in the conversation
                reading_delay = int((response_text.count(" ") / 5.0)*1.1)  # 5 words per second + understanding time
                yield {
                    "type": "reading_delay",
                    "delay": reading_delay,
                    "message": f"Agents processing message ({reading_delay:.1f}s)..."
                }
                await asyncio.sleep(reading_delay)

                # Allow human to participate by temporarily enabling input
                # User can stop the orchestration and send their message
                # Or let agents continue for a few more turns
                yield {
                    "type": "wait_for_human",
                    "timeout": 3.0,  # 3 second window
                    "message": "You can stop and send a message..."
                }

                # Brief pause to give human a moment to react
                # They can click stop button during this time
                await asyncio.sleep(3.0)

            # Process memory after each turn (non-blocking)
            if self.enable_memory and self.conversation_id:
                asyncio.create_task(
                    self._process_memory_turn(messages, turn)
                )

            # Evaluate persona consistency periodically (Phase 3)
            if self.enable_persona_consistency and turn > 0 and turn % 10 == 0:
                asyncio.create_task(
                    self._evaluate_persona_consistency(turn)
                )

        # Final processing (memory + persona)
        final_stats = {}

        if self.enable_memory and self.conversation_id:
            memory_stats = await self._final_memory_processing(messages, self.max_turns)
            final_stats["memory"] = memory_stats

        if self.enable_persona_consistency and self.conversation_id:
            quality_metrics = await self._final_quality_evaluation()
            final_stats["quality"] = quality_metrics

        if final_stats:
            yield {"type": "final_stats", "stats": final_stats}

        yield {"type": "done", "total_turns": self.max_turns}

    async def _process_memory_turn(self, messages: list[BaseMessage], turn_number: int):
        """Process memory for current turn (background task)"""
        try:
            # Convert BaseMessage to dict
            messages_dict = [
                {"role": msg.__class__.__name__.replace("Message", "").lower(),
                 "content": msg.content}
                for msg in messages
            ]

            # Process turn (facts, summaries, checkpoints)
            await memory_service.process_conversation_turn(
                self.conversation_id,
                messages_dict,
                turn_number
            )
        except Exception as e:
            print(f"Error processing memory for turn {turn_number}: {e}")

    async def _final_memory_processing(self, messages: list[BaseMessage], turn_number: int) -> dict:
        """Final memory processing at end of conversation"""
        try:
            # Convert messages
            messages_dict = [
                {"role": msg.__class__.__name__.replace("Message", "").lower(),
                 "content": msg.content}
                for msg in messages
            ]

            # Force final summary and checkpoint
            await memory_service.process_conversation_turn(
                self.conversation_id,
                messages_dict,
                turn_number,
                force_summary=True,
                force_checkpoint=True
            )

            # Return stats
            return memory_service.get_memory_stats(self.conversation_id)

        except Exception as e:
            print(f"Error in final memory processing: {e}")
            return {}

    async def _evaluate_persona_consistency(self, turn_number: int):
        """Evaluate persona consistency for all agents (Phase 3)"""
        try:
            messages_dict = []  # Dummy for now, would use actual conversation history

            for agent_id, responses in self.agent_responses.items():
                if len(responses) >= 3:  # Need sufficient responses
                    agent = self.agents[agent_id]
                    await persona_service.evaluate_consistency(
                        agent_id,
                        agent.system_prompt,
                        responses,
                        messages_dict
                    )
        except Exception as e:
            print(f"Error evaluating persona consistency: {e}")

    async def _final_quality_evaluation(self) -> dict:
        """Final quality evaluation at end of conversation (Phase 3)"""
        try:
            # Evaluate diversity
            messages_dict = []  # Would use actual conversation history
            diversity_metrics = await persona_service.evaluate_diversity(
                self.conversation_id,
                self.agent_responses,
                messages_dict
            )

            # Get overall quality metrics
            quality_metrics = await persona_service.get_conversation_quality_metrics(
                self.conversation_id
            )

            # Get improvement suggestions
            suggestions = persona_service.get_improvement_suggestions(
                self.conversation_id
            )

            return {
                **quality_metrics,
                "suggestions": suggestions,
                "diversity": {
                    "response_similarity": diversity_metrics.response_similarity,
                    "topic_diversity": diversity_metrics.topic_diversity,
                    "opinion_diversity": diversity_metrics.opinion_diversity
                }
            }

        except Exception as e:
            print(f"Error in final quality evaluation: {e}")
            return {}
