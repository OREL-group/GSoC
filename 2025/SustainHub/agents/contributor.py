from agents.base_agent import BaseAgent
from agents.sarsa import SARSAAgentLogic

class Contributor(BaseAgent):
    def __init__(self, name):
        super().__init__(name, "Contributor")
        self.sarsa = SARSAAgentLogic(
            agent_name=name,
            actions=["code_fix", "ask_peer", "retry"]
        )

    def calculate_reward(self, task_type):
        return 3 if task_type == "bug" else 1

    def act_and_learn(self, task_type, success):
        state = (task_type,)  # Can add more like expertise_level
        action = self.sarsa.choose_action(state)
        reward = self.calculate_reward(task_type) if success else -1

        next_state = (task_type,)  # same task for now
        next_action = self.sarsa.choose_action(next_state)

        self.sarsa.update(state, action, reward, next_state, next_action)

        print(f"🧠 {self.name} used action '{action}' for {task_type} and got reward {reward}")
