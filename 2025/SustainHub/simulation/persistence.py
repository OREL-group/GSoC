import json
import os

def save_agents(agents, filepath="data/trained_agents.json"):
    data = [agent.to_dict() for agent in agents]
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def load_agents(agents, filepath="data/trained_agents.json"):
    if not os.path.exists(filepath):
        return
    with open(filepath, "r") as f:
        data = json.load(f)
    name_map = {agent.name: agent for agent in agents}
    for entry in data:
        if entry["name"] in name_map:
            name_map[entry["name"]].load_from_dict(entry)
