class BaseAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.expertise_level = "Apprentice"
        self.task_load = 0
        self.success_rate = 0.5  # initial average performance

    def assign_task(self, task):
        self.task_load += 1
        print(f"[{self.role}] {self.name} assigned task: {task['type']}")

    def complete_task(self, task):
        self.task_load -= 1
        print(f"[{self.role}] {self.name} completed task: {task['type']}")
