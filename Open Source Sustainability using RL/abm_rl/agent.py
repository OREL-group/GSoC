from abm.agent import Issue, Contributor, Maintainer
from abm_rl.utility import move
class Issue_RL(Issue):

    def step(self):
        self.update_neighbors()

class Contributor_RL(Contributor):

    def __init__(self, unique_id, model, pos, vision, skill):
        super().__init__(unique_id, model, pos, vision, skill)
        self.issue_solved = False  # Initialize the attribute

    def step(self):
        action_tuple = self.model.action_dict[self.unique_id]
        issue_pos = self.neighborhood[action_tuple[0]]
        for agent in self.model.grid.get_cell_list_contents(self.neighborhood):
            if isinstance(agent, Issue) and agent.status == "Open" and agent.pos == issue_pos:
                agent.status = "Solved"
                self.issue_solved = True
                if (self.skill == "Beginner"):
                    code_quality = self.random.randint(40, 80)
                elif (self.skill == "Intermediate"):
                    code_quality = self.random.randint(50, 90)
                else:
                    code_quality = self.random.randint(60, 100)
                agent.code_efficiency = code_quality
        
        self.update_neighbors()
        action = self.model.action_dict.get(self.unique_id, 0)

        if self.model.movement:
            move(self, action, self.empty_neighbors)
            # move(self, self.model.action_dict[self.unique_id[1], self.empty_neighbors])
        
        self.update_neighbors()


class Maintainer_RL(Maintainer):

    def __init__(self, unique_id, model, pos, vision):
        super().__init__(unique_id, model, pos, vision)
        self.issue_reviewed = False

    def step(self):
        action_tuple = self.model.action_dict[self.unique_id]
        issue_pos = self.neighborhood[action_tuple[0]]
        for agent in self.model.grid.get_cell_list_contents(self.neighborhood):
            if isinstance(agent, Issue) and agent.status == "Solved" and agent.code_efficiency >= 70 and agent.pos == issue_pos:
                agent.status = "Closed"
                self.issue_reviewed = True
                agent.closing_time = self.model.schedule.time
                print(agent.status)

            else:
                agent.status = "Open"        
        self.update_neighbors()
        action = self.model.action_dict.get(self.unique_id, 0)

        if self.model.movement:
            move(self, action, self.empty_neighbors)
            # move(self, self.model.action_dict[self.unique_id[1], self.empty_neighbors])
            # self.model.action_dict[self.unique_id[1]

        self.update_neighbors()
