import numpy as np
import random
import json
import os

class SARSAAgentLogic:
    def __init__(self, agent_name, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.agent_name = agent_name
        self.actions = ["do_task", "skip_task"]  # Fixed action space
        self.alpha = alpha      # Learning rate
        self.gamma = gamma      # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = {}

        # ✅ Track how many times each action is chosen
        self.action_counts = {a: 0 for a in self.actions}

        # Path to save Q-table
        self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", f"qtable_{agent_name}.json"))

        self._load_q_table()

    def _load_q_table(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.q_table = json.load(f)

    def _save_q_table(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.q_table, f, indent=2)

    def get_q(self, state, action):
        state_str = str(state)
        return self.q_table.get(state_str, {}).get(action, 0.0)

    def choose_action(self, state):
        state_str = str(state)
        self.q_table.setdefault(state_str, {a: 0.0 for a in self.actions})

        if random.random() < self.epsilon:
            action = random.choice(self.actions)
        else:
            action = max(self.q_table[state_str], key=self.q_table[state_str].get)

        # Increment count here too (just in case you want centralized tracking)
        self.action_counts[action] += 1
        return action

    def update(self, state, action, reward, next_state, next_action):
        s, a = str(state), action
        ns, na = str(next_state), next_action

        self.q_table.setdefault(s, {act: 0.0 for act in self.actions})
        self.q_table.setdefault(ns, {act: 0.0 for act in self.actions})

        q_current = self.q_table[s][a]
        q_next = self.q_table[ns][na]

        new_q = q_current + self.alpha * (reward + self.gamma * q_next - q_current)
        self.q_table[s][a] = new_q

        self._save_q_table()
