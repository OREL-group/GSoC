from agents.contributor import Contributor
from agents.maintainer import Maintainer
from tasks.generator import generate_task
from tasks.mab import MABAllocator
import random
import json
import os
from graph import plot_sarsa_agents
from simulation.metrics import compute_harmony_index, compute_resilience_quotient, calculate_reassignment_overhead

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))
SAVE_FILE = os.path.join(DATA_DIR, "trained_agents.json")


class Simulation:
    def __init__(self, agent_count, tasks_per_step=3, dropouts_per_step=0):
        self.agent_count = agent_count
        self.tasks_per_step = tasks_per_step
        self.dropouts_per_step = dropouts_per_step
        self.agents = self.load_agents()
        self.maintainer = Maintainer("Alice")
        self.task_queue = []
        self.mab_allocator = MABAllocator(self.agents)
        self.harmony_history = []
        self.rq_history = []
        self.ro_history = []  # NEW metric tracking
        self.dropped_task_log = []
        self.total_tasks_assigned_step = 0
        self.total_reassigned_tasks_step = 0

    def load_agents(self):
        agents = [Contributor(f"C{i}") for i in range(1, self.agent_count + 1)]
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
        # Track totals for RO calculation
        self.total_tasks_assigned_step = len(self.task_queue)
        self.total_reassigned_tasks_step = 0

        for task in self.task_queue:
            selected_agent = self.mab_allocator.select_agent(task)

            while selected_agent and getattr(selected_agent, "inactive", False):
                selected_agent = self.mab_allocator.select_agent(task)

            if selected_agent and selected_agent.assign_task(task):
                # Increment reassignment counters
                self.total_reassigned_tasks_step += 1
                selected_agent.reassigned_tasks = getattr(selected_agent, "reassigned_tasks", 0) + 1

                print(f"Assigned {task.task_type} task to {selected_agent.name}")

                for entry in self.dropped_task_log:
                    if entry["task_type"] == task.task_type and entry["reassigned_to"] is None:
                        entry["reassigned_to"] = selected_agent.name
                        entry["completion_status"] = "Pending"
                        break
            else:
                print(f"No available agent for {task.task_type} task")

        self.task_queue.clear()

    def simulate_task_completion(self):
        for agent in self.agents:
            if getattr(agent, "inactive", False):
                continue

            while agent.task_load > 0 and agent.current_tasks:
                task_type = agent.current_tasks[0]
                success = random.random() > 0.3

                if hasattr(agent, "act_and_learn"):
                    agent.act_and_learn(task_type, success)
                else:
                    print(f"⚠️ {agent.name} skipped the task '{task_type}' → reward: 0")

                task_done = agent.complete_task(success, task_type)
                if task_done:
                    print(f"{agent.name} completed a {task_type} task {'successfully' if success else 'unsuccessfully'}")

                    for entry in self.dropped_task_log:
                        if (
                            entry["task_type"] == task_type and
                            entry["reassigned_to"] == agent.name and
                            entry["completion_status"] == "Pending"
                        ):
                            entry["completion_status"] = "Success" if success else "Fail"
                            break

                    agent.current_tasks.pop(0)

    def simulate_dropout(self, count=2):
        dropout_agents = random.sample([a for a in self.agents if not getattr(a, "inactive", False)], k=count)
        for agent in dropout_agents:
            agent.inactive = True
            agent.dropped_tasks = len(agent.current_tasks)
            agent.reassigned_tasks = 0

            print(f"❌ {agent.name} DROPPED OUT ")

            for task_type in agent.current_tasks:
                self.dropped_task_log.append({
                    "task_type": task_type,
                    "original_agent": agent.name,
                    "reassigned_to": None,
                    "completion_status": None
                })

            agent.current_tasks = []
            agent.task_load = 0

    def infer_role(self, agent):
        task_counts = agent.total_counts
        if task_counts.sum() == 0:
            return "Unclassified"
        max_index = int(task_counts.argmax())
        return ["Contributor", "Innovator", "Knowledge Curator"][max_index]

    def print_agent_stats(self):
        print("\n🔍 Agent Stats After Step:")
        for agent in self.agents:
            if getattr(agent, "inactive", False):
                continue

            dynamic_role = self.infer_role(agent)
            print(f"\n👤 {agent.name} ({dynamic_role}):")
            for i, task_type in enumerate(["bug", "feature", "docs"]):
                total = agent.total_counts[i]
                success = agent.success_counts[i]
                fail = total - success
                success_rate = (success / total * 100) if total > 0 else 0
                print(f"   {task_type.capitalize()}: {success:.0f} Success / {fail:.0f} Fail | Success Rate: {success_rate:.1f}%")

    def run(self, steps=5):
        print("Simulation starting...\n")

        for step in range(steps):
            print(f"\n--- Step {step + 1} ---")

            self.simulate_dropout(count=self.dropouts_per_step)

            new_tasks = [generate_task() for _ in range(self.tasks_per_step)]
            self.task_queue.extend(new_tasks)

            self.assign_tasks()
            self.simulate_task_completion()

            harmony = compute_harmony_index(self.agents)
            self.harmony_history.append(harmony)

            success_rates = [
                sum(agent.success_counts) / sum(agent.total_counts)
                for agent in self.agents if sum(agent.total_counts) > 0
            ]
            avg_success = sum(success_rates) / len(success_rates) if success_rates else 0
            dropout_count = len([a for a in self.agents if getattr(a, 'inactive', False)])

            rq = compute_resilience_quotient(self.agents, avg_success, harmony, dropout_count)
            self.rq_history.append(rq)

            # Compute RO
            ro_value = calculate_reassignment_overhead(self.total_reassigned_tasks_step, self.total_tasks_assigned_step)
            self.ro_history.append(ro_value)

            self.print_agent_stats()
            print(f"\nRO: {ro_value:.3f}")
            print(f"RQ: {rq:.3f}")
            print(f"Harmony: {harmony:.3f}")

        print("\nSimulation completed.")

        self.save_agents()
        plot_sarsa_agents(
            self.agents,
            DATA_DIR,
            harmony_index_history=self.harmony_history,
            rq_history=self.rq_history,
            ro_history=self.ro_history
        )

