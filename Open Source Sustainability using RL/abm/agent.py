import mesa
import random

class Issue(mesa.Agent):
    # A random issue in the repository, may or may not be solved
    

    def __init__(
        self,
        unique_id,
        model,
        pos,
        difficulty,
        priority,
        threshold,
    ):
        super().__init__(unique_id, model)
        self.difficulty = difficulty
        self.pos = pos
        self.status = "Open"
        self.priority = priority
        self.threshold = threshold
        self.opening_time = self.model.schedule.time
        self.closing_time = None
        self.code_efficiency = None

    def step(self):
        pass

    def update_neighbors(self):
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, radius=7
        )
        self.neighbors = self.model.grid.get_cell_list_contents(self.neighborhood)
        self.empty_neighbors = [
            c for c in self.neighborhood if self.model.grid.is_cell_empty(c)
        ]

class Contributor(mesa.Agent):

    def __init__(self, unique_id, model, pos, vision, skill):
        super().__init__(unique_id, model)
        self.pos = pos
        self.vision = vision
        self.skill = skill

    def step(self):
        self.update_neighbors()
        active_neighbors = []

        for agent in self.neighbors:
            if(
                isinstance(agent, Issue)
                and agent.status == "Open"
            ):
                active_neighbors.append(agent)
        
        if active_neighbors:
            selected_issue = self.random.choice(active_neighbors)
            selected_issue.status = "Solved"
            print(selected_issue.status)
            if (self.skill == "Beginner"):
                code_quality = self.random.randint(40, 80)
            elif (self.skill == "Intermediate"):
                code_quality = self.random.randint(50, 90)
            else:
                code_quality = self.random.randint(60, 100)
            selected_issue.code_efficiency = code_quality
        
        if self.model.movement and self.empty_neighbors:
            new_pos = self.random.choice(self.empty_neighbors)
            self.model.grid.move_agent(self, new_pos)
            

    def update_neighbors(self):
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, radius=self.vision
        )
        self.neighbors = self.model.grid.get_cell_list_contents(self.neighborhood)
        self.empty_neighbors = [
            c for c in self.neighborhood if self.model.grid.is_cell_empty(c)
        ]

class Maintainer(mesa.Agent):
    def __init__(self, unique_id, model, pos, vision):
        super().__init__(unique_id,model)
        self.pos = pos
        self.vision = vision
    
    def step(self):
        self.update_neighbors()
        active_neighbors = []

        for agent in self.neighbors:
            if(
                isinstance(agent, Issue)
                and agent.status == "Solved"
            ):
                active_neighbors.append(agent)
        
        if active_neighbors:
            selected_issue = self.random.choice(active_neighbors)
            if(selected_issue.code_efficiency >= 70):
                selected_issue.status = "Closed"
                selected_issue.closing_time = self.model.schedule.time
                # print(selected_issue.closing_time)
            else:
                selected_issue.status = "Open"
            
            print(selected_issue.status)

        if self.model.movement and self.empty_neighbors:
            new_pos = self.random.choice(self.empty_neighbors)
            self.model.grid.move_agent(self, new_pos)

    def update_neighbors(self):
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, radius=self.vision
        )
        self.neighbors = self.model.grid.get_cell_list_contents(self.neighborhood)
        self.empty_neighbors = [
            c for c in self.neighborhood if self.model.grid.is_cell_empty(c)
        ]
