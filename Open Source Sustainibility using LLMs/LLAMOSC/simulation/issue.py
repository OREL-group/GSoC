from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Issue:
    id: int
    difficulty: int
    filepath: str
    subtasks: List[Dict[str, Any]] = field(default_factory=list, init=False)
    is_collaborative: bool = field(default=False, init=False)
    
    def split_for_collaboration(self, agent1, agent2):
        """Issue #64: Split into 2 subtasks for collaboration"""
        self.subtasks = [
            {'description': 'Core implementation', 'agent': agent1},
            {'description': 'Testing + refactoring', 'agent': agent2}
        ]
        self.is_collaborative = True
        print(f"Issue {self.id} split for collaboration: {len(self.subtasks)} subtasks")

