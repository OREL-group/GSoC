import numpy as np

class BaseAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.task_load = 0
        self.max_load = 5  
        self.success_counts = np.zeros(3)  
        self.total_counts = np.zeros(3)   
        self.expertise_level = 1  


    def assign_task(self, task):
        if self.task_load < self.max_load:
            self.task_load += 1
            return True
        return False

    def complete_task(self, success, task_type):
        self.task_load -= 1
        task_idx = self._task_type_to_idx(task_type)
        self.total_counts[task_idx] += 1
        if success:
            self.success_counts[task_idx] += 1
        

    def get_success_rate(self, task_type):
        task_idx = self._task_type_to_idx(task_type)
        total = self.total_counts[task_idx]
        return self.success_counts[task_idx] / total if total > 0 else 0.5  # Default to 0.5 if no data

    def _task_type_to_idx(self, task_type):
        if task_type == "bug":
            return 0
        elif task_type == "feature":
            return 1
        return 2  # docs
