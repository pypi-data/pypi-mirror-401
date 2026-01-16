from eagle.agents.agent_memory.base import AgentMemoryStack
from eagle.agents.agent_memory.conversation_memory.simple_conversation_memory import SimpleConversationAgentMemory
from eagle.agents.agent_memory.observation_memory.simple_observation_memory import SimpleObservationAgentMemory
from eagle.agents.agent_memory.planning_memory.todo_list_planning_memory import ToDoListPlanningAgentMemory
from eagle.agents.agent_memory.shared_memory.shared_objects_memory import SharedObjectsAgentMemory, SharedObjectsMemoryConfigSchema
from eagle.memory.shared.shared_objects_memory import SharedObjectsMemory
from eagle.utils.agents_utils import extract_node_prefix

# Memory adaptations
class AdaptedSharedObjectsAgentMemory(SharedObjectsAgentMemory):
    
    def __init__(self, shared_memory: SharedObjectsMemory, shared_memory_config: SharedObjectsMemoryConfigSchema = SharedObjectsMemoryConfigSchema()):
        self._execute_node_memory = SharedObjectsAgentMemory(
            shared_memory=shared_memory,
            include_must_cite=True,
            shared_memory_config=shared_memory_config
        )
        self._other_nodes_memory = SharedObjectsAgentMemory(
            shared_memory=shared_memory,
            include_must_cite=False,
            shared_memory_config=shared_memory_config
        )
    
    def manifest_memory(self, state, config, node_name):
        # Node prefix
        node_prefix = extract_node_prefix(node_name)

        if node_prefix == "execute":
            return self._execute_node_memory.manifest_memory(state, config, node_name)
        else:
            return self._other_nodes_memory.manifest_memory(state, config, node_name)
        
# Memory stack
class ConversationBasicAgentMemoryStackTemplate(AgentMemoryStack):
    def __init__(
            self,
            shared_memory: SharedObjectsMemory,
            shared_memory_config: SharedObjectsMemoryConfigSchema = SharedObjectsMemoryConfigSchema(),
            chat_history_window_size: int = 10,
        ):
        super().__init__()
        self.conversation_memory = SimpleConversationAgentMemory(
            chat_history_window_size=chat_history_window_size
        )
        self.observation_memory = SimpleObservationAgentMemory()
        self.shared_objects_memory = AdaptedSharedObjectsAgentMemory(
            shared_memory=shared_memory,
            shared_memory_config=shared_memory_config
        )
        self.todo_list_planning_memory = ToDoListPlanningAgentMemory(
            nodes_to_plan_on=["plan"],
            llm=None,
            use_structured_output=False,
            chat_history_window_size=chat_history_window_size
        )
        self.add_memories([
                self.conversation_memory,
                self.observation_memory,
                self.shared_objects_memory,
                self.todo_list_planning_memory
            ]
        )
