## Usage

This project simulates an open-source community with different agent roles and task assignments using reinforcement learning techniques like Multi-Armed Bandits (MAB) for task allocation.

### How to run the simulation

1. **Clone the repository**

    ```bash
    git clone https://github.com/OREL-group/GSoC.git
    cd GSoC/2025/SustainHub
    ```

2. **Make sure you have Python 3 installed** (preferably 3.7 or higher).

3. **Install required dependencies** (if any, e.g., numpy):

    ```bash
    pip install numpy
    ```

4. **Run the simulation script:**

    ```bash
    python3 simulation.py
    ```

### What happens during the simulation

- Agents represent different community roles: Maintainer, Contributor, Innovator, and Knowledge Curator.
- Tasks (bugs, features, documentation) are assigned to agents.
- The assignment is dynamically improved by leveraging Multi-Armed Bandit algorithms, allowing agents to learn and optimize task success rates.
- The simulation outputs task assignments and whether tasks were completed successfully step-by-step.
