from agents.base_agent import BaseAgent
from agents.sarsa import SARSAAgentLogic

class Innovator(BaseAgent):
    def __init__(self, name):
        super().__init__(name, "Innovator")
        self.sarsa = SARSAAgentLogic(agent_name=name)
        self.rewards_history = []

    def calculate_reward(self, task_type):
        return 3 if task_type == "feature" else 1

    def act_and_learn(self, task_type, success):
        state = (task_type,)
        action = self.sarsa.choose_action(state)
        reward = self.calculate_reward(task_type) if success and action == "do_task" else -1
        next_state = (task_type,)
        next_action = self.sarsa.choose_action(next_state)

        self.sarsa.update(state, action, reward, next_state, next_action)

        self.rewards_history.append(reward)
        self.sarsa.action_counts[action] = self.sarsa.action_counts.get(action, 0) + 1
