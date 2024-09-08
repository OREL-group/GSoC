# import numpy as np

def create_initial_agents(self, Issue_RL, Contributor_RL, Maintainer_RL):

    unique_id = 0
    difficulties = ["Earth", "Moon", "Mars"]
    skill_level = ["Beginner", "Intermediate", "Advance"]

    if self.issue_density + self.contributor_density + self.maintainer_density > 1:
        raise ValueError("The sum of density of all agents should be less than one")
    issues = []
    contributors = []
    maintainers = []

    for contents, (x,y) in self.grid.coord_iter():
        if self.random.random() < self.issue_density:
                unique_id_str = f"issue_{unique_id}"
                issue = Issue_RL(unique_id_str,
                              self,
                              (x,y),
                              difficulty=self.random.choice(difficulties),
                              priority=self.random.randint(1,8),
                              threshold=self.threshold
                            )
                unique_id += 1
                self.grid[x][y] = issue
                issues.append(issue)
        
        elif self.random.random() < (self.issue_density + self.contributor_density):
                unique_id_str = f"contributor_{unique_id}"
                contributor = Contributor_RL(unique_id_str, self, (x,y), self.contributor_vision, self.random.choice(skill_level))
                unique_id += 1
                self.grid[x][y] = contributor
                contributors.append(contributor)
        
        elif self.random.random() < (self.issue_density + self.contributor_density + self.maintainer_density):
                unique_id_str = f"maintainer_{unique_id}"
                maintainer = Maintainer_RL(unique_id_str, self, (x,y), vision=self.maintainer_vision)
                unique_id += 1
                self.grid[x][y] = maintainer
                maintainers.append(maintainer)
        
    for issue in issues:
          self.schedule.add(issue)
    for contributor in contributors:
          self.schedule.add(contributor)
    for maintainer in maintainers:
          self.schedule.add(maintainer)
    
def grid_to_observation(self, Issue_RL):
    self.obs_grid = []
    for i in self.grid._grid:
        row = []
        for j in i:
            if j is None:
                row.append(0)
            elif isinstance(j, Issue_RL):
                if j.status == "Open":
                    row.append(2)
                elif j.status == "Solved":
                    row.append(1)
                elif j.status == "Closed":
                    row.append(4)
            else:
                row.append(3)

        self.obs_grid.append(row)



def move(self, action, empty_neighbors):
    if action == 0:
        new_position = (self.pos[0] + 1, self.pos[1])  # Move right
    elif action == 1:
        new_position = (self.pos[0] - 1, self.pos[1])  # Move left
    elif action == 2:
        new_position = (self.pos[0], self.pos[1] - 1)  # Move up
    elif action == 3:
        new_position = (self.pos[0], self.pos[1] + 1)  # Move down
    else:
        new_position = self.pos  # Don't move
    new_position = (new_position[0] % self.model.grid.width, new_position[1] % self.model.grid.height)  # Wrap around the grid
    if new_position in empty_neighbors:
        self.model.grid.move_agent(self, new_position)  # Move to the new position
    
    
                

                    