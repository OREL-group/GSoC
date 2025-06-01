from agents.maintainer import Maintainer
from agents.contributor import Contributor
from agents.innovator import Innovator
from agents.knowledge_curator import KnowledgeCurator
from tasks.generator import generate_task

class Simulation:
    def __init__(self):
        self.agents = [
            Maintainer("Alice"),
            Contributor("Bob"),
            Innovator("Charlie"),
            KnowledgeCurator("Vidhi")
        ]
        self.task_queue = [generate_task() for _ in range(5)]

    def assign_tasks(self):
        for task in self.task_queue:
            available_agent = min(self.agents, key=lambda agent: agent.task_load)
            available_agent.assign_task(task)
        self.task_queue.clear()

    def run(self):
        print("Simulation starting...\n")
        self.assign_tasks()

if __name__ == "__main__":
    sim = Simulation()
    sim.run()
