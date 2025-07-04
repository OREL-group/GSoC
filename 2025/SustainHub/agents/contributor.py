from agents.base_agent import BaseAgent
from agents.sarsa import SARSAAgentLogic

class Contributor(BaseAgent):
    def __init__(self, name):
        super().__init__(name, "Contributor")
        self.sarsa = SARSAAgentLogic(agent_name=name)
        self.rewards_history = []
        self.cumulative_rewards = []

    def calculate_reward(self, task_type):
        return 3 if task_type == "bug" else 1

    def act_and_learn(self, task_type, success):
        state = (task_type,)
        action = self.sarsa.choose_action(state)
        reward = self.calculate_reward(task_type) if success and action == "do_task" else -1
        next_state = (task_type,)
        next_action = self.sarsa.choose_action(next_state)

        self.sarsa.update(state, action, reward, next_state, next_action)

        # 🟦 Track rewards
        self.rewards_history.append(reward)
        self.sarsa.action_counts[action] = self.sarsa.action_counts.get(action, 0) + 1

        # 🟠 Track cumulative rewards
        if self.cumulative_rewards:
            self.cumulative_rewards.append(self.cumulative_rewards[-1] + reward)
        else:
            self.cumulative_rewards.append(reward)
