"""
Broadcast service for WebSocket-based real-time synchronization
Manages WebSocket connections and broadcasts data changes to all connected clients
"""

import json
from typing import Set, Any
from fastapi import WebSocket


class BroadcastService:
    """
    Manages WebSocket connections and broadcasts events to all connected clients
    Used for real-time synchronization across browser tabs and different browsers
    """

    def __init__(self):
        self.connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        """Register new WebSocket connection"""
        await websocket.accept()
        self.connections.add(websocket)
        print(f"[BroadcastService] Client connected. Total connections: {len(self.connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        self.connections.discard(websocket)
        print(f"[BroadcastService] Client disconnected. Total connections: {len(self.connections)}")

    async def broadcast(self, event_type: str, data: dict[str, Any]):
        """
        Broadcast event to all connected clients
        Automatically removes dead connections
        """
        if not self.connections:
            return  # No clients connected

        message = json.dumps({"type": event_type, **data})
        dead_connections = set()

        for connection in self.connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"[BroadcastService] Failed to send to client: {e}")
                dead_connections.add(connection)

        # Clean up dead connections
        if dead_connections:
            self.connections -= dead_connections
            print(f"[BroadcastService] Removed {len(dead_connections)} dead connections")

    # Agent events
    async def broadcast_agent_created(self, agent: dict[str, Any]):
        """Broadcast agent creation to all clients"""
        await self.broadcast("agent:created", {"agent": agent})

    async def broadcast_agent_updated(self, agent: dict[str, Any]):
        """Broadcast agent update to all clients"""
        await self.broadcast("agent:updated", {"agent": agent})

    async def broadcast_agent_deleted(self, agent_id: str):
        """Broadcast agent deletion to all clients"""
        await self.broadcast("agent:deleted", {"agentId": agent_id})

    # Provider events
    async def broadcast_provider_created(self, provider: dict[str, Any]):
        """Broadcast provider creation to all clients"""
        await self.broadcast("provider:created", {"provider": provider})

    async def broadcast_provider_updated(self, provider: dict[str, Any]):
        """Broadcast provider update to all clients"""
        await self.broadcast("provider:updated", {"provider": provider})

    async def broadcast_provider_deleted(self, provider_id: str):
        """Broadcast provider deletion to all clients"""
        await self.broadcast("provider:deleted", {"providerId": provider_id})

    # Conversation events
    async def broadcast_conversation_created(self, conversation: dict[str, Any]):
        """Broadcast conversation creation to all clients"""
        await self.broadcast("conversation:created", {"conversation": conversation})

    async def broadcast_conversation_updated(self, conversation: dict[str, Any]):
        """Broadcast conversation update to all clients"""
        await self.broadcast("conversation:updated", {"conversation": conversation})

    async def broadcast_conversation_deleted(self, conversation_id: str):
        """Broadcast conversation deletion to all clients"""
        await self.broadcast("conversation:deleted", {"conversationId": conversation_id})

    # Message events
    async def broadcast_message_added(self, conversation_id: str, message: dict[str, Any]):
        """Broadcast message addition to all clients"""
        await self.broadcast("message:added", {"conversationId": conversation_id, "message": message})

    async def broadcast_message_updated(self, conversation_id: str, message: dict[str, Any]):
        """Broadcast message update to all clients"""
        await self.broadcast("message:updated", {"conversationId": conversation_id, "message": message})

    async def broadcast_message_deleted(self, conversation_id: str, message_id: str):
        """Broadcast message deletion to all clients"""
        await self.broadcast("message:deleted", {"conversationId": conversation_id, "messageId": message_id})

    # Settings events
    async def broadcast_settings_updated(self, settings: dict[str, Any]):
        """Broadcast settings update to all clients"""
        await self.broadcast("settings:updated", {"settings": settings})

    # Memory events
    async def broadcast_memory_updated(self, conversation_id: str, memory: dict[str, Any]):
        """Broadcast memory update to all clients"""
        await self.broadcast("memory:updated", {"conversationId": conversation_id, "memory": memory})

    # Provider Key events
    async def broadcast_provider_key_created(self, key: dict[str, Any]):
        """Broadcast provider key creation to all clients"""
        await self.broadcast("provider_key:created", {"key": key})

    async def broadcast_provider_key_updated(self, key: dict[str, Any]):
        """Broadcast provider key update to all clients"""
        await self.broadcast("provider_key:updated", {"key": key})

    async def broadcast_provider_key_deleted(self, key_id: str):
        """Broadcast provider key deletion to all clients"""
        await self.broadcast("provider_key:deleted", {"keyId": key_id})


# Global singleton instance
broadcast_service = BroadcastService()
