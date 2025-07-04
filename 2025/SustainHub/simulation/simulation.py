from agents.contributor import Contributor
from agents.maintainer import Maintainer
from tasks.generator import generate_task
from tasks.mab import MABAllocator
import random
import json
import os
import matplotlib.pyplot as plt  # ✅ New

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))
SAVE_FILE = os.path.join(DATA_DIR, "trained_agents.json")


class Simulation:
    def __init__(self):
        self.agents = self.load_agents()
        self.maintainer = Maintainer("Alice")
        self.task_queue = [generate_task() for _ in range(7)]
        self.mab_allocator = MABAllocator(self.agents)

    def load_agents(self):
        agents = [Contributor(f"C{i}") for i in range(1, 11)]
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r') as f:
                saved_data = json.load(f)
                for agent in agents:
                    if agent.name in saved_data:
                        agent.load_from_dict(saved_data[agent.name])
        return agents

    def save_agents(self):
        data = {agent.name: agent.to_dict() for agent in self.agents}
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    def assign_tasks(self):
        for task in self.task_queue:
            selected_agent = self.mab_allocator.select_agent(task)
            if selected_agent and selected_agent.assign_task(task):
                print(f"Assigned {task.task_type} task to {selected_agent.name}")
            else:
                print(f"No available agent for {task.task_type} task")
        self.task_queue.clear()

    def simulate_task_completion(self):
        for agent in self.agents:
            while agent.task_load > 0 and agent.current_tasks:
                task_type = agent.current_tasks[0]  # Peek without popping
                success = random.random() > 0.3     # 70% success chance

                if hasattr(agent, "act_and_learn"):
                    # For SARSA agents
                    agent.act_and_learn(task_type, success)
                else:
                    print(f"⚠️ {agent.name} skipped the task '{task_type}' → reward: 0")

                task_done = agent.complete_task(success, task_type)
                if task_done:
                    print(f"{agent.name} completed a {task_type} task {'successfully' if success else 'unsuccessfully'}")
                    agent.current_tasks.pop(0)

    def infer_role(self, agent):
        task_counts = agent.total_counts
        if task_counts.sum() == 0:
            return "Unclassified"
        max_index = int(task_counts.argmax())
        return ["Contributor", "Innovator", "Knowledge Curator"][max_index]

    def print_agent_stats(self):
        print("\n🔍 Agent Stats After Step:")
        for agent in self.agents:
            dynamic_role = self.infer_role(agent)
            print(f"\n👤 {agent.name} ({dynamic_role}):")
            for i, task_type in enumerate(["bug", "feature", "docs"]):
                total = agent.total_counts[i]
                success = agent.success_counts[i]
                fail = total - success
                success_rate = (success / total * 100) if total > 0 else 0
                print(f"   {task_type.capitalize()}: {success:.0f} Success / {fail:.0f} Fail | Success Rate: {success_rate:.1f}%")

    def plot_results(self):
        os.makedirs(DATA_DIR, exist_ok=True)

        sarsa_agents = [a for a in self.agents if hasattr(a, "sarsa") and hasattr(a, "rewards_history")]

        if not sarsa_agents:
            print("No SARSA agents found to visualize.")
            return

        num_agents = len(sarsa_agents)
        fig, axs = plt.subplots(num_agents, 2, figsize=(12, 4 * num_agents))
        if num_agents == 1:
            axs = [axs]  # Handle single-agent case

        for idx, agent in enumerate(sarsa_agents):
            # 📈 Rewards per step
            rewards = agent.rewards_history
            axs[idx][0].plot(range(len(rewards)), rewards, marker='o', linestyle='-', color='blue')
            axs[idx][0].set_title(f"{agent.name} - Reward Over Steps")
            axs[idx][0].set_xlabel("Step")
            axs[idx][0].set_ylabel("Reward")
            axs[idx][0].grid(True)

            # 📊 Action frequencies
            actions = agent.sarsa.action_counts
            axs[idx][1].bar(actions.keys(), actions.values(), color=['green', 'red'])
            axs[idx][1].set_title(f"{agent.name} - Action Frequency")
            axs[idx][1].set_ylabel("Count")

        plt.tight_layout()
        full_path = os.path.join(DATA_DIR, "sarsa_agents_summary.png")
        plt.savefig(full_path)
        plt.show()
        print(f"📊 Plots saved to: {full_path}")

    def run(self, steps=10):
        print("Simulation starting...\n")
        for step in range(steps):
            print(f"\n--- Step {step + 1} ---")
            self.task_queue = [generate_task() for _ in range(3)]
            self.assign_tasks()
            self.simulate_task_completion()
            self.print_agent_stats()
        self.save_agents()
        self.plot_results()


if __name__ == "__main__":
    sim = Simulation()
    sim.run(steps=10)
