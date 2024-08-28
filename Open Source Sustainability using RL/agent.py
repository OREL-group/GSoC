from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random

class IssueAgent(Agent):
    def __init__(self, unique_id, model, difficulty):
        super().__init__(unique_id, model)
        self.marked_for_review = False
        self.difficulty = difficulty  # Difficulty levels: Mars-shot, Moon-shot, Earth-shot
        self.code_efficiency = None  # Initially, no efficiency value
        self.pr_accepted = False
        self.creation_time = self.model.schedule.time  # Time when the issue is created
        self.marked_time = None  # Time when the issue is marked for review
        self.review_time = None  # Time when the issue is reviewed
        self.c

    def step(self):
        # if self.marked_for_review and self.pr_accepted:
        #     self.model.grid.remove_agent(self)
        #     self.model.schedule.remove(self)  
        pass

class ContributorAgent(Agent):
    def __init__(self, unique_id, model, skill_level):
        super().__init__(unique_id, model)
        self.skill_level = skill_level  # Skill levels: Beginner, Intermediate, Advanced

    def step(self):
        action_tuple = self.model.action_dict[self.unique_id]
        issue_pos = self.neighborhood[action_tuple[0]]
        for agent in self.model.grid.get_cell_list_contents(self.neighborhood):
            if isinstance(agent, IssueAgent) and agent.marked_for_review == False and agent.pos == issue_pos:
                agent.marked_for_review == True
                agent.code_efficiency == random.randint(1, 100)
                agent.marked_time = self.model.schedule.time
                break
        self.update_neighbors()
        # Move based on action
        if self.model.movement:
            move(self, self.model.action_dict[self.unique_id][1], self.empty_neighbors)
        # Update the neighbors for observation space
        self.update_neighbors()
class MaintainerAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        action_tuple = self.model.action_dict[self.unique_id]
        issue_pos = self.neighborhood[action_tuple[0]]
        for agent in self.model.grid.get_cell_list_contents(self.neighborhood):
            if isinstance(agent, IssueAgent) and agent.marked_for_review and agent.pr_accepted == False and agent.pos == issue_pos:
                if agent.code_efficiency>70:
                    agent.pr_accepted = True
                    agent.review_time = self.model.schedule.time
                else:
                    agent.marked_for_review = False
        
        self.update_neighbors()
        # Move based on action
        if self.model.movement:
            move(self, self.model.action_dict[self.unique_id][1], self.empty_neighbors)
        # Update the neighbors for observation space
        self.update_neighbors()


