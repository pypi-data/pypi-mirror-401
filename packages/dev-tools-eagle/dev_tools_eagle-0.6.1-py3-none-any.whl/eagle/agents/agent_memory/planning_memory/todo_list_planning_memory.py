from eagle.agents.agent_memory.base import AgentMemory
from eagle.utils.agents_utils import extract_node_prefix
from eagle.utils.prompt_utils import EagleJsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence, RunnableLambda
from langchain_core.language_models.base import BaseLanguageModel
from pydantic import BaseModel, Field
from jinja2 import Template
from typing import List, ClassVar
from operator import itemgetter

# Prompts
CREATE_TODO_LIST_STR_PT_BR = """
Você é um agente de planejamento que cria listas de tarefas para atingir objetivos específicos. Com base nas informações fornecidas, elabore uma lista de tarefas detalhada e organizada que ajude a alcançar o objetivo proposto.
Observe o histórico de interações abaixo e o plano proposto:
------------------ Histórico de Interações ------------------
{{ history }}
-------------------------------------------------------------
{%- if last_plan %}
------------------ Plano Proposto ANTERIORMENTE -------------
{{ last_plan }}
-------------------------------------------------------------
{%- endif %}
{%- if observation %}
------------------ Observações Recentes ------------------
{{ observation }}
----------------------------------------------------------
{%- endif %}
------------------ Plano Proposto AGORA ------------------
{{ proposed_plan }}
----------------------------------------------------------
Com base nessas informações, defina ou atualize a lista ORDENADA de tarefas com a seguinte estrutura:
{
  "tarefas": [
    {
      "descricao": "Descrição detalhada da tarefa",
      "status": "Pendente" ou "Concluída" ou "Problemática",
      "anotacoes": "Anotações sobre problemas, caso status seja 'Problemática', ou de conclusões importantes, caso o status seja 'Concluída'."
    },
    {
    ... outra tarefa ...
    }... e assim por diante ...
  ]
}
Diretrizes importantes:
- Mantenha as tarefas concluídas na lista para registro.
- Indique claramente as tarefas problemáticas com anotações apropriadas.
RESPOSTA:
"""

CREATE_TODO_LIST_STR_EN = """
You are a planning agent that creates task lists to achieve specific goals. Based on the provided information, craft a detailed and organized task list that helps accomplish the proposed objective.
Review the interaction history below and the proposed plan:
------------------ Interaction History ------------------
{{ history }}
---------------------------------------------------------
{%- if last_plan %}
------------------ Previously Proposed Plan -------------
{{ last_plan }}
---------------------------------------------------------
{%- endif %}
{%- if observation %}
------------------ Recent Observations ------------------
{{ observation }}
----------------------------------------------------------
{%- endif %}
------------------ Currently Proposed Plan ------------------
{{ proposed_plan }}
----------------------------------------------------------
Based on this information, define or update the ORDERED list of tasks with the following structure:
{
  "tasks": [
    {
      "description": "Detailed description of the task",
      "status": "Pending" or "Completed" or "Problematic",
      "annotations": "Notes about problems, if status is 'Problematic', or important conclusions, if status is 'Completed'."
    },
    { ... another task ...
    }... and so on ...
  ]
}
Important guidelines:
- Maintain the completed tasks in the list for record-keeping.
- Clearly indicate problematic tasks with appropriate annotations.
RESPONSE:
"""

CREATE_TO_DO_LIST_PROMPTS = {
    "en": PromptTemplate.from_template(CREATE_TODO_LIST_STR_EN, template_format="jinja2"),
    "pt-br": PromptTemplate.from_template(CREATE_TODO_LIST_STR_PT_BR, template_format="jinja2"),
}

HISTORY_MESSAGES_PROMPT_STR = """
{%- for message in messages %}
{{ message.name }}: {{ message.content }}
{%- endfor %}
"""

MANIFEST_TODO_LIST_STR_PT_BR = """
----------- Plano a ser Executado ------------
Lista de Tarefas:
{%- for item in plan.tasks %}
- Descrição: {{ item.description }}
  Status: {{ item.status }}
  Anotações: {{ item.annotations }}
{%- endfor %}
----------------------------------------------
"""

MANIFEST_TODO_LIST_STR_EN = """
------------ Plan to be Executed -------------
Task List:
{%- for item in plan.tasks %}
- Description: {{ item.description }}
  Status: {{ item.status }}
  Annotations: {{ item.annotations }}
{%- endfor %}
----------------------------------------------
"""

MANIFEST_TO_DO_LIST_PROMPTS = {
    "en": Template(MANIFEST_TODO_LIST_STR_EN),
    "pt-br": Template(MANIFEST_TODO_LIST_STR_PT_BR),
}

# Schemas
class ToDoListItemSchemaPT_BR(BaseModel):
    descricao: str = Field(..., description="Descrição detalhada da tarefa")
    status: str = Field(..., description="Status da tarefa: 'Pendente', 'Concluída' ou 'Problemática'")
    anotacoes: str = Field("", description="Anotações sobre problemas ou conclusões importantes")

class ToDoListItemSchemaEN(BaseModel):
    description: str = Field(..., description="Detailed description of the task")
    status: str = Field(..., description="Task status: 'Pending', 'Completed' or 'Problematic'")
    annotations: str = Field("", description="Notes about problems or important conclusions")

class ToDoListSchemaPT_BR(BaseModel):
    tarefas: List[ToDoListItemSchemaPT_BR] = Field(..., description="Lista de tarefas") 

class ToDoListSchemaEN(BaseModel):
    tasks: List[ToDoListItemSchemaEN] = Field(..., description="List of tasks")

# Output Parsers
class ToDoListOutputParser(EagleJsonOutputParser):
    
    CONVERTION_SCHEMA: ClassVar[dict] = {
        "pt-br": {
            "class_for_parsing": ToDoListSchemaPT_BR,
            "convertion_schema": {
                "tarefas": {
                    "target_key": "tasks",
                    "value_mapping": {
                        "descricao": {
                            "target_key": "description",
                            "value_mapping": {}
                        },
                        "status": {
                            "target_key": "status",
                            "value_mapping": {
                                "Pendente": "Pending",
                                "Concluída": "Completed",
                                "Problemática": "Problematic"
                            }
                        },
                        "anotacoes": {
                            "target_key": "annotations",
                            "value_mapping": {}
                        }
                    }
                }
            }
        },
        "en": {
            "class_for_parsing": ToDoListSchemaEN,
            "convertion_schema": {
                "tasks": {
                    "target_key": "tasks",
                    "value_mapping": {
                        "description": {
                            "target_key": "description",
                            "value_mapping": {}
                        },
                        "status": {
                            "target_key": "status",
                            "value_mapping": {}
                        },
                        "annotations": {
                            "target_key": "annotations",
                            "value_mapping": {}
                        }
                    }
                }
            }
        },
    }

    TARGET_SCHEMA: BaseModel = ToDoListSchemaEN

# Chains
def _get_create_a_todo_list_chain(prompt_language: str, llm: BaseLanguageModel, use_structured_output: bool = False) -> RunnableSequence:
    if prompt_language not in CREATE_TO_DO_LIST_PROMPTS:
        raise ValueError(f"Unsupported prompt language: {prompt_language}")
    prompt = CREATE_TO_DO_LIST_PROMPTS[prompt_language]
    output_parser = ToDoListOutputParser(
        source_lang=prompt_language,
        llm=llm,
        use_structured_output=use_structured_output
    )
    _parse = RunnableLambda(lambda x: output_parser.parse(x))
    chain = (
        {"history": itemgetter("history"), "last_plan": itemgetter("last_plan"), "observation": itemgetter("observation"), "proposed_plan": itemgetter("proposed_plan")}
        | prompt
        | llm
        | _parse
    )
    return chain

# Memory class
class ToDoListPlanningAgentMemory(AgentMemory):
    """Memory implementation for to-do list planning."""

    def __init__(
            self,
            nodes_to_plan_on: List[str] = ["plan"],
            llm: BaseLanguageModel = None,
            use_structured_output: bool = False,
            chat_history_window_size: int = None
        ):
        """Initialize the to-do list planning memory."""
        super().__init__()
        self._nodes_to_plan_on = nodes_to_plan_on
        self._plan = []
        self._llm = llm
        self._use_structured_output = use_structured_output
        self._chat_history_window_size = chat_history_window_size
        
    def store_memory(self, state, config, node_name: str, step: str):
        """Store memory if the node is in the nodes to plan on."""
        node_prefix = extract_node_prefix(node_name)
        if node_prefix in self._nodes_to_plan_on and step == 'end':
            # Implement logic to store to-do list planning memory
            llm = self._llm or config.get("configurable").get(f"{node_prefix}_node_llm")
            use_structured_output = self._use_structured_output or config.get("configurable").get(f"{node_prefix}_node_llm_use_structured_output")
            chat_history_window_size = min(self._chat_history_window_size or config.get("configurable").get("chat_history_window_size"), len(state.messages))
            prompt_language = config.get("configurable").get(f"{node_prefix}_node_llm_prompt_language")
            history = Template(HISTORY_MESSAGES_PROMPT_STR).render(
                messages=state.messages[-chat_history_window_size:]
            )
            last_plan = self.manifest_memory(state, config, node_name)
            chain = _get_create_a_todo_list_chain(prompt_language, llm, use_structured_output)
            inputs = {
                "history": history,
                "last_plan": last_plan,
                "observation": state.observation or "",
                "proposed_plan": state.plan or ""
            }
            self._plan = chain.invoke(inputs)

    def manifest_memory(self, state, config, node_name):
        """Manifest the current to-do list plan."""
        if self._plan:
            node_prefix = extract_node_prefix(node_name)
            prompt_language = config.get("configurable").get(f"{node_prefix}_node_llm_prompt_language")
            if prompt_language not in MANIFEST_TO_DO_LIST_PROMPTS:
                raise ValueError(f"Unsupported prompt language: {prompt_language}")
            template = MANIFEST_TO_DO_LIST_PROMPTS[prompt_language]
            rendered = template.render(plan=self._plan)
            return rendered
        else:
            return ""