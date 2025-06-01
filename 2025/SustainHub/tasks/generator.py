import random

TASK_TYPES = ["bug_fix", "feature", "docs"]

def generate_task():
    task_type = random.choice(TASK_TYPES)
    difficulty = random.choice(["easy", "medium", "hard"])
    return {"type": task_type, "difficulty": difficulty}
