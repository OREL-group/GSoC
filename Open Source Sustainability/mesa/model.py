from mesa import Model
from agent import Contributor
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


class SimulationModel(Model):
    """OSS sustainability model"""

    def __init__(self, number_agents: int, width: int, height: int):
        self.num_agents = number_agents
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = (True)

        self.datacollector_currents = DataCollector(
            {
                "Retained Agents": SimulationModel.current_healthy_agents,
                "Non Retained Agents": SimulationModel.current_non_healthy_agents,
            }
        )

        # Create agents
        for i in range(self.num_agents):
            a = Contributor(i, self, self.random.randrange(4))
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
        self.datacollector_currents.collect(self)

        if SimulationModel.current_healthy_agents(self) == 1:
            self.running = False

    @staticmethod
    def current_healthy_agents(model) -> int:
        """Returns the total number of retianed contributors.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        return sum([1 for agent in model.schedule.agents if agent.health > 0])

    @staticmethod
    def current_non_healthy_agents(model) -> int:
        """Returns the total number of non retianed contributors.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        return sum([1 for agent in model.schedule.agents if agent.health == 0])