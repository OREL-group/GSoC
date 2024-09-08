import mesa
from mesa.visualization import Slider, Checkbox, CanvasGrid, ChartModule, ModularServer
import ray
from ray.rllib.algorithms.algorithm import Algorithm
from abm_rl.agent import Issue_RL
from abm_rl.model import SustainabilityModel_RL
from abm_rl.utility import grid_to_observation
from ray import tune
import numpy as np
from abm.server import agent_portrayal
import os

ray.init()


class SustainabilityModelServer(SustainabilityModel_RL):

    def __init__(self, height=15, width=15, issue_density=0.7,contributor_density=0.1, maintainer_density=0.1, contributor_vision=7, maintainer_vision=7, threshold=70, movement=True, max_iters=200, model_path=None):
        super().__init__(height, width, issue_density, contributor_density, maintainer_density, contributor_vision, maintainer_vision, threshold, movement, max_iters)
        self.running = True
        self.iteration = 0
        def env_creator(_):
            return SustainabilityModel_RL(height, width, issue_density, contributor_density, maintainer_density, contributor_vision, maintainer_vision, threshold, movement, max_iters)
        tune.register_env("OpenSourceSustainabilityModel-v0", env_creator)
        checkpoint_path = model_path
        algo = Algorithm.from_checkpoint(checkpoint_path)
        self.contributor_policy = algo.get_policy("policy_contributor")
        self.maintainer_policy = algo.get_policy("policy_maintainer")

    def step(self):
        if self.iteration == 0:
            self.reset()
        grid_to_observation(self, Issue_RL)
        observation = {}
        for agent in self.schedule.agents:
            observation[agent.unique_id] = [self.obs_grid[neighbor[0]][neighbor[1]] for neighbor in agent.neighborhood]  
            # print("unique_id: ",agent.unique_id)
        
        action_dict = {}
        for agent in self.schedule.agents:
            if agent.unique_id.startswith("contributor"):
                action_dict[agent.unique_id] = self.contributor_policy.compute_single_action(np.array(observation[agent.unique_id]).T, explore=False)[0]
            elif agent.unique_id.startswith("maintainer"):
                action_dict[agent.unique_id] = self.maintainer_policy.compute_single_action(np.array(observation[agent.unique_id]).T, explore=False)[0]
            else:
                pass
        self.action_dict = action_dict

        self.schedule.step()
        self.datacollector.collect(self)
        self.iteration += 1
        if self.iteration > self.max_iters:
            self.running = False
        
model_params = {
    "width": 40,
    "height": 40,
    "model_path": None,
    "issue_density": Slider(
        "Initial issue density", 0.7, 0.0, 0.9, 0.1
    ),
    "contributor_density": Slider(
        "Initial contributor density", 0.07, 0.0, 0.1, 0.01
    ),
    "maintainer_density": Slider(
        "Initial maintainer density", 0.07, 0.0, 0.1, 0.01
    ),
    "contributor_vision": Slider(
        "Contributor vision", 7, 1, 10, 1
    ),
    "maintainer_vision": Slider(
        "Maintainer vision", 7, 1, 10, 1
    ),
    "threshold": Slider(
        "Threshold code efficiency", 70, 50, 100, 10
    ),
    "movement": Checkbox("Allow contributor movement", True)
}

grid = CanvasGrid(agent_portrayal, 40, 40, 480, 480)

chart_raised_PRs = ChartModule(
    [
        {"Label": "Earth Issues", "Color": "yellow"},
        {"Label": "Moon Issues", "Color": "orange"},
        {"Label": "Mars Issues", "Color": "red"},
        {"Label": "Accepted PRs", "Color": "black"},
    ],
    data_collector_name="datacollector"
)

chart_code_efficiency = ChartModule(
    [
        {"Label": "Average code efficiency", "Color": "maroon"}
    ],
    data_collector_name="datacollector"
)

chart_review_time = ChartModule(
    [
        {"Label": "Average review time", "Color": "purple"}
    ],
    data_collector_name="datacollector"
)

def run_model(height = 40, width = 40, model_path = None):
    model_params["height"] = height
    model_params["width"] = width
    model_params["model_path"] = model_path
    server = ModularServer(
    SustainabilityModelServer,
    [grid, chart_raised_PRs, chart_code_efficiency, chart_review_time],
    "OSS Model",
    model_params
    )

    return server
            