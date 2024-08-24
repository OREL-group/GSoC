from model import IssueTrackingModel
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserParam, Slider
from agent import IssueAgent, ContributorAgent, MaintainerAgent

simulation_params = {
    "n_contributors": Slider(
        "Number of contributors",
        value=10,
        min_value=5,
        max_value=50,
        step=1
    ),
    "n_issues": Slider(
        "Number of Issues",
        value=10,
        min_value=5,
        max_value=50,
        step=1
    ),
    "n_maintainers": Slider(
        "Number of maintainers",
        value=10,
        min_value=5,
        max_value=50,
        step=1
    ),
    "width": 80,
    "height": 80
}

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 1.0, "Layer": 0}
    # print(f"Agent: {agent}, Type: {type(agent)}")

    if isinstance(agent, IssueAgent):
        portrayal["Layer"] = 1
        if agent.difficulty == "Earth-shot":
            portrayal["Color"] = "yellow"
        elif agent.difficulty == "Moon-shot":
            portrayal["Color"] = "orange"
        elif agent.difficulty == "Mars-shot":
            portrayal["Color"] = "red"

    elif isinstance(agent, ContributorAgent):
        portrayal["Layer"] = 2
        if agent.skill_level == "Beginner":
            portrayal["Color"] = "blue"
        elif agent.skill_level == "Intermediate":
            portrayal["Color"] = "grey"
        elif agent.skill_level == "Advanced":
            portrayal["Color"] = "black"
    
    elif isinstance(agent, MaintainerAgent):
        portrayal["Layer"] = 3
        portrayal["Color"] = "green"
    
    return portrayal


grid = CanvasGrid(
    agent_portrayal,
    80,
    80,
    800,
    800,
)

chart_currents = ChartModule(
    [
        {"Label": "EarthIssues", "Color": "yellow"}, 
        {"Label": "MarsIssues", "Color": "orange"}, 
        {"Label": "MoonIssues", "Color": "red"},
        {"Label": "AcceptedPR", "Color": "black"},
    ],
    canvas_height=300,
    data_collector_name="datacollector", 
)

chart_currents_efficency = ChartModule(
    [
        {
            "Label": "Average_Efficiency", "Color": "maroon"
        }
    ],
    canvas_height=300,
    data_collector_name="datacollector"
)

chart_average_review = ChartModule(
    [
        {"Label": "Average_Resolution_Time", "Color": "purple"},
        {"Label": "Average_Review_Time", "Color": "pink"}
    ],
    canvas_height=300,
    data_collector_name="datacollector"
)

server = ModularServer(
    IssueTrackingModel,
    [grid, chart_currents, chart_currents_efficency, chart_average_review],
    "OSS Model",
    simulation_params,
)


server.port = 8521  # The default
server.launch()




    

