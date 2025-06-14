from agents.maintainer import Maintainer
from agents.contributor import Contributor
from agents.innovator import Innovator
from agents.knowledge_curator import KnowledgeCurator
from tasks.generator import generate_task
from tasks.mab import MABAllocator
import random

class Simulation:
    def __init__(self):
        self.agents = [
            Maintainer("Alice"),
            Contributor("Bob"),
            Innovator("Charlie"),
            KnowledgeCurator("Vidhi")
        ]
        self.task_queue = [generate_task() for _ in range(7)]
        self.mab_allocator = MABAllocator(self.agents)
        
    def assign_tasks(self):
        for task in self.task_queue:
            selected_agent = self.mab_allocator.select_agent(task)
            if selected_agent and selected_agent.assign_task(task):
                print(f"Assigned {task.task_type} task to {selected_agent.name}")
            else:
                print(f"No available agent for {task.task_type} task")
        
        self.task_queue.clear()
    
    def simulate_task_completion(self):
        """Simulate agents completing tasks and reporting success/failure"""
        for agent in self.agents:
            if agent.task_load > 0:
                # Simulate completing one random task
                task_type = random.choice(["bug", "feature", "docs"])
                success = random.random() > 0.3  # 70% success rate for demo
                agent.complete_task(success, task_type)
                print(f"{agent.name} completed a {task_type} task {'successfully' if success else 'unsuccessfully'}")
    
    def run(self, steps=5):
        print("Simulation starting...\n")
        for step in range(steps):
            print(f"\n--- Step {step + 1} ---")
            # Generate new tasks each step
            self.task_queue = [generate_task() for _ in range(3)]
            self.assign_tasks()
            self.simulate_task_completion()

if __name__ == "__main__":
    sim = Simulation()
    sim.run()