"""
Chat router - optimized with parallel processing and caching
"""

import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from aidiscuss.app.db.base import get_db
from aidiscuss.app.models.agent import Agent
from aidiscuss.app.models.provider import Provider
from aidiscuss.app.models.provider_key import ProviderKey
from aidiscuss.app.models.conversation import Conversation, Message
from aidiscuss.app.services.orchestrator_parallel import ParallelOrchestratorService
from aidiscuss.app.services.cache import cache
from aidiscuss.app.services.rag_service import rag_service
from aidiscuss.app.services.analytics_service import analytics_service, TokenUsage
from nanoid import generate
from datetime import datetime

router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message model"""

    role: str
    content: str
    agent_id: str | None = None


class ChatRequest(BaseModel):
    """Chat request model"""

    message: str
    agent_ids: list[str]
    conversation_id: str | None = None
    orchestration_strategy: str = "round-robin"
    max_turns: int = 3  # Reduced to allow human participation between turns
    use_rag: bool = False
    rag_namespace: str = "default"
    rag_k: int = 3


class ChatResponse(BaseModel):
    """Chat response model"""

    conversation_id: str
    messages: list[ChatMessage]


async def _get_agents_and_providers(
    agent_ids: list[str], db: AsyncSession
) -> tuple[list[Agent], dict[str, Provider]]:
    """
    Optimized helper to get agents and providers with caching

    Returns:
        Tuple of (agents, providers_dict)
    """
    # Try to get from cache first
    cached_agents = []
    missing_agent_ids = []

    for agent_id in agent_ids:
        cached = cache.get_agent(agent_id)
        if cached:
            cached_agents.append(cached)
        else:
            missing_agent_ids.append(agent_id)

    # Fetch missing agents from database
    if missing_agent_ids:
        result = await db.execute(
            select(Agent).where(Agent.id.in_(missing_agent_ids))
        )
        db_agents = list(result.scalars().all())

        # Cache them
        for agent in db_agents:
            cache.set_agent(agent)

        cached_agents.extend(db_agents)

    agents = cached_agents

    if len(agents) != len(agent_ids):
        raise HTTPException(status_code=400, detail="Some agents not found")

    # Get providers with their API keys (with caching)
    provider_ids = list(set(agent.provider_id for agent in agents))
    providers = {}

    for provider_id in provider_ids:
        cached = cache.get_provider(provider_id)
        if cached:
            providers[provider_id] = cached
        else:
            # Load provider schema
            result = await db.execute(
                select(Provider).where(Provider.id == provider_id)
            )
            provider = result.scalar_one_or_none()
            if not provider:
                continue

            # Load an enabled provider key for this provider
            key_result = await db.execute(
                select(ProviderKey)
                .where(ProviderKey.provider == provider_id)
                .where(ProviderKey.enabled == True)
                .limit(1)
            )
            provider_key = key_result.scalar_one_or_none()

            if provider_key:
                # Attach decrypted API key to provider
                provider.api_key_encrypted = provider_key.get_decrypted_key()

            cache.set_provider(provider)
            providers[provider_id] = provider

    return agents, providers


@router.post("/send", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Send a chat message with optimized parallel processing
    """
    # Get agents and providers (with caching)
    agents, providers = await _get_agents_and_providers(request.agent_ids, db)

    # Verify all providers exist and have API keys
    for agent in agents:
        if agent.provider_id not in providers:
            raise HTTPException(
                status_code=400,
                detail=f"Provider '{agent.provider_id}' not found for agent '{agent.id}'",
            )
        if not providers[agent.provider_id].get_api_key():
            raise HTTPException(
                status_code=400,
                detail=f"No API key set for provider '{agent.provider_id}'",
            )

    # Create or get conversation
    conversation_id = request.conversation_id or generate(size=12)
    if not request.conversation_id:
        conversation = Conversation(
            id=conversation_id,
            title="New Conversation",
            orchestration_strategy=request.orchestration_strategy,
            agent_ids=request.agent_ids,
        )
        db.add(conversation)
        await db.commit()

    # Retrieve RAG context if enabled
    rag_context = None
    if request.use_rag:
        results = rag_service.search(
            query=request.message,
            namespace=request.rag_namespace,
            k=request.rag_k,
            min_score=0.7,
        )
        if results:
            rag_context = "\n\n".join(
                [f"Source: {r['metadata'].get('source', 'Unknown')}\n{r['content']}" for r in results]
            )

    # Create optimized orchestrator with parallel support, memory, and persona consistency
    orchestrator = ParallelOrchestratorService(
        agents=agents,
        providers=providers,
        orchestration_strategy=request.orchestration_strategy,
        max_turns=request.max_turns,
        enable_parallel=True,  # Enable parallel processing
        rag_context=rag_context,  # Inject RAG context
        conversation_id=conversation_id,  # Enable memory tracking
        enable_memory=True,  # Phase 2: Memory Enhancement
        enable_persona_consistency=True,  # Phase 3: Persona Consistency
        enable_tools=True,  # Phase 4: Tool Use
    )

    # Run conversation and collect messages
    response_messages = [ChatMessage(role="user", content=request.message)]

    # Collect messages for batch insert
    messages_to_insert = []
    turn_number = 0
    start_time = datetime.now()

    async for event in orchestrator.run_conversation(request.message):
        if event["type"] == "agent_done":
            # Prepare message for batch insert
            message = Message(
                id=generate(size=12),
                conversation_id=conversation_id,
                role="assistant",
                content=event["content"],
                agent_id=event["agent_id"],
                turn_number=turn_number,
            )
            messages_to_insert.append(message)

            # Track analytics for this agent response
            agent = next((a for a in agents if a.id == event["agent_id"]), None)
            if agent:
                # Estimate token usage (rough approximation: 4 chars per token)
                prompt_tokens = len(request.message) // 4
                completion_tokens = len(event["content"]) // 4
                total_tokens = prompt_tokens + completion_tokens

                latency_ms = (datetime.now() - start_time).total_seconds() * 1000

                analytics_service.track_api_call(
                    conversation_id=conversation_id,
                    agent_id=event["agent_id"],
                    provider_id=agent.provider_id,
                    model=agent.model,
                    tokens=TokenUsage(
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens,
                        total_tokens=total_tokens
                    ),
                    latency_ms=latency_ms,
                    success=True
                )

            turn_number += 1

            response_messages.append(
                ChatMessage(
                    role="assistant",
                    content=event["content"],
                    agent_id=event["agent_id"],
                )
            )

    # Batch insert messages (more efficient)
    if messages_to_insert:
        db.add_all(messages_to_insert)

    # Commit in background
    async def _commit():
        await db.commit()

    background_tasks.add_task(_commit)

    return ChatResponse(conversation_id=conversation_id, messages=response_messages)


