from pynetlogo import NetLogoLink
import os

class NetLogoVisualizer:
    def __init__(self, agent_data):
        self.netlogo = NetLogoLink(gui=True)
        self.agent_data = agent_data
        self.model_path = os.path.join(os.getcwd(), 'SustainHub.nlogo')
        self.netlogo.load_model(self.model_path)

    def setup_agents(self):
        self.netlogo.command('clear-all')
        self.netlogo.command(f'create-turtles {len(self.agent_data)}')

        for i, agent in enumerate(self.agent_data):
            role = agent['role']
            self.netlogo.command(f'ask turtle {i} [ setxy random-xcor random-ycor set role "{role}" ]')

            if role == "Contributor":
                color = "blue"
            elif role == "Maintainer":
                color = "green"
            else:
                color = "red"

            self.netlogo.command(f'ask turtle {i} [ set color {color} ]')

        self.netlogo.command('reset-ticks')

    def run_steps(self, steps=10):
        for _ in range(steps):
            self.netlogo.command('go')

    def close(self):
        self.netlogo.kill_workspace()