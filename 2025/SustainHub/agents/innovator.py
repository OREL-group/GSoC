from agents.base_agent import BaseAgent

class Innovator(BaseAgent):
    def __init__(self, name):
        super().__init__(name, "Innovator")

    def get_reward(self, task_type):
        return 3 if task_type == "feature" else 0.5
