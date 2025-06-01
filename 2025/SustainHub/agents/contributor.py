from agents.base_agent import BaseAgent

class Contributor(BaseAgent):
    def __init__(self, name):
        super().__init__(name, "Contributor")