@router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for streaming chat responses with real LangChain integration
    """
    await websocket.accept()

    try:
        # Receive initial request
        data = await websocket.receive_json()

        message = data.get("message", "")
        agent_ids = data.get("agent_ids", [])
        orchestration_strategy = data.get("orchestration_strategy", "round-robin")
        max_turns = data.get("max_turns", 3)  # Reduced to allow human participation
        use_rag = data.get("use_rag", False)
        rag_namespace = data.get("rag_namespace", "default")
        rag_k = data.get("rag_k", 3)

        # Get database session
        async with AsyncSessionLocal() as db:
            # Get agents and providers with caching
            try:
                agents, providers = await _get_agents_and_providers(agent_ids, db)
            except HTTPException as e:
                await websocket.send_json({
                    "type": "error",
                    "error": e.detail
                })
                await websocket.close()
                return

            # Verify providers have API keys
            for agent in agents:
                if agent.provider_id not in providers:
                    await websocket.send_json({
                        "type": "error",
                        "error": f"Provider '{agent.provider_id}' not found"
                    })
                    await websocket.close()
                    return

                if not providers[agent.provider_id].get_api_key():
                    await websocket.send_json({
                        "type": "error",
                        "error": f"No API key set for provider '{agent.provider_id}'"
                    })
                    await websocket.close()
                    return

            # Create or get conversation
            conversation_id = data.get("conversation_id") or generate(size=12)
            if not data.get("conversation_id"):
                conversation = Conversation(
                    id=conversation_id,
                    title="New Conversation",
                    orchestration_strategy=orchestration_strategy,
                    agent_ids=agent_ids,
                )
                db.add(conversation)
                await db.commit()

            # Retrieve RAG context if enabled
            rag_context = None
            if use_rag:
                results = rag_service.search(
                    query=message,
                    namespace=rag_namespace,
                    k=rag_k,
                    min_score=0.7,
                )
                if results:
                    rag_context = "\n\n".join(
                        [f"Source: {r['metadata'].get('source', 'Unknown')}\n{r['content']}" for r in results]
                    )

            # Create optimized orchestrator with memory and persona consistency
            try:
                orchestrator = ParallelOrchestratorService(
                    agents=agents,
                    providers=providers,
                    orchestration_strategy=orchestration_strategy,
                    max_turns=max_turns,
                    enable_parallel=True,  # Enable parallel processing
                    rag_context=rag_context,  # Inject RAG context
                    conversation_id=conversation_id,  # Enable memory tracking
                    enable_memory=True,  # Phase 2: Memory Enhancement
                    enable_persona_consistency=True,  # Phase 3: Persona Consistency
                    enable_tools=True,  # Phase 4: Tool Use
                )
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "error": f"Failed to create orchestrator: {str(e)}"
                })
                await websocket.close()
                return

            # Stream conversation with parallel support
            messages_to_insert = []
            turn_number = 0
            start_time = datetime.now()

            async for event in orchestrator.run_conversation(message):
                # Send event to client
                await websocket.send_json(event)

                # Collect agent responses for database storage
                if event.get("type") == "agent_done":
                    msg = Message(
                        id=generate(size=12),
                        conversation_id=conversation_id,
                        role="assistant",
                        content=event.get("content", ""),
                        agent_id=event.get("agent_id"),
                        turn_number=turn_number,
                    )
                    messages_to_insert.append(msg)

                    # Track analytics for this agent response
                    agent = next((a for a in agents if a.id == event.get("agent_id")), None)
                    if agent:
                        # Estimate token usage
                        prompt_tokens = len(message) // 4
                        completion_tokens = len(event.get("content", "")) // 4
                        total_tokens = prompt_tokens + completion_tokens

                        latency_ms = (datetime.now() - start_time).total_seconds() * 1000

                        analytics_service.track_api_call(
                            conversation_id=conversation_id,
                            agent_id=event.get("agent_id"),
                            provider_id=agent.provider_id,
                            model=agent.model,
                            tokens=TokenUsage(
                                prompt_tokens=prompt_tokens,
                                completion_tokens=completion_tokens,
                                total_tokens=total_tokens
                            ),
                            latency_ms=latency_ms,
                            success=True
                        )

                    turn_number += 1

            # Batch insert messages
            if messages_to_insert:
                db.add_all(messages_to_insert)
                await db.commit()

            # Send completion signal
            await websocket.send_json({"type": "complete"})

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "error": str(e)
            })
        except (WebSocketDisconnect, RuntimeError) as send_error:
            print(f"Could not send error message to websocket: {send_error}")
        try:
            await websocket.close()
        except (WebSocketDisconnect, RuntimeError) as close_error:
            print(f"Could not close websocket: {close_error}")


# Import AsyncSessionLocal for WebSocket handler
from aidiscuss.app.db.base import AsyncSessionLocal
