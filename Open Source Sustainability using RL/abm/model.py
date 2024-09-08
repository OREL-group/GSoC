import mesa
import random

from abm.agent import Issue, Contributor, Maintainer


class SustainablilityModel(mesa.Model):

    def __init__(
            self,
            width,
            height,
            issue_density = 0.7,
            contributor_density = 0.1,
            maintainer_density = 0.1,
            contributor_vision = 7,
            maintainer_vision = 7,
            threshold = 70,
            movement = True,
            max_iters = 1000
    ):
        
        super().__init__()
        self.width = width
        self.height = height
        self.issue_density = issue_density
        self.contributor_density = contributor_density
        self.maintainer_density = maintainer_density
        self.contributor_vision = contributor_vision
        self.maintainer_vision = maintainer_vision
        self.threshold = threshold
        self.movement = movement
        self.max_iters = max_iters
        self.iteration = 0

        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(width, height, torus=True)

        model_reporters = {
            "Earth Issues": lambda m: SustainablilityModel.raised_PRs(m, "Earth"),
            "Moon Issues": lambda m: SustainablilityModel.raised_PRs(m, "Moon"),
            "Mars Issues": lambda m: SustainablilityModel.raised_PRs(m, "Mars"),
            "Accepted PRs": SustainablilityModel.accepted_PRs,
            "Average review time": SustainablilityModel.avg_review_time,
            "Average code efficiency": SustainablilityModel.compute_average_efficiency
        }

        agent_reporters = {
            "x": lambda a: a.pos[0] if a else None,
            "y": lambda a: a.pos[1] if a else None,
            "type": lambda a: type(a).__name__ if a else None,
            "status": lambda a: getattr(a, "status", None) if a else None,
            "difficulty": lambda a: getattr(a, "difficulty", None) if a else None,
            "code_efficiency": lambda a: getattr(a, "code_efficiency", None) if a else None
        }

        self.datacollector = mesa.DataCollector(
            model_reporters=model_reporters, agent_reporters=agent_reporters
        )

        unique_id = 0
        difficulties = ["Earth", "Moon", "Mars"]
        skill_level = ["Beginner", "Intermediate", "Advance"]
        if self.issue_density + self.contributor_density + self.maintainer_density > 1:
            raise ValueError("The sum of densities of all agents should be less than 1")
        for contents, (x,y) in self.grid.coord_iter():
            if self.random.random() < self.issue_density:
                issue = Issue(unique_id,
                              self,
                              (x,y),
                              difficulty=self.random.choice(difficulties),
                              priority=self.random.randint(1,8),
                              threshold=self.threshold
                            )
                unique_id += 1
                self.grid[x][y] = issue
                self.schedule.add(issue)
            
            elif self.random.random() < (self.issue_density + self.contributor_density):
                contributor = Contributor(unique_id, self, (x,y), self.contributor_vision, self.random.choice(skill_level))
                unique_id += 1
                self.grid[x][y] = contributor
                self.schedule.add(contributor)
            
            elif self.random.random() < (self.issue_density + self.contributor_density + self.maintainer_density):
                maintainer = Maintainer(unique_id, self, (x,y), vision=self.maintainer_vision)
                unique_id += 1
                self.grid[x][y] = maintainer
                self.schedule.add(maintainer)
        
        self.running = True
        # self.datacollector.collect(self)
    
    def step(self):
        self.schedule.step()
        self.agents.shuffle().do("step")
        self.datacollector.collect(self)
        # data = self.datacollector.get_agent_vars_dataframe()
        # print(data.head())
        self.iteration =+ 1
        if self.iteration > self.max_iters:
            self.running = False

    @staticmethod
    def raised_PRs(model, difficulty) -> int:
        return sum(1 for agent in model.schedule.agents if isinstance(agent, Issue) and agent.status == "Solved" and agent.difficulty == difficulty)
        
    @staticmethod
    def accepted_PRs(model) -> int:
        return sum(1 for agent in model.schedule.agents if isinstance(agent, Issue) and agent.status == "Closed")
        
    @staticmethod
    def compute_average_efficiency(model) -> float:
        efficiencies = [
            agent.code_efficiency
            for agent in model.schedule.agents
            if isinstance(agent, Issue) and agent.status == "Solved"
        ]
        if efficiencies:
            return sum(efficiencies)/len(efficiencies)
        return 0
        
    @staticmethod
    def avg_review_time(model) -> float:
        reviewed_issues = [agent for agent in model.schedule.agents if isinstance(agent, Issue) and agent.status == "Closed"]
        if not reviewed_issues:
            return 0
            
        total_time = sum((agent.closing_time - agent.opening_time) for agent in reviewed_issues)
        return total_time/len(reviewed_issues)
                
        
        
            