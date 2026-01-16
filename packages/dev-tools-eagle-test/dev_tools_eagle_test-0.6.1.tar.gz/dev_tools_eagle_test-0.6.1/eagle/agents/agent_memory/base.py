
from typing import List

class AgentMemory:
    """Base class for agent memory implementations."""
    
    def __init__(self):
        """Initialize the agent memory."""
        pass

    def store_memory(self, state, config, node_name: str, step: str = 'start'):

        pass

    def manifest_memory(self, state, config, node_name: str) -> str:
        return ""

class AgentMemoryStack:
    
    def __init__(self):
        self.memories = []

    def add_memories(self, memories: List[AgentMemory]):
        self.memories.extend(memories)

    def store_memories(self, state, config, node_name: str, step: str = 'start'):
        for memory in self.memories:
            memory.store_memory(state, config, node_name, step=step)
        
    def manifest_memories(self, state, config, node_name: str) -> str:
        manifested = []
        for memory in self.memories:
            manifested.append(memory.manifest_memory(state, config, node_name))
        return "\n".join(manifested)