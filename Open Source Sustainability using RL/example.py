from abm_rl.model import SustainabilityModel_RL
from abm_rl.server import run_model
from abm_rl.train_config import config
from train import train_model

env = SustainabilityModel_RL()
observation, info = env.reset(seed=42)

for _ in range(10):
    action_dict = {}
    for agent in env.schedule.agents:
        action_dict[agent.unique_id] = env.action_space.sample()
        # print(1)
    observation, reward, terminated, truncated, info = env.step(action_dict)

    if terminated or truncated:
        observation, info = env.reset()

train_model(config, num_iterations=1, result_path='results.txt', checkpoint_dir='checkpoints')

server = run_model(model_path='checkpoints')
server.port = 6005
server.launch(open_browser=True)

