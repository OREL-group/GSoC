from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import NumberInput

from model import SimulationModel
from mesa.visualization.modules import CanvasGrid, ChartModule

NUMBER_OF_CELLS = 10
SIZE_OF_CANVAS_IN_PIXELS_X = 700
SIZE_OF_CANVAS_IN_PIXELS_Y = 550

simulation_params = {
    "number_agents": NumberInput(
        "Choose how many agents to include in the model", value=NUMBER_OF_CELLS
    ),
    "width": NUMBER_OF_CELLS,
    "height": NUMBER_OF_CELLS,
}


def agent_portrayal(agent):
    # if the agent is buried we put it as white, not showing it.
    if agent.buried:
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Color": "white",
            "r": 0.01,
            "text": "",
            "Layer": 0,
            "text_color": "black",
        }
        return portrayal

    # the default config is a circle
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5,
        "text": f"{agent.health} Type: {agent.type}",
        "text_color": "black",
    }

    # if the agent is dead on the floor we change it to a black rect
    if agent.dead:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.2
        portrayal["h"] = 0.2
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1

        return portrayal

    # if the agent is retained we set its radius according to the its type
    if agent.type == 0:
        portrayal["r"] = 0.2

    elif agent.type == 1:
        portrayal["r"] = 0.4

    elif agent.type == 2:
        portrayal["r"] = 0.6

    elif agent.type == 3:
        portrayal["r"] = 0.9

    # according to the level 0 health of the agent we change the color of it
    if agent.health > 50:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1

    else:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 2

    return portrayal


grid = CanvasGrid(
    agent_portrayal,
    NUMBER_OF_CELLS,
    NUMBER_OF_CELLS,
    SIZE_OF_CANVAS_IN_PIXELS_X,
    SIZE_OF_CANVAS_IN_PIXELS_Y,
)

chart_healthy = ChartModule(
    [
        {"Label": "Retained Agents", "Color": "green"},
        {"Label": "Non Retained Agents", "Color": "red"},
    ],
    canvas_height=300,
    data_collector_name="datacollector_currents",
)


server = ModularServer(
    SimulationModel,
    [grid, chart_healthy],
    "OSS Sustainability Model",
    simulation_params,
)
server.port = 8521
server.launch()