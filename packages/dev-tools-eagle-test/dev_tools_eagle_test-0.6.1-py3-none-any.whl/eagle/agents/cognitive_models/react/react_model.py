from eagle.agents.cognitive_models.base import AgentNodeCognitiveModel
from eagle.agents.cognitive_models.react.prompts import prompt_generator
from eagle.utils.agents_utils import extract_node_prefix
from eagle.utils.image_utils import object_to_image_url
from eagle.agents.agent_memory.base import AgentMemoryStack
from eagle.agents.agent_memory.shared_memory.shared_objects_memory import SharedObjectsAgentMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, ToolMessage, BaseMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.graph.message import add_messages
from typing import List, Any, Dict, Optional, Annotated, Sequence
import hashlib

# React special state
class ReactAgentState(AgentState):
    """
    State for the React Planning Agent.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
    observation: str = ""
    plan: str = ""
    tools_interactions: Dict[str, Any] = {}

# Auxiliary functions and classes can be defined here if needed
def process_graph_stream(graph, inputs, config):
    """
    Helper function to process the graph stream and update tool interactions.
    """
            
    tool_calls_by_tool_names = {}
        
    done = False
    while not done:
        for s in graph.stream(inputs, stream_mode="values"):
            messages = s["messages"]
            state_snapshot = graph.get_state(config)
            if isinstance(messages[-1], AIMessage) and len(messages[-1].tool_calls) > 0: 
                for tool_call in messages[-1].tool_calls:
                    inputs["tools_interactions"][tool_call['id']] = {
                        "call": tool_call,
                        "response": None
                    }
            elif isinstance(messages[-1], ToolMessage):
                _messages = [m for m in messages if isinstance(m, ToolMessage)]
                for message in _messages:
                    tool_name = inputs["tools_interactions"][message.tool_call_id]['call']['name']
                    args_hash = hashlib.sha256(str(inputs["tools_interactions"][message.tool_call_id]['call']['args']).encode("utf-8")).hexdigest()
                    response_hash = hashlib.sha256(str(message.content).encode("utf-8")).hexdigest()
                    if tool_name in tool_calls_by_tool_names and args_hash in tool_calls_by_tool_names[tool_name]:
                        if tool_calls_by_tool_names[tool_name][args_hash] != response_hash:
                            inputs["tools_interactions"][message.tool_call_id]['response'] = message.content if message.content != '' else 'Empty response!!'
                    else:
                        inputs["tools_interactions"][message.tool_call_id]['response'] = message.content if message.content != '' else 'Empty response!!'
                    
                    if tool_name not in tool_calls_by_tool_names:
                        tool_calls_by_tool_names[tool_name] = {
                            args_hash: response_hash
                        }
                    else:
                        tool_calls_by_tool_names[tool_name][args_hash] = response_hash
                return inputs, None
        done = isinstance(messages[-1], AIMessage) and (not messages[-1].tool_calls) and messages[-1].content != ''    
    return inputs, messages[-1]

def get_vision_context(
        node_prompt_language,
        node_llm,
        node_prompt_use_structured_output,
        agent_memory_stack: AgentMemoryStack,
        node_name: str,
        state,
        config
    ):

    def _extract_special_memory_stack_for_vision(
            agent_memory_stack: AgentMemoryStack,
            state,
            config,
            node_name: str
        ) -> str:
        """Extract memory context for vision node."""
        if not agent_memory_stack:
            return "", None
        special_memory_stack_for_vision = AgentMemoryStack()
        shared_object_memory = None
        for memory in agent_memory_stack.memories:
            if isinstance(memory, SharedObjectsAgentMemory):
                special_memory_stack_for_vision.add_memories([memory])
                shared_object_memory = memory
                break
        memory_context_for_vision = special_memory_stack_for_vision.manifest_memories(
            state, config, node_name
        )
        return memory_context_for_vision, shared_object_memory

    # reading node prefix
    node_prefix = extract_node_prefix(node_name)
    chat_id = config.get("configurable").get("chat_id")
    important_guidelines = config.get("configurable").get(f"{node_prefix}_important_guidelines")

    prompt_data = prompt_generator.generate_prompt(
        prompt_name="node_vision",
        language=node_prompt_language,
        llm=node_llm,
        use_structured_output=node_prompt_use_structured_output,
    )

    prompt = prompt_data["prompt"]
    output_parser = prompt_data["output_parser"]
    memory_context_for_vision, shared_memory = _extract_special_memory_stack_for_vision(
        agent_memory_stack, state, config, node_name
    )
        
    message = None
    while not isinstance(message, AIMessage):
        graph = create_react_agent(
        model=node_llm,
            prompt=prompt.partial(
                agent_name=config.get("configurable").get("agent_name"),
                agent_description=config.get("configurable").get("agent_description"),
                memory=memory_context_for_vision,
                important_guidelines=important_guidelines,
            ),
            tools=[],
            state_schema=ReactAgentState,
        )
        inputs = {
            "messages": state.messages,
            "observation": state.observation,
            "plan": state.plan,
            "tools_interactions": {}
        }
        inputs, message = process_graph_stream(graph, inputs, config)
    
    if message.type == "ai":
        response = output_parser.parse(message)
    else:
        raise ValueError(f"Expected AI message but got: {message.__class__}")
    
    shared_objects = [shared_memory._shared_memory.get_memory_object(chat_id, _id) for _id in response.ids if shared_memory._shared_memory.get_memory_object(chat_id, _id) is not None]

    context_list = []
    for shared_object in shared_objects:
        b64_url = object_to_image_url(shared_object.object, format="JPEG")
        if b64_url:
            context_list.append(
                {
                    "type": "text",
                    "text": f"Image ID: {shared_object.metadata.object_id}\nImage Name: {shared_object.metadata.name}\nImage Description: {shared_object.metadata.description}"
                }
            )
            context_list.append(
                {
                    "type": "image_url",
                    "image_url": {"url": b64_url}
                }
            )
    
    if context_list:
        return HumanMessage(
            content=context_list
        )
    else:
        return None


# Cognitive model implementation
class ReactNodeCognitiveModel(AgentNodeCognitiveModel):
    """
    Cognitive model implementing the ReAct framework.
    """

    def think(self, state, config, node_name: str):
        # reading node prefix
        node_prefix = extract_node_prefix(node_name)
        
        # reading configurable parameters
        agent_name=config.get("configurable").get("agent_name"),
        agent_description=config.get("configurable").get("agent_description")
        node_prompt_language = config.get("configurable").get(f"{node_prefix}_node_llm_prompt_language")
        node_llm = config.get("configurable").get(f"{node_prefix}_node_llm")
        node_llm_use_structured_output = config.get("configurable").get(f"{node_prefix}_node_llm_use_structured_output", False)
        node_has_vision = config.get("configurable").get(f"{node_prefix}_node_has_vision", False)

        tools = config.get("configurable").get(f"{node_prefix}_tools", [])

        important_guidelines = config.get("configurable").get(f"{node_prefix}_important_guidelines")
        # generating memory context
        memory_context = self._agent_memory_stack.manifest_memories(state, config, node_name) if self._agent_memory_stack else ""
        
        # generating prompt
        prompt_data = prompt_generator.generate_prompt(
            prompt_name=node_prefix,
            language=node_prompt_language,
            llm=node_llm,
            use_structured_output=node_llm_use_structured_output
        )
        prompt = prompt_data["prompt"]
        output_parser = prompt_data["output_parser"]

        message = None
        inputs = {
            "messages": state.messages,
            "observation": state.observation,
            "plan": state.plan,
            "tools_interactions": {}
        }
        while not isinstance(message, AIMessage):
  
            vision_context = None
            if node_has_vision:
                vision_context = get_vision_context(
                    node_prompt_language=node_prompt_language,
                    node_llm=node_llm,
                    node_prompt_use_structured_output=node_llm_use_structured_output,
                    agent_memory_stack=self._agent_memory_stack,
                    node_name=node_name,
                    state=state,
                    config=config
                )
            
            prompt_partial = prompt.partial(
                agent_name=agent_name,
                agent_description=agent_description,
                memory=memory_context,
                important_guidelines=important_guidelines,
                tools_interactions=inputs.get("tools_interactions", {})
            )

            rendered_messages = prompt_partial.format_messages()

            if vision_context:
                rendered_messages.append(vision_context)

            graph = create_react_agent(
                model=node_llm,
                    prompt=ChatPromptTemplate.from_messages(rendered_messages),
                    tools=tools,
                    state_schema=ReactAgentState,
                )
            inputs, message = process_graph_stream(graph, inputs, config)

        # Access the 'role' attribute directly instead of using subscript notation
        if message.type == "ai":
            response = output_parser.parse(message)
        else:
            raise ValueError(f"Expected AI message but got: {message.__class__}")
        
        return response