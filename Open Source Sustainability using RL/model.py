from agent import IssueAgent, ContributorAgent, MaintainerAgent
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class IssueTrackingModel(Model):
    def __init__(self, n_contributors, n_issues, n_maintainers, width, height):
        super().__init__()  # Ensure the Model class is correctly initialized
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.high_efficiency_issues = []

        # Define classifications for agents
        skill_levels = ['Beginner', 'Intermediate', 'Advanced']
        difficulties = ['Earth-shot', 'Moon-shot', 'Mars-shot']

        # Create issue agents
        for i in range(n_issues):
            difficulty = self.random.choice(difficulties)
            issue = IssueAgent(i, self, difficulty)
            self.schedule.add(issue)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(issue, (x, y))

        # Create contributor agents
        for i in range(n_contributors):
            skill_level = self.random.choice(skill_levels)
            contributor = ContributorAgent(i + n_issues, self, skill_level)
            self.schedule.add(contributor)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(contributor, (x, y))

        # Create maintainer agents
        for i in range(n_maintainers):
            maintainer = MaintainerAgent(i + n_issues + n_contributors, self)
            self.schedule.add(maintainer)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(maintainer, (x, y))
        
        self.datacollector = DataCollector(
            {
             "EarthIssues": IssueTrackingModel.compute_earth_issues,
             "MarsIssues": IssueTrackingModel.compute_mars_issues,
             "MoonIssues": IssueTrackingModel.compute_moon_issues,
             "AcceptedPR": IssueTrackingModel.accepted_PR,
             "Average_Efficiency": IssueTrackingModel.compute_average_efficiency,
             "Average_Resolution_Time": IssueTrackingModel.avg_resolution_time,
             "Average_Review_Time": IssueTrackingModel.avg_review_time
            }
        )

        # self.datacollector_codeEfficiency = DataCollector(
        #     {
        #         "Average_Efficiency": IssueTrackingModel.compute_average_efficiency
        #     }
        # )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        # Add print statements to see output
        for agent in self.schedule.agents:
            if isinstance(agent, IssueAgent):
                print(f'{agent.difficulty} IssueAgent {agent.unique_id} at {agent.pos} marked for review: {agent.marked_for_review}')
            # elif isinstance(agent, ContributorAgent):
            #     print(f'{agent.skill_level} ContributorAgent {agent.unique_id} at {agent.pos}')
            # elif isinstance(agent, MaintainerAgent):
            #     print(f'MaintainerAgent {agent.unique_id} at {agent.pos}')

    @staticmethod
    def compute_moon_issues(model) -> int:
        return sum(1 for agent in model.schedule.agents if isinstance(agent, IssueAgent) and agent.marked_for_review and agent.difficulty == 'Moon-shot')
    
    @staticmethod
    def compute_mars_issues(model) -> int:
        return sum(1 for agent in model.schedule.agents if isinstance(agent, IssueAgent) and agent.marked_for_review and agent.difficulty == 'Mars-shot')
    
    @staticmethod
    def compute_earth_issues(model) -> int:
        return sum(1 for agent in model.schedule.agents if isinstance(agent, IssueAgent) and agent.marked_for_review and agent.difficulty == 'Earth-shot')
    
    @staticmethod
    def accepted_PR(model) -> int:
        return sum(1 for agent in model.schedule.agents if isinstance(agent, IssueAgent) and agent.pr_accepted)
    
    @staticmethod
    def compute_average_efficiency(model) -> float:
        efficiencies = [
            agent.code_efficiency
            for agent in model.schedule.agents
            if isinstance(agent, IssueAgent) and agent.marked_for_review
        ]
        if efficiencies:
            return sum(efficiencies) / len(efficiencies)
        return 0  # If there are no efficiencies recorded, return 0
    
    @staticmethod
    def avg_resolution_time(model) -> float:
        resolved_issues = [agent for agent in model.schedule.agents if isinstance(agent, IssueAgent) and agent.marked_time is not None]
        if not resolved_issues:
            return 0
        total_time = sum((agent.marked_time - agent.creation_time) for agent in resolved_issues)
        return total_time / len(resolved_issues)

    @staticmethod
    def avg_review_time(model) -> float:
        reviewed_issues = [agent for agent in model.schedule.agents if isinstance(agent, IssueAgent) and agent.review_time is not None]
        if not reviewed_issues:
            return 0
        total_time = sum((agent.review_time - agent.marked_time) for agent in reviewed_issues)
        return total_time / len(reviewed_issues)



if __name__ == "__main__":
    # Parameters: width, height, number of contributors, number of issues, number of maintainers
    model = IssueTrackingModel(10, 10, 5, 10, 3)
    
    for i in range(50):
        print(f'Step {i}')
        model.step()

    print("PRs Accepted (efficiency > 70):", model.high_efficiency_issues)