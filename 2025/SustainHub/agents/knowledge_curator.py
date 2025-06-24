from agents.base_agent import BaseAgent

class KnowledgeCurator(BaseAgent):
    def __init__(self, name):
        super().__init__(name, "Knowledge Curator")

    def get_reward(self, task_type):
        return 3 if task_type == "docs" else 0.5
