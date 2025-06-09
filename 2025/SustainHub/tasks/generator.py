import random

class Task:
    def __init__(self, task_type, difficulty):
        self.task_type = task_type
        self.difficulty = difficulty

def generate_task():
    task_type = random.choice(["bug", "feature", "docs"])
    difficulty = random.randint(1, 5)
    return Task(task_type, difficulty)