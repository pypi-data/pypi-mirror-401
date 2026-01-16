from eagle.agents.agent_memory.base import AgentMemory
from eagle.utils.agents_utils import extract_node_prefix
import pandas as pd
from datetime import datetime
from jinja2 import Template

# Prompts
OBSERVATION_STR_PT_BR = """
{%- if observation %}
Há pouco, você anotou a seguinte observação:
-------------------- Observação ------------------------
{{ observation }}
--------------------------------------------------------
{%- endif %}
"""
OBSERVATION_STR_EN = """
{%- if observation %}
You noted the following observation a moment ago:
-------------------- Observation --------------------
{{ observation }}
-----------------------------------------------------
{%- endif %}
"""

OBSERVATION_PROMPT_DICT = {
    "pt-br": Template(OBSERVATION_STR_PT_BR),
    "en": Template(OBSERVATION_STR_EN),
}

# Memory class
class SimpleObservationAgentMemory(AgentMemory):
    """
    A simple observation memory.
    """
        
    def store_memory(self, state, config, node_name: str, step: str):
        pass

    def manifest_memory(self, state, config, node_name: str):
        """Return the most recent observation formatted as a prompt."""
        node_prefix = extract_node_prefix(node_name)
        prompt_language = config.get("configurable").get(f"{node_prefix}_node_llm_prompt_language")
        template = OBSERVATION_PROMPT_DICT.get(prompt_language, OBSERVATION_PROMPT_DICT["en"])
        rendered_observations = template.render(
            observation=state.observation
        )
        return rendered_observations