from simulation.simulation import Simulation

if __name__ == "__main__":
    sim = Simulation(agent_count=15)  
    sim.run(steps=7)
