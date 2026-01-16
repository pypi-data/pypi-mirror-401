from eagle.agents.agent_memory.base import AgentMemoryStack
from pydantic import BaseModel, Field

class AgentNodeCognitiveResponse(BaseModel):
    action: str = Field(description="Action to be taken by the agent.")
    message: str = Field(description="Message associated with the action.")


class AgentNodeCognitiveModel:
    """
    Base class for agent cognitive models.
    """

    def __init__(self, agent_memory_stack: AgentMemoryStack = None):
        """Initialize the cognitive model."""
        self._agent_memory_stack = agent_memory_stack

    def think(self, state, config, node_name: str) -> AgentNodeCognitiveResponse:
        """
        Generate thoughts based on the current state, configuration, and node name.

        Args:
            state: The current state of the agent.
            config: The configuration settings for the agent.
            node_name (str): The name of the current node.

        Returns:
            AgentNodeCognitiveResponse: The generated response.
        """
        return AgentNodeCognitiveResponse(action="none", message="")