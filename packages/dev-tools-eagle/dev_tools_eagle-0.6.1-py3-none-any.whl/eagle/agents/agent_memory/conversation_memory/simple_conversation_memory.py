from eagle.agents.agent_memory.base import AgentMemory
from eagle.utils.agents_utils import extract_node_prefix
import pandas as pd
from datetime import datetime
from jinja2 import Template

# Prompts
HISTORY_MESSAGES_PROMPT_STR_PT_BR = """
---------- Histórico das {{ window_size }} mensagens mais recentes ------------
{%- if messages_from_past_interactions %}
------- De interações passadas -------
{%- for message in messages_from_past_interactions %}
[{{ message['timestamp'] }}] - {{ message['name'] }}: {{ message['content'] }}
{%- endfor %}
----------------------------------
{%- endif %}
{%- if messages_from_current_interaction %}
------- Da interação atual -------
{%- for message in messages_from_current_interaction %}
[{{ message['timestamp'] }}] - {{ message['name'] }}: {{ message['content'] }}
{%- endfor %}
----------------------------------
{%- endif %}
"""

HISTORY_MESSAGES_PROMPT_STR_EN = """
---------- History of the {{ window_size }} most recent messages ------------
{%- if messages_from_past_interactions %}
------- From past interactions -------
{%- for message in messages_from_past_interactions %}
[{{ message['timestamp'] }}] - {{ message['name'] }}: {{ message['content'] }}
{%- endfor %}
----------------------------------
{%- endif %}
{%- if messages_from_current_interaction %}
------- From current interaction -------
{%- for message in messages_from_current_interaction %}
[{{ message['timestamp'] }}] - {{ message['name'] }}: {{ message['content'] }}
{%- endfor %}
----------------------------------
{%- endif %}
"""

HISTORY_MESSAGES_PROMPT_DICT = {
    "pt-br": Template(HISTORY_MESSAGES_PROMPT_STR_PT_BR),
    "en": Template(HISTORY_MESSAGES_PROMPT_STR_EN),
}

# Memory class
class SimpleConversationAgentMemory(AgentMemory):
    """
    A simple conversation memory that stores the last N messages.
    """

    def __init__(self, chat_history_window_size: int = 10):
        self._chat_history_window_size = chat_history_window_size
        self._messages = []

    def _messages_to_dataframe(self):
        messages_as_df = pd.DataFrame(self._messages)
        if messages_as_df.empty:
            return messages_as_df
        messages_as_df.set_index(keys=['id'], inplace=True)
        messages_as_df.drop_duplicates(inplace=True)
        return messages_as_df

    def _add_messages(self, messages):

        messages_as_df = self._messages_to_dataframe()
        _new_messages = []
        for msg in messages:
            if msg.id not in messages_as_df.index:
                msg_dict = {
                    "id": msg.id,
                    "name": msg.name,
                    "type": msg.type,
                    "content": msg.content,
                    "timestamp": datetime.utcnow(),
                }
                _new_messages.append(msg_dict)
        self._messages.extend(_new_messages)
        
    def store_memory(self, state, config, node_name: str, step: str):
        """Store the last messages from the conversation."""
        if step == 'start':
            self._add_messages(state.messages)

    def manifest_memory(self, state, config, node_name: str):
        """Return the N most recent stored messages as a formatted string."""
        node_prefix = extract_node_prefix(node_name)
        messages_as_df = self._messages_to_dataframe()
        chat_history_window_size = min(self._chat_history_window_size or config.get("configurable").get("chat_history_window_size"), len(state.messages))
        last_messages = messages_as_df.tail(self._chat_history_window_size)
        # Certifique-se de que a coluna 'timestamp' está no tipo correto
        last_messages = last_messages.copy()
        last_messages['timestamp'] = pd.to_datetime(last_messages['timestamp'], utc=True)
        current_interaction_messages = last_messages[
            last_messages['timestamp'] >= state.interaction_initial_datetime
        ]
        past_interaction_messages = last_messages[
            last_messages['timestamp'] < state.interaction_initial_datetime
        ]
        prompt_language = config.get("configurable").get(f"{node_prefix}_node_llm_prompt_language")
        template = HISTORY_MESSAGES_PROMPT_DICT.get(prompt_language, HISTORY_MESSAGES_PROMPT_DICT["en"])
        rendered_messages = template.render(
            window_size=chat_history_window_size,
            messages_from_current_interaction=current_interaction_messages.to_dict('records'),
            messages_from_past_interactions=past_interaction_messages.to_dict('records'),
        )
        return rendered_messages
