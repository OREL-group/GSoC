import numpy as np
import json
from agents.sarsa import SARSAAgentLogic

TASK_TYPES = ["bug", "feature", "docs"]
ACTIONS = ["retry", "ask_peer", "code_fix"]  # Example SARSA actions

class BaseAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.task_load = 0
        self.max_load = 5
        self.success_counts = np.zeros(3)
        self.total_counts = np.zeros(3)
        self.rewards = []
        self.current_tasks = []  # Tracks assigned task types
        self.expertise_level = 1

        # SARSA logic initialized
        self.sarsa = SARSAAgentLogic(agent_name=name, actions=ACTIONS)

    def assign_task(self, task):
        if self.task_load < self.max_load:
            self.task_load += 1
            self.current_tasks.append(task.task_type)
            return True
        return False

    def complete_task(self, success, task_type=None):
        self.task_load -= 1
        if task_type is None and self.current_tasks:
            task_type = self.current_tasks.pop(0)
        elif task_type is None:
            task_type = "bug"  # fallback

        task_idx = self._task_type_to_idx(task_type)
        self.total_counts[task_idx] += 1
        if success:
            self.success_counts[task_idx] += 1
            reward = self.calculate_reward(task_type)
        else:
            reward = -1

        self.rewards.append({
            "task_type": task_type,
            "success": success,
            "reward": reward
        })

        # === SARSA update ===
        self.act_and_learn(task_type, reward)

    def act_and_learn(self, task_type, reward):
        state = (task_type,)
        action = self.sarsa.choose_action(state)
        next_state = (task_type,)
        next_action = self.sarsa.choose_action(next_state)
        self.sarsa.update(state, action, reward, next_state, next_action)

    def calculate_reward(self, task_type):
        # Default reward
        return 1

    def get_success_rate(self, task_type):
        task_idx = self._task_type_to_idx(task_type)
        total = self.total_counts[task_idx]
        return self.success_counts[task_idx] / total if total > 0 else 0.5

    def _task_type_to_idx(self, task_type):
        return TASK_TYPES.index(task_type)

    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "success_counts": self.success_counts.tolist(),
            "total_counts": self.total_counts.tolist(),
            "rewards": self.rewards
        }

    def load_from_dict(self, data):
        self.success_counts = np.array(data.get("success_counts", [0, 0, 0]))
        self.total_counts = np.array(data.get("total_counts", [0, 0, 0]))
        self.rewards = data.get("rewards", [])
