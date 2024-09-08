import os
from ray.rllib.algorithms.ppo import PPOConfig
from abm_rl.model import SustainabilityModel_RL
from ray.rllib.policy.policy import PolicySpec

def env_creator(_):
    # os.environ["RAY_DEDUP_LOGS"] = "0"

    return SustainabilityModel_RL(width=15, height=15, issue_density=0.7, contributor_density=0.1, maintainer_density=0.1, contributor_vision=7, maintainer_vision=7, threshold=70)

config = {
    "env_name": "OpenSourceSustainabilityModel-v0",
    "env_creator": env_creator,
    "framework": "torch",
    "train_batch_size": 250,
    "policies": {
        "policy_contributor": PolicySpec(config=PPOConfig.overrides(framework_str="torch")),
        "policy_maintainer": PolicySpec(config=PPOConfig.overrides(framework_str="torch"))
    },
    "policy_mapping_fn": lambda agent_id, *args, **kwargs: "policy_contributor" if agent_id[0:11]=="contributor" else "policy_maintainer",
    "policies_to_train": ["policy_contributor", "policy_maintainer"],
    # "num_gpus": int(os.environ.get("RLLIB_NUM_GPUS", "1")),
    "num_gpus": 0,  # Set to 0 to run on CPU
    "num_gpus_per_learner": 0,  # Set to 0 to avoid GPU allocation for learners
    "num_gpus_per_env_runner": 0,
    "num_learners": 10,
    "num_env_runners": 5,
    "num_envs_per_env_runner": 1,
    "batch_mode": "truncate_episodes",
    "rollout_fragment_length": "auto",
    # RAY_DEDUP_LOGS: 0
}