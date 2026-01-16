from eagle.agents.agent_memory.base import AgentMemory
from eagle.memory.shared.shared_objects_memory import SharedObjectsMemory
from eagle.utils.agents_utils import extract_node_prefix
from datetime import datetime, timezone
from jinja2 import Template
from pydantic import Field, BaseModel

# Prompts
OBJECTS_SUMMARY_STR_PT_BR = """
{%- if objects_summary %}
Abaixo está um resumo dos últimos objetos criados e as relações entre eles:
------------------ Sumário de Objetos ------------------
{{ objects_summary }}
--------------------------------------------------------
{%- endif %}
{%- if must_cite_objects_summary %}
Os seguintes objetos devem ser citados na resposta, com os respectivos IDs:
--------------- Objetos a serem citados-----------------
{{ must_cite_objects_summary }}
--------------------------------------------------------
{%- endif %}
"""

OBJECTS_SUMMARY_STR_EN = """
{%- if objects_summary %}
Below is a summary of the last created objects and the relationships between them:
------------------ Objects Summary ------------------
{{ objects_summary }}
-----------------------------------------------------
{%- endif %}
{%- if must_cite_objects_summary %}
The following objects must be cited in the response, with their respective IDs:
--------------- Objects to be cited -----------------
{{ must_cite_objects_summary }}
-----------------------------------------------------
{%- endif %}
"""

OBJECTS_SUMMARY_TEMPLATE_DICT = {
    "pt-br": Template(OBJECTS_SUMMARY_STR_PT_BR.strip()),
    "en": Template(OBJECTS_SUMMARY_STR_EN.strip()),
}

# Auxiliary Functions

def _get_objects_summary_template(language: str) -> Template:
    """Get the objects summary template based on the language."""
    return OBJECTS_SUMMARY_TEMPLATE_DICT.get(language.lower(), OBJECTS_SUMMARY_TEMPLATE_DICT["en"])

# Memory configs
class SharedObjectsMemoryConfigSchema(BaseModel):
    language: str = Field(default="pt-br", description="Language for object summaries.")
    k: int = Field(default=10, description="Number of recent memories to retrieve.")

# Memory class

class SharedObjectsAgentMemory(AgentMemory):
    """Memory implementation for shared objects among agents."""

    def __init__(self, shared_memory: SharedObjectsMemory, include_must_cite: bool = False, shared_memory_config: SharedObjectsMemoryConfigSchema = SharedObjectsMemoryConfigSchema()):
        """Initialize the shared objects memory."""
        super().__init__()
        self._shared_memory = shared_memory
        self._include_must_cite = include_must_cite
        self._shared_memory_config = shared_memory_config
    
    def store_memory(self, state, config, node_name: str, step: str):
        pass

    def _manifest_memory_no_must_cite(self, state, chat_id: str, prompt_language: str) -> str:
        # Generate manifested memory
        last_memories_metadata = self._shared_memory.get_last_memories_metadata(chat_id=chat_id, k=self._shared_memory_config.k)
        object_ids = [metadata.object_id for metadata in last_memories_metadata]
        objects_summary = self._shared_memory.generate_summary_from_object_ids(
            chat_id=chat_id, object_ids=object_ids, language=self._shared_memory_config.language    
        )
        template = _get_objects_summary_template(prompt_language)
        manifested_memory = template.render(objects_summary=objects_summary, must_cite_objects_summary="")

        return manifested_memory
    
    def _manifest_memory_with_must_cite(self, state, chat_id: str, prompt_language: str) -> str:
        # Generate manifested memory with must cite information
        last_memories_metadata = self._shared_memory.get_last_memories_metadata(chat_id=chat_id, k=self._shared_memory_config.k)
        object_ids = [metadata.object_id for metadata in last_memories_metadata]
        must_cite_object_ids = []
        if state.interaction_initial_datetime:  
            for metadata in last_memories_metadata:
                if datetime.fromtimestamp(metadata.created_at/1000).astimezone(timezone.utc) >= state.interaction_initial_datetime:
                    must_cite_object_ids.append(metadata.object_id)
        objects_summary = self._shared_memory.generate_summary_from_object_ids(
            chat_id=chat_id, object_ids=list(set(object_ids)-set(must_cite_object_ids)), language=self._shared_memory_config.language    
        )
        must_cite_objects_summary = self._shared_memory.generate_summary_from_object_ids(
            chat_id=chat_id, object_ids=must_cite_object_ids, language=self._shared_memory_config.language    
        )
        template = _get_objects_summary_template(prompt_language)
        manifested_memory = template.render(objects_summary=objects_summary, must_cite_objects_summary=must_cite_objects_summary)

        return manifested_memory

    def manifest_memory(self, state, config, node_name: str) -> str:
        """Manifest the shared objects as a string."""
        # Node prefix
        node_prefix = extract_node_prefix(node_name)

        # Config parameters
        chat_id = config.get("configurable").get("chat_id")
        prompt_language = config.get("configurable").get(f"{node_prefix}_node_llm_prompt_language")

        # Generate manifested memory
        if self._include_must_cite:
            return self._manifest_memory_with_must_cite(
                state=state,
                chat_id=chat_id,
                prompt_language=prompt_language
            )
        else:
            return self._manifest_memory_no_must_cite(
                state=state,
                chat_id=chat_id,
                prompt_language=prompt_language
            )