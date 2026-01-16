from eagle.agents.base import (
    BasicAgent,
    BasicAgentConfigSchema,
    BasicWorkingMemoryState,
    basic_route_after_observe,
    basic_route_after_plan,
    basic_route_after_execute
)
from eagle.agents.agent_memory.base import AgentMemoryStack
from eagle.agents.cognitive_models.react.react_model import ReactNodeCognitiveModel
from eagle.utils.message_enrichment_utils import set_now_time_to_string
from langchain_core.language_models.chat_models  import BaseChatModel
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage
from langchain_core.tools import BaseTool
from typing import List, Optional
from pydantic import Field, field_validator, BaseModel

# Auxiliar functions
def node_path_count(state, node_from: str, node_to: str):

    if not node_from:
        return state
    
    state.other_registers["node_paths_counter"][f"{node_from}_{node_to}"] += 1

    return state

def node_path_count_reached_the_limit(state, config):
    max_node_paths_count = config.get("configurable").get("max_node_paths_count")
    node_path_counter = state.other_registers.get("node_paths_counter")
    for path, max_count in max_node_paths_count.items():
        if max_count is not None:
            if node_path_counter[path] >= max_count:
                return True
    return False

# Callback managers
# Agent's state callback manager
class ReactAgentStateCallbackManager:

    def __init__(self):
        self.callbacks = {
            "on_observe_node_start": [],
            "on_observe_node_end": [],
            "on_plan_node_start": [],
            "on_plan_node_end": [],
            "on_execute_node_start": [],
            "on_execute_node_end": []
        }

    def register_callback(self, event_type, callback_fn):
        """Permite registrar callbacks adicionais antes de rodar o app."""
        self.callbacks[event_type].append(callback_fn)

    def on_observe_node_start(self, state, config):
        for callback in self.callbacks["on_observe_node_start"]:
            callback(state, config)

    def on_observe_node_end(self, state, config):
        for callback in self.callbacks["on_observe_node_end"]:
            callback(state, config)

    def on_plan_node_start(self, state, config):
        for callback in self.callbacks["on_plan_node_start"]:
            callback(state, config)

    def on_plan_node_end(self, state, config):
        for callback in self.callbacks["on_plan_node_end"]:
            callback(state, config)

    def on_execute_node_start(self, state, config):
        for callback in self.callbacks["on_execute_node_start"]:
            callback(state, config)

    def on_execute_node_end(self, state, config):
        for callback in self.callbacks["on_execute_node_end"]:
            callback(state, config)

# Config schemas
class MaxNodePathsCountSchema(BaseModel):
    observe_node_plan_node: Optional[int] = Field( default=None, description="Max paths from observe to plan node.")
    observe_node_execute_node: Optional[int] = Field(default=None, description="Max paths from observe to execute node.")
    plan_node_execute_node: Optional[int] = Field(default=None, description="Max paths from plan to execute node.")
    plan_node_observe_node: Optional[int] = Field(default=2, description="Max paths from plan to observe node.")
    execute_node_observe_node: Optional[int] = Field(default=2, description="Max paths from execute to observe node.")
    execute_node_plan_node: Optional[int] = Field(default=2, description="Max paths from execute to plan node.")

class ReactPlanningAgentConfigSchema(BasicAgentConfigSchema):
    chat_history_window_size: int = Field(default=5, description="Size of the chat history window.")
    observe_tools: List[BaseTool] = Field(default_factory=list, description="List of tools for the observe node.")
    plan_tools: List[BaseTool] = Field(default_factory=list, description="List of tools for the planning node.")
    execute_tools: List[BaseTool] = Field(default_factory=list, description="List of tools for the executing node.")
    observe_important_guidelines: str = Field(default="", description="Important guidelines for the observe node.")
    plan_important_guidelines: str = Field(default="", description="Important guidelines for the plan node.")
    execute_important_guidelines: str = Field(default="", description="Important guidelines for the execute node.")
    observe_node_llm: Optional[BaseChatModel] = Field(default=None, description="Pre-instantiated LLM for the observe node.")
    observe_node_llm_prompt_language: str = Field(default="pt-br", description="Prompt language for the observe node.")
    observe_node_has_vision: bool = Field(default=False, description="Whether the observe node has vision capabilities.")
    observe_node_llm_use_structured_output: bool = Field(default=False, description="Whether to use structured output for the observe node.")
    plan_node_llm: Optional[BaseChatModel] = Field(default=None, description="Pre-instantiated LLM for the plan node.")
    plan_node_llm_prompt_language: str = Field(default="pt-br", description="Prompt language for the plan node.")
    plan_node_has_vision: bool = Field(default=False, description="Whether the plan node has vision capabilities.")
    plan_node_llm_use_structured_output: bool = Field(default=False, description="Whether to use structured output for the plan node.")
    execute_node_llm: Optional[BaseChatModel] = Field(default=None, description="Pre-instantiated LLM for the execute node.")
    execute_node_llm_prompt_language: str = Field(default="pt-br", description="Prompt language for the execute node.")
    execute_node_has_vision: bool = Field(default=False, description="Whether the execute node has vision capabilities.")
    execute_node_llm_use_structured_output: bool = Field(default=False, description="Whether to use structured output for the execute node.")
    observe_node_callback_manager: ReactAgentStateCallbackManager = Field(
        default=ReactAgentStateCallbackManager(),
        description="Callback manager for the observe node."
    )
    plan_node_callback_manager: ReactAgentStateCallbackManager = Field(
        default=ReactAgentStateCallbackManager(),
        description="Callback manager for the plan node."
    )
    execute_node_callback_manager: ReactAgentStateCallbackManager = Field(
        default=ReactAgentStateCallbackManager(),
        description="Callback manager for the execute node."
    )
    max_node_paths_count: MaxNodePathsCountSchema = Field(default_factory=MaxNodePathsCountSchema, description="Max number of passages from one node to another")

    @field_validator('observe_tools', 'plan_tools', 'execute_tools', mode='before')
    def validate_tool_objects(cls, v):
        if isinstance(v, list) and all(issubclass(type(tool), BaseTool) for tool in v):
            return v
        raise TypeError("All tools must be instances of BaseTool or its subclasses.")

    @field_validator('observe_node_llm', 'plan_node_llm', 'execute_node_llm', mode='before')
    def validate_llm_objects(cls, v):
        if v is None or issubclass(type(v), BaseChatModel):
            return v
        raise TypeError("LLM must be an instance of BaseChatModel or its subclasses.")

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        # Serialize LLM objects to dictionaries
        for field_name in ['observe_node_llm', 'plan_node_llm', 'execute_node_llm']:
            data[field_name] = getattr(self, field_name)
        # Serialize tools to dictionaries
        for field_name in ['observe_tools', 'plan_tools', 'execute_tools']:
            data[field_name] = getattr(self, field_name)
        return data

    class Config:
        arbitrary_types_allowed = True

# State schemas
class ReactPlanningAgentWorkingMemoryState(BasicWorkingMemoryState):
    other_registers: dict = Field(
        default={
            "node_paths_counter": {
                "observe_node_plan_node": 0,
                "observe_node_execute_node": 0,
                "plan_node_observe_node": 0,
                "plan_node_execute_node": 0,
                "execute_node_observe_node": 0,
                "execute_node_plan_node": 0
            }
        }
    )

# Nodes
def observe_node(state: BasicWorkingMemoryState, config: RunnableConfig, store):

    state = node_path_count(state, state.node_from, "observe_node")
    agent_memory_stack: AgentMemoryStack = store.get_memory("agent_memory_stack")

    agent_memory_stack.store_memories(state, config, node_name="observe_node", step="start")

    cognitive_model = ReactNodeCognitiveModel(
        agent_memory_stack=agent_memory_stack
    )

    response = cognitive_model.think(
        state,
        config,
        node_name="observe_node"
    )

    if response.action == "nothing":
        return {
            "node_from": "observe_node",
            "i_need_a_feedback": False,
            "execution_is_complete": True,
            "messages": [AIMessage(content=set_now_time_to_string(response.message), name=config.get("configurable").get("agent_name"))],
            "other_registers": state.other_registers
        }

    elif response.action == "answer":
        return {
            "node_from": "observe_node",
            "i_need_a_feedback": False,
            "execution_is_complete": True,
            "messages": [AIMessage(content=set_now_time_to_string(response.message), name=config.get("configurable").get("agent_name"))],
            "other_registers": state.other_registers
        }

    elif response.action == "think":
        return {
            "node_from": "observe_node",
            "i_need_a_feedback": False,
            "execution_is_complete": False,
            "observation": response.message,
            "other_registers": state.other_registers
        }
    else:
        raise ValueError(f"Invalid action in response: {response.action}")

def plan_node(state: BasicWorkingMemoryState, config: RunnableConfig, store):

    state = node_path_count(state, state.node_from, "plan_node")
    agent_memory_stack: AgentMemoryStack = store.get_memory("agent_memory_stack")

    agent_memory_stack.store_memories(state, config, node_name="plan_node", step="start")

    cognitive_model = ReactNodeCognitiveModel(
        agent_memory_stack=agent_memory_stack
    )

    response = cognitive_model.think(
        state,
        config,
        node_name="plan_node"
    )

    if response.action == "execute":
        return {
            "node_from": "plan_node",
            "i_need_a_feedback": False,
            "execution_is_complete": False,
            "my_plan_is_complete": True,
            "observation": "",
            "plan": response.message,
            "other_registers": state.other_registers
        }

    elif response.action == "nothing":
        return {
            "node_from": "plan_node",
            "i_need_a_feedback": False,
            "execution_is_complete": False,
            "my_plan_is_complete": False,
            "observation": "",
            "plan": response.message,
            "other_registers": state.other_registers
        }
    else:
        raise ValueError(f"Invalid action in response: {response.action}")

def execute_node(state: BasicWorkingMemoryState, config: RunnableConfig, store):
    
    state = node_path_count(state, state.node_from, "execute_node")
    agent_memory_stack: AgentMemoryStack = store.get_memory("agent_memory_stack")
    
    agent_memory_stack.store_memories(state, config, node_name="execute_node", step="start")

    cognitive_model = ReactNodeCognitiveModel(
        agent_memory_stack=agent_memory_stack
    )

    response = cognitive_model.think(
        state,
        config,
        node_name="execute_node"
    )

    if response.action == "success":
        return {
            "node_from": "execute_node",
            "i_need_a_feedback": False,
            "execution_is_complete": True,
            "my_plan_is_complete": False,
            "messages": [AIMessage(content=set_now_time_to_string(response.message), name=config.get("configurable").get("agent_name"))],
            "other_registers": state.other_registers
        }

    elif response.action == "failure":
        if node_path_count_reached_the_limit(state, config):
            return {
                "node_from": "execute_node",
                "i_need_a_feedback": False,
                "execution_is_complete": False,
                "my_plan_is_complete": False,
                "messages": [AIMessage(content=set_now_time_to_string(response.message), name=config.get("configurable").get("agent_name"))],
                "observation": response.message,
                "other_registers": state.other_registers
            }
        else:
            return {
                "node_from": "execute_node",
                "i_need_a_feedback": False,
                "execution_is_complete": False,
                "my_plan_is_complete": False,
                "observation": response.message,
                "other_registers": state.other_registers
            }
    else:
        raise ValueError(f"Invalid action in response: {response.action}")

# Node routers

def route_after_observe(state, config, store):

    # Get the callback manager for the observe node
    observe_node_callback_manager = config.get("configurable").get("observe_node_callback_manager")

    # Get agent memory stack
    agent_memory_stack: AgentMemoryStack = store.get_memory("agent_memory_stack")

    # Route the state and config to the appropriate callback manager
    observe_node_callback_manager.on_observe_node_end(state, config)

    # Store memories at the end of the observe node
    agent_memory_stack.store_memories(state, config, node_name="observe_node", step="end")

    # call the original route function
    return basic_route_after_observe(state, config, store)

def route_after_plan(state, config, store):

    # Get the callback manager for the plan node
    plan_node_callback_manager = config.get("configurable").get("plan_node_callback_manager")

    # Get agent memory stack
    agent_memory_stack: AgentMemoryStack = store.get_memory("agent_memory_stack")

    # Route the state and config to the appropriate callback manager
    plan_node_callback_manager.on_plan_node_end(state, config)

    # Store memories at the end of the plan node
    agent_memory_stack.store_memories(state, config, node_name="plan_node", step="end")

    # checking max node path count 
    if node_path_count_reached_the_limit(state, config):
        return "execute"
    else:
        # call the original route function
        return basic_route_after_plan(state, config, store)

def route_after_execute(state, config, store):

    # Get the callback manager for the execute node
    execute_node_callback_manager = config.get("configurable").get("execute_node_callback_manager")

    # Get agent memory stack
    agent_memory_stack: AgentMemoryStack = store.get_memory("agent_memory_stack")

    # Route the state and config to the appropriate callback manager
    execute_node_callback_manager.on_execute_node_end(state, config)

    # Store memories at the end of the execute node
    agent_memory_stack.store_memories(state, config, node_name="execute_node", step="end")

    # checking max node path count 
    if node_path_count_reached_the_limit(state, config):
        return "end"
    else:
        # call the original route function
        return basic_route_after_execute(state, config, store)
    
# Agent class
class ReactPlanningAgent(BasicAgent):

    AGENT_TYPE = "react_planning_basic"
    OBSERVE_NODE = observe_node
    ROUTE_AFTER_OBSERVE_NODE = route_after_observe
    ROUTE_AFTER_PLAN_NODE = route_after_plan
    ROUTE_AFTER_EXECUTE_NODE = route_after_execute
    PLAN_NODE = plan_node
    EXECUTE_NODE = execute_node
    CONFIG_SCHEMA = ReactPlanningAgentConfigSchema
    WORKING_MEMORY_STATE = ReactPlanningAgentWorkingMemoryState
