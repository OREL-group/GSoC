import mesa
from mesa.visualization import Slider, Checkbox, CanvasGrid, ChartModule, ModularServer
from . agent import Issue, Contributor, Maintainer
from . model import SustainablilityModel

def agent_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {
        "Shape": "circle",
        "x": agent.pos[0],
        "y": agent.pos[1],
        "Filled": "true"
    }

    if isinstance(agent, Issue):
        portrayal["Layer"] = 1
        if agent.difficulty == "Earth":
            portrayal["Color"] = "yellow"
            portrayal["r"] = 0.7
        elif agent.difficulty == "Moon":
            portrayal["Color"] = "orange"
            portrayal["r"] = 0.8
        elif agent.difficulty == "Mars":
            portrayal["Color"] = "red"
            portrayal["r"] = 0.9
    
    elif isinstance(agent, Contributor):
        portrayal["Layer"] = 2
        portrayal["Color"] = "blue"
        portrayal["r"] = 0.5
    
    elif isinstance(agent, Maintainer):
        portrayal["Layer"] = 3
        portrayal["Color"] = "green"
        portrayal["r"] = 0.4
    
    return portrayal

model_params = {
    "width": 40,
    "height": 40,
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

server = ModularServer(
    SustainablilityModel,
    [grid, chart_raised_PRs, chart_code_efficiency, chart_review_time],
    "OSS Model",
    model_params
)


