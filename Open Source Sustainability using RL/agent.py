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
        self.move()
        self.check_issue()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def check_issue(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if isinstance(agent, IssueAgent) and agent.marked_for_review == False:
                agent.marked_for_review = True
                agent.code_efficiency = random.randint(1, 100)  # Assign efficiency when marked for review
                agent.marked_time = self.model.schedule.time
                print(f'{self.skill_level} ContributorAgent {self.unique_id} found {agent.difficulty} IssueAgent {agent.unique_id} at {self.pos} and marked it for review with efficiency {agent.code_efficiency}')

class MaintainerAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        self.move()
        self.check_issue_for_review()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def check_issue_for_review(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if isinstance(agent, IssueAgent) and agent.marked_for_review and agent.pr_accepted == False:
                print(f'Maintainer {self.unique_id} found marked {agent.difficulty} IssueAgent {agent.unique_id} at {self.pos} with efficiency {agent.code_efficiency}')
                if agent.code_efficiency > 50:
                    agent.pr_accepted = True
                    agent.review_time = self.model.schedule.time
                    self.model.high_efficiency_issues.append(agent.unique_id)
                else:
                    agent.marked_for_review = False


