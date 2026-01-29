"""
Memory Capability - Access to Memory Guild via CNS Bus.

Provides a typed interface to all Memory Guild intents organized by namespace:
- Episodic: Personal experiences and events
- Semantic: Facts and knowledge
- Procedural: Skills and procedures
- Self: Identity and preferences
- Working: Current goals and context
- Cognitive: Context building and integration
- Conversation: Dialogue history
- Goals: Goal management
- Social: Collaboration and messaging
- Perceptual: Sensory data storage
- Batch: Bulk operations
- Admin: Administrative operations
"""

from typing import Any, Dict, List, Optional
from .cns_client import CNSClient


class MemoryCapability:
    """
    Unified interface to Memory Guild via CNS Bus.

    Example:
        cns = CNSClient()
        memory = MemoryCapability(cns)

        # Remember something
        await memory.episodic.remember("Learned about FCA today")

        # Query knowledge
        results = await memory.semantic.query("FCA architecture")

        # Set current goal
        await memory.working.set_goal("Implement cache organ")

        # Build context for LLM
        context = await memory.cognitive.build_context("cache implementation")
    """

    def __init__(self, cns: CNSClient):
        """
        Initialize Memory Capability.

        Args:
            cns: CNSClient instance for dispatching intents
        """
        self.cns = cns
        self.episodic = EpisodicMemory(cns)
        self.semantic = SemanticMemory(cns)
        self.procedural = ProceduralMemory(cns)
        self.self_memory = SelfMemory(cns)
        self.working = WorkingMemory(cns)
        self.cognitive = CognitiveMemory(cns)
        self.conversation = ConversationMemory(cns)
        self.goals = GoalsMemory(cns)
        self.social = SocialMemory(cns)
        self.perceptual = PerceptualMemory(cns)
        self.batch = BatchMemory(cns)

    # Convenience methods that delegate to namespaces
    async def remember(self, content: str, tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """Convenience: Remember in episodic memory."""
        return await self.episodic.remember(content, tags)

    async def query(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Convenience: Query semantic memory."""
        return await self.semantic.query(query, limit)

    async def set_goal(self, goal: str, goal_type: str = "task") -> Dict[str, Any]:
        """Convenience: Set current goal in working memory."""
        return await self.working.set_goal(goal, goal_type)

    async def build_context(
        self,
        query: str,
        include: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Convenience: Build context from multiple memory types."""
        return await self.cognitive.build_context(query, include)


class EpisodicMemory:
    """Episodic memory - personal experiences and events."""

    def __init__(self, cns: CNSClient):
        self.cns = cns

    async def remember(
        self,
        content: str,
        tags: Optional[List[str]] = None,
        importance: float = 0.5,
    ) -> Dict[str, Any]:
        """Store an episodic memory."""
        return await self.cns.dispatch(
            "vy.memory.episodic.remember.v1",
            {"content": content, "tags": tags or [], "importance": importance},
        )

    async def recall(
        self,
        query: str,
        limit: int = 10,
        time_range: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Recall episodic memories matching query."""
        payload = {"query": query, "limit": limit}
        if time_range:
            payload["time_range"] = time_range
        return await self.cns.dispatch("vy.memory.episodic.recall.v1", payload)

    async def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """Search episodic memories with filters."""
        payload = {"query": query, "limit": limit}
        if filters:
            payload["filters"] = filters
        return await self.cns.dispatch("vy.memory.episodic.search.v1", payload)

    async def forget(self, memory_id: str) -> Dict[str, Any]:
        """Remove an episodic memory."""
        return await self.cns.dispatch(
            "vy.memory.episodic.forget.v1",
            {"memory_id": memory_id},
        )


class SemanticMemory:
    """Semantic memory - facts and knowledge."""

    def __init__(self, cns: CNSClient):
        self.cns = cns

    async def store(
        self,
        content: str,
        category: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Store semantic knowledge."""
        payload = {"content": content}
        if category:
            payload["category"] = category
        if metadata:
            payload["metadata"] = metadata
        return await self.cns.dispatch("vy.memory.semantic.store.v1", payload)

    async def query(
        self,
        query: str,
        limit: int = 10,
        categories: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Query semantic knowledge."""
        payload = {"query": query, "limit": limit}
        if categories:
            payload["categories"] = categories
        return await self.cns.dispatch("vy.memory.semantic.query.v1", payload)

    async def get_related(
        self,
        concept: str,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """Get related concepts."""
        return await self.cns.dispatch(
            "vy.memory.semantic.get_related.v1",
            {"concept": concept, "limit": limit},
        )

    async def get_categories(self) -> Dict[str, Any]:
        """List all semantic categories."""
        return await self.cns.dispatch("vy.memory.semantic.get_categories.v1", {})


class ProceduralMemory:
    """Procedural memory - skills and procedures."""

    def __init__(self, cns: CNSClient):
        self.cns = cns

    async def store_skill(
        self,
        skill_name: str,
        steps: List[str],
        category: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Store a skill/procedure."""
        payload = {"skill_name": skill_name, "steps": steps}
        if category:
            payload["category"] = category
        return await self.cns.dispatch("vy.memory.procedural.store_skill.v1", payload)

    async def get_procedures(
        self,
        query: str,
        limit: int = 5,
    ) -> Dict[str, Any]:
        """Get procedures matching query."""
        return await self.cns.dispatch(
            "vy.memory.procedural.get_procedures.v1",
            {"query": query, "limit": limit},
        )

    async def get_skills(
        self,
        category: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List all skills, optionally filtered by category."""
        payload = {}
        if category:
            payload["category"] = category
        return await self.cns.dispatch("vy.memory.procedural.get_skills.v1", payload)


class SelfMemory:
    """Self memory - identity and preferences."""

    def __init__(self, cns: CNSClient):
        self.cns = cns

    async def remember(
        self,
        content: str,
        aspect: str = "general",
    ) -> Dict[str, Any]:
        """Store self-related memory."""
        return await self.cns.dispatch(
            "vy.memory.self.remember.v1",
            {"content": content, "aspect": aspect},
        )

    async def remember_identity(
        self,
        trait: str,
        value: str,
    ) -> Dict[str, Any]:
        """Store identity trait."""
        return await self.cns.dispatch(
            "vy.memory.self.remember_identity.v1",
            {"trait": trait, "value": value},
        )

    async def remember_preference(
        self,
        preference: str,
        value: Any,
    ) -> Dict[str, Any]:
        """Store a preference."""
        return await self.cns.dispatch(
            "vy.memory.self.remember_preference.v1",
            {"preference": preference, "value": value},
        )

    async def remember_relationship(
        self,
        entity: str,
        relationship_type: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Store relationship information."""
        payload = {"entity": entity, "relationship_type": relationship_type}
        if details:
            payload["details"] = details
        return await self.cns.dispatch(
            "vy.memory.self.remember_relationship.v1",
            payload,
        )

    async def get_preferences(
        self,
        category: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get preferences."""
        payload = {}
        if category:
            payload["category"] = category
        return await self.cns.dispatch("vy.memory.self.get_preferences.v1", payload)

    async def get_context(self) -> Dict[str, Any]:
        """Get self context."""
        return await self.cns.dispatch("vy.memory.self.get_context.v1", {})


class WorkingMemory:
    """Working memory - current goals and context."""

    def __init__(self, cns: CNSClient):
        self.cns = cns

    async def set_goal(
        self,
        goal: str,
        goal_type: str = "task",
        priority: int = 5,
    ) -> Dict[str, Any]:
        """Set current goal."""
        return await self.cns.dispatch(
            "vy.memory.working.set_goal.v1",
            {"goal": goal, "goal_type": goal_type, "priority": priority},
        )

    async def update_compass(
        self,
        direction: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Update cognitive compass."""
        payload = {"direction": direction}
        if context:
            payload["context"] = context
        return await self.cns.dispatch("vy.memory.working.update_compass.v1", payload)

    async def update_state(
        self,
        state: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Update working state."""
        return await self.cns.dispatch(
            "vy.memory.working.update_state.v1",
            {"state": state},
        )

    async def flow_buffer_add(
        self,
        item: str,
        item_type: str = "thought",
    ) -> Dict[str, Any]:
        """Add item to flow buffer."""
        return await self.cns.dispatch(
            "vy.memory.working.flow_buffer.add.v1",
            {"item": item, "item_type": item_type},
        )

    async def flow_buffer_clear(self) -> Dict[str, Any]:
        """Clear flow buffer."""
        return await self.cns.dispatch("vy.memory.working.flow_buffer.clear.v1", {})

    async def get_current(self) -> Dict[str, Any]:
        """Get current working memory state."""
        return await self.cns.dispatch("vy.memory.working.get_current.v1", {})


class CognitiveMemory:
    """Cognitive memory - context building and integration."""

    def __init__(self, cns: CNSClient):
        self.cns = cns

    async def build_context(
        self,
        query: str,
        include: Optional[List[str]] = None,
        max_tokens: int = 4000,
    ) -> Dict[str, Any]:
        """
        Build integrated context from multiple memory types.

        Args:
            query: Query to build context for
            include: Memory types to include (episodic, semantic, working, etc.)
            max_tokens: Maximum tokens in context

        Returns:
            Integrated context from specified memory types
        """
        payload = {
            "query": query,
            "include": include or ["semantic", "episodic", "working"],
            "max_tokens": max_tokens,
        }
        return await self.cns.dispatch("vy.memory.cognitive.build.v1", payload)

    async def integrate(
        self,
        memories: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Integrate multiple memories into coherent context."""
        return await self.cns.dispatch(
            "vy.memory.cognitive.integrate.v1",
            {"memories": memories},
        )


class ConversationMemory:
    """Conversation memory - dialogue history."""

    def __init__(self, cns: CNSClient):
        self.cns = cns

    async def remember(
        self,
        role: str,
        content: str,
        conversation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Store conversation message."""
        payload = {"role": role, "content": content}
        if conversation_id:
            payload["conversation_id"] = conversation_id
        return await self.cns.dispatch("vy.memory.conversation.remember.v1", payload)

    async def get_history(
        self,
        conversation_id: str,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Get conversation history."""
        return await self.cns.dispatch(
            "vy.memory.conversation.get_history.v1",
            {"conversation_id": conversation_id, "limit": limit},
        )

    async def summarize(
        self,
        conversation_id: str,
    ) -> Dict[str, Any]:
        """Summarize conversation."""
        return await self.cns.dispatch(
            "vy.memory.conversation.summarize.v1",
            {"conversation_id": conversation_id},
        )


class GoalsMemory:
    """Goals memory - goal management."""

    def __init__(self, cns: CNSClient):
        self.cns = cns

    async def create(
        self,
        goal: str,
        goal_type: str = "task",
        priority: int = 5,
        parent_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new goal."""
        payload = {"goal": goal, "goal_type": goal_type, "priority": priority}
        if parent_id:
            payload["parent_id"] = parent_id
        return await self.cns.dispatch("vy.memory.goals.create.v1", payload)

    async def update(
        self,
        goal_id: str,
        status: Optional[str] = None,
        progress: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Update goal status/progress."""
        payload = {"goal_id": goal_id}
        if status:
            payload["status"] = status
        if progress is not None:
            payload["progress"] = progress
        return await self.cns.dispatch("vy.memory.goals.update.v1", payload)

    async def complete(self, goal_id: str) -> Dict[str, Any]:
        """Mark goal as completed."""
        return await self.cns.dispatch(
            "vy.memory.goals.complete.v1",
            {"goal_id": goal_id},
        )

    async def get(self, goal_id: str) -> Dict[str, Any]:
        """Get goal by ID."""
        return await self.cns.dispatch(
            "vy.memory.goals.get.v1",
            {"goal_id": goal_id},
        )

    async def list_active(self) -> Dict[str, Any]:
        """List active goals."""
        return await self.cns.dispatch("vy.memory.goals.list_active.v1", {})


class SocialMemory:
    """Social memory - collaboration and messaging."""

    def __init__(self, cns: CNSClient):
        self.cns = cns

    async def send_message(
        self,
        recipient: str,
        content: str,
        message_type: str = "text",
    ) -> Dict[str, Any]:
        """Send a message."""
        return await self.cns.dispatch(
            "vy.memory.social.send_message.v1",
            {"recipient": recipient, "content": content, "message_type": message_type},
        )

    async def get_inbox(
        self,
        limit: int = 50,
        unread_only: bool = False,
    ) -> Dict[str, Any]:
        """Get inbox messages."""
        return await self.cns.dispatch(
            "vy.memory.social.get_inbox.v1",
            {"limit": limit, "unread_only": unread_only},
        )

    async def get_collaborations(self) -> Dict[str, Any]:
        """Get active collaborations."""
        return await self.cns.dispatch("vy.memory.social.get_collaborations.v1", {})


class PerceptualMemory:
    """Perceptual memory - sensory data storage."""

    def __init__(self, cns: CNSClient):
        self.cns = cns

    async def store(
        self,
        data: Dict[str, Any],
        modality: str = "visual",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Store perceptual data."""
        payload = {"data": data, "modality": modality}
        if metadata:
            payload["metadata"] = metadata
        return await self.cns.dispatch("vy.memory.perceptual.store.v1", payload)

    async def query(
        self,
        query: str,
        modality: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """Query perceptual data."""
        payload = {"query": query, "limit": limit}
        if modality:
            payload["modality"] = modality
        return await self.cns.dispatch("vy.memory.perceptual.query.v1", payload)

    async def get(self, perception_id: str) -> Dict[str, Any]:
        """Get perceptual data by ID."""
        return await self.cns.dispatch(
            "vy.memory.perceptual.get.v1",
            {"perception_id": perception_id},
        )

    async def find_similar(
        self,
        data: Dict[str, Any],
        limit: int = 5,
    ) -> Dict[str, Any]:
        """Find similar perceptual data."""
        return await self.cns.dispatch(
            "vy.memory.perceptual.find_similar.v1",
            {"data": data, "limit": limit},
        )


class BatchMemory:
    """Batch operations for memory."""

    def __init__(self, cns: CNSClient):
        self.cns = cns

    async def store(
        self,
        items: List[Dict[str, Any]],
        memory_type: str = "episodic",
    ) -> Dict[str, Any]:
        """Batch store memories."""
        return await self.cns.dispatch(
            "vy.memory.batch.store.v1",
            {"items": items, "memory_type": memory_type},
        )

    async def retrieve(
        self,
        ids: List[str],
        memory_type: str = "episodic",
    ) -> Dict[str, Any]:
        """Batch retrieve memories."""
        return await self.cns.dispatch(
            "vy.memory.batch.retrieve.v1",
            {"ids": ids, "memory_type": memory_type},
        )

    async def delete(
        self,
        ids: List[str],
        memory_type: str = "episodic",
    ) -> Dict[str, Any]:
        """Batch delete memories."""
        return await self.cns.dispatch(
            "vy.memory.batch.delete.v1",
            {"ids": ids, "memory_type": memory_type},
        )

    async def update(
        self,
        updates: List[Dict[str, Any]],
        memory_type: str = "episodic",
    ) -> Dict[str, Any]:
        """Batch update memories."""
        return await self.cns.dispatch(
            "vy.memory.batch.update.v1",
            {"updates": updates, "memory_type": memory_type},
        )
