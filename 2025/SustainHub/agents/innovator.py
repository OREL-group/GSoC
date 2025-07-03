from agents.base_agent import BaseAgent

class Innovator(BaseAgent):
    def __init__(self, name):
        super().__init__(name, "Innovator")

    def calculate_reward(self, task_type):
        return 3 if task_type == "feature" else 1

    def act_and_learn(self, task_type, success):
        state = (task_type,)
        action = self.sarsa.choose_action(state)
        reward = self.calculate_reward(task_type) if success else -1
        next_state = state
        next_action = self.sarsa.choose_action(next_state)

        self.sarsa.update(state, action, reward, next_state, next_action)

       # print(f"💡 {self.name} used action '{action}' for {task_type} → reward: {reward}")
