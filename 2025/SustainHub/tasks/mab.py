# Implement MAB for task allocation
import numpy as np
from scipy.stats import beta

class MABAllocator:
    def __init__(self, agents, exploration_factor=0.2):
        self.agents = agents
        self.exploration_factor = exploration_factor

    def select_agent(self, task):
        task_type = task.task_type

        # Exploration
        if np.random.random() < self.exploration_factor:
            available_agents = [a for a in self.agents if a.task_load < a.max_load]
            if available_agents:
                return np.random.choice(available_agents)
            return None

        # Exploitation (Thompson Sampling)
        max_sample = -1
        best_agent = None

        for agent in self.agents:
            if agent.task_load >= agent.max_load:
                continue

            task_idx = agent._task_type_to_idx(task_type)
            successes = agent.success_counts[task_idx]
            failures = agent.total_counts[task_idx] - successes

            sample = beta.rvs(successes + 1, failures + 1)

            if sample > max_sample:
                max_sample = sample
                best_agent = agent

        return best_agent
