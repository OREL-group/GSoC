import mesa
import numpy as np
import gymnasium as gym
from ray.rllib.env import MultiAgentEnv
from abm_rl.agent import Issue_RL, Contributor_RL, Maintainer_RL
from abm.model import SustainablilityModel
from abm_rl.utility import grid_to_observation, create_initial_agents


class SustainabilityModel_RL(SustainablilityModel, MultiAgentEnv):

    def __init__(
            self,
            width = 15,
            height = 15,
            issue_density = 0.7,
            contributor_density = 0.1,
            maintainer_density = 0.1,
            contributor_vision = 7,
            maintainer_vision = 7,
            threshold = 70,
            movement = True,
            max_iters = 200
    ):
        
        super().__init__(width, height, issue_density, contributor_density, maintainer_density, contributor_vision, maintainer_vision, threshold, movement, max_iters)

        self.observation_space = gym.spaces.Box(low=0, high=4, shape=(224,), dtype=np.float32)
        self.action_space = gym.spaces.Tuple((gym.spaces.Discrete(8), gym.spaces.Discrete(5)))

    def step(self, action_dict):

        self.action_dict = action_dict

        self.schedule.step()
        self.datacollector.collect(self)
        
        rewards = self.cal_reward()

        grid_to_observation(self, Issue_RL)
        observation = {}

        for agent in self.schedule.agents:
            count = 0
            observation[agent.unique_id] = [self.obs_grid[neighbor[0]][neighbor[1]] for neighbor in agent.neighborhood]
            # print("agent: ", agent.unique_id)
            # for neighbor in agent.neighborhood:
            #     # print("neighbor ", neighbor)
            #     count += 1
            # print(count)
            # print("unique_id: ",neighbor[0])

        done = {a.unique_id: False for a in self.schedule.agents}
        truncated = {a.unique_id: False for a in self.schedule.agents}
        truncated['__all__'] = np.all(list(truncated.values()))
        done['__all__'] = True if self.schedule.time > self.max_iters else False

        return observation, rewards, done, truncated, {}
    
    def cal_reward(self):
        rewards = {}
        for agent in self.schedule.agents:
            if isinstance(agent, Contributor_RL):
                if agent.issue_solved:
                    rewards[agent.unique_id] = 1
                else:
                    rewards[agent.unique_id] = 0
        
            elif isinstance(agent, Maintainer_RL):
                if agent.issue_reviewed:
                    rewards[agent.unique_id] = 1
                else:
                    rewards[agent.unique_id] = 0
            
            else:
                pass

        return rewards

    def reset(self, *, seed=None, options=None):

        super().reset()

        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(self.width, self.height, torus=True)
        create_initial_agents(self, Issue_RL, Contributor_RL, Maintainer_RL)
        grid_to_observation(self, Issue_RL)

        self.action_dict = {a.unique_id: (0,0) for a in self.schedule.agents}

        for agent in self.schedule.agents:
            agent.update_neighbors()

        self.schedule.step()
        observation = {}

        for agent in self.schedule.agents:
            observation[agent.unique_id] = [self.obs_grid[neighbor[0]][neighbor[1]] for neighbor in agent.neighborhood]
            # print("unique_id: ",agent.unique_id)
        return observation, {}
