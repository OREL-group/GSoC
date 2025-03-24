# LLAMOSC : LLM-Powered Agent-Based Model for Open Source Communities

## Overview

LLAMOSC (LLM-Powered Agent-Based Model for Open Source Communities) is a comprehensive framework designed to simulate and enhance the sustainability of open-source communities using Large Language Models (LLMs). The framework focuses on modeling interactions and productivity of agents with varying levels of experience, knowledge, and engagement in a virtual open-source environment.

### Key Components and Features implemented so far

1. **Environment**:
    - **GitHub (CodeSpace Environment)**: A simulated code space (powered by AutoCodeRover) where agents contribute to open-source projects, mirroring real-world GitHub repositories.

2. **Environment Variables**:
    - **Issues**: Issues are categorized with varying difficulty from 1 to 5, resembling real-life variation from "Good First Issues" to "Expert Required Issues", assigned based on the contributor agent's experience level.

3. **Agents**:
    - **Coding Ability**: Skill level in writing and reviewing code, (powered by AutoCodeRover).

4. **Agent Variables (Internal States)**:
    - **Experience Level**: Categorized from 1 to 5 resembling real-life contributors ranging from Novice to Experienced.

### Framework Capabilities

LLAMOSC integrates multiple capabilities to automate and optimize open-source community activities:

1. **AutoCodeRover Integration**:
    - Combines LLMs with advanced code navigation and debugging capabilities.
    - Operates in two stages: Context retrieval and Patch generation.
    - Features Program Structure Aware code search APIs to navigate codebases and generate patches.

2. **Automated Pull Request Lifecycle**:
    - **ContributorAgent**: Automates issue identification, solution proposal, and pull request creation.
    - **MaintainerAgent**: Automates pull request review and merging based on predefined criteria.
    - Utilizes Docker for environment consistency and isolation.
    - Implements diff extraction and automated pull request submission (powered by AutoCodeRover).

3. **Multi-Agent Decision Making Algorithms**:
    - **Authoritarian Algorithm (Benevolent Dictator Model)**:
        - Central maintainer manages and allocates tasks.
        - Contributors are rated and assigned tasks based on maintainer’s discretion.
    - **Decentralized Algorithm (Meritocratic Model)**:
        - Distributed decision-making among contributors.
        - Contributors bid on tasks based on their suitability and experience.

4. **Metrics and Trends Visualization**:
    - Visualizes different metrics throughout the simulation at each time step.
    - Includes **tracking** of contributor experience levels, code quality trends, and motivation levels to provide comprehensive insights into the dynamics of the open-source community.

### Accomplishments of LLAMOSC so far

- **Preliminary Design and Implementation**:
    - Created a robust framework for simulating open-source environments.
    - Developed agents with varying skill levels and experience to reflect real-world dynamics.

- **Automated Pull Request Lifecycle**:
    - Streamlined the process of identifying, solving issues, creating, submitting, reviewing, and merging pull requests.
    - Implemented reliable and reproducible workflows for ContributorAgent and MaintainerAgent.

- **Multi-Agent Decision Making**:
    - Simulated governance models used in open-source projects.
    - Developed algorithms for both centralized (authoritarian) and decentralized (meritocratic) task allocation.
    - ### Accomplishments of LLAMOSC so far
    - 
- **Graphical User Interface**:
    - Developed an intuitive graphical interface for inputting data and visualizing real-time updates of metrics within the LLAMOSC framework.
    - Enhanced the user experience by making complex metric visualizations easily accessible and actionable.
 
### Demo 
![LLAMOSC Simulation GUI](https://github.com/user-attachments/assets/91ccaf5c-ff2f-4391-9618-273aaaef493c)
You can find the full demo at https://youtu.be/NuKh1i70X8Q .

## Installation instructions

To begin, please follow the instructions provided in `Open Source Sustainibility using LLMs\Environment_Creation\README.md` and ensure that the scripts run successfully.

### Step 1: Install LLAMOSC

Make sure you have your virtual environment activated, then install LLAMOSC:

- The following command should be used after navigating to the directory `Open Source Sustainibility using LLMs\` i.e. the root directory of the LLAMOSC package:

```bash
pip install -e .
```

This command will install the package in editable mode, allowing changes to be made to the code and having them reflected immediately without the need for reinstallation. It will also install any dependencies specified in the setup.py file.

**Expected Output for successfull installation**:

```bash
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... done
  Preparing editable metadata (pyproject.toml) ... done
Building wheels for collected packages: LLAMOSC
  Building editable for LLAMOSC (pyproject.toml) ... done
  Created wheel for LLAMOSC: filename=LLAMOSC-0.1-0.editable-py3-none-any.whl size=2633 sha256=9d91d727f73ac57f32e943a2ba7a6703cf4d10121d0ef98075b8d5c37fe4b4a2
  Stored in directory: C:\Users\sarrah\AppData\Local\Temp\pip-ephem-wheel-cache-1u2f0e0o\wheels\4e\1f\49\6511790848ca800f7fae3bb0dbad2013b799fdf29612974710
Successfully built LLAMOSC
Installing collected packages: LLAMOSC
Successfully installed LLAMOSC-0.1
```
### Step 2: Create toy-repo Directory as the Environemnt ffor the Agent-Based Model
Run the provided script to create the toy_repo directory:

```bash
python Open Source Sustainibility using LLMs\Environment_Creation\create_toy_repo.py
```

This will create an empty calculator_project directory where the main `OREL-group/GSoC` repository was cloned.

### Step 3: Download and Extract `calculator_project`

1. **Download `calculator_project` files from the GitHub repository:**

    - Go to the [calculator_project GitHub repository](https://github.com/sarrah-basta/toy-repos-for-LLAMOSC/tree/main/calculator_project).
    - Download each file within the `calculator_project` by clicking on it and then clicking the `Download` button.

    Alternatively, you can download all files as a zip:

    - Click on the `Code` button on the main repository page.
    - Select `Download ZIP`.
    - Extract the zip file and copy the files within the `calculator_project` directory.

2. **Move the files to the correct location:**

    After downloading, move the files within `calculator_project` directory to the correct location (i.e the `calculator_project` directory created for you in Step 2)


### Directory Structure

After completing these steps, the directory structure should look like this:

```
calculator_project/
OREL-GSoC/
├───Open Source Sustainibility using LLMs
│   ├───Environment_Creation
│   ├───LLAMOSC
│   │   ├───agents
│   │   │   └───__pycache__
│   │   ├───scripts
│   │   ├───simulation
│   │   │   └───__pycache__
│   │   └───__pycache__
│   ├───LLAMOSC.egg-info
│   ├───Multi_Agent_Decision_Making
│   │   └───__pycache__
│   └───Preliminary Design
│       └───Assets
```

## Running the LLAMOSC Graphical User Interface

To set up and run the LLAMOSC simulation, follow these steps:

### Prerequisites

Ensure you have Python installed and the required dependencies set up.

### Steps to Run:

1. **Clear Previous Simulation Data**

   ```sh
   python .\LLAMOSC\scripts\clear_calculator_project.py
   ```

   This command removes earlier simulation data to ensure a fresh run.

2. **Start the Simulation GUI**

   ```sh
   python .\LLAMOSC\scripts\run_llamosc_frontend.py
   ```

   Running this command will open the LLAMOSC Simulation interface.

### Simulation UI Explanation

The LLAMOSC Simulation GUI consists of multiple input fields and options:
![LLAMOSC Simulation GUI Page 1](https://github.com/user-attachments/assets/1ea12821-0188-48d1-9bfd-0c7832cfe511)

- **Number of Contributors:** Specify the number of contributor agents in the simulation.
- **Number of Maintainers:** Define how many maintainers will oversee the project.
- **Number of Issues:** Set the number of issues that the agents will work on.
- **Use ACR:** (Optional) Enables AutoCodeRover functionality. This can be left unchecked to run the simulation without using AutoCodeRover as a dependency.
- **Testing Mode:** If enabled, the simulation will run without requiring an Ollama LLM setup (this should be checked for debugging and non-LLM execution).
- **Decision-Making Algorithm:** Choose between Authoritarian (Benevolent Dictatator) or Decentralized (Meritocratic) decision-making.
- **Select Issues Path:** Choose path of the main `calculator_project` folder (take care not to choose the `issues` subfolder).
- **Start Simulation Button:** Begins the simulation.

### Running the Simulation

- Click **Start Simulation** and watch the agents interact with issues in real-time.
- Monitor the **terminal logs** to observe agent creation, discussion, and issue resolution.
  ![Terminal Logs](https://github.com/user-attachments/assets/09768b29-07b3-4cd1-9a92-49ef779a0504)
- At this point agents are created.
  ![Starting Main GUI Window](https://github.com/user-attachments/assets/2f6440e0-11cc-47d5-b963-6277e886242a)
- Watch the main simulation window (opened via PyGUI) which will visualize the interactions.
![LLAMOSC Simulation GUI](https://github.com/user-attachments/assets/3d5af289-b95a-44bf-8f74-ef50fc280853)

## Understanding the LLAMOSC Simulation Framework
The simulation is based on the following structure:

### **1. Simulated Environment**
The framework mimics an open-source environment with:

- **Code Spaces:** Representing code repositories of projects where issues arise, and the **pull requests** that are submitted by the contributors to solve the issues are displayed here.
- **Discussion Spaces:** Simulating **active discussion** for communication and decision-making among contributors.

### **2. Agent Roles**
- **Issue Creator Agents:** Generate and submit issues based on the codebase (powered by LLMs).
- **Contributor Agents:** Work on resolving issues (powered by LLMs and AutoCodeRover).
- **Maintainer Agents:** Review contributions and approve/reject them based on quality (powered by LLMs).

### **3. Decision-Making & Evaluation Metrics**
The simulation assesses different metrics such as:

- **Code Quality** (based on the pull requests submitted)
- **Contributor Experience** (how contributor experience is imapcted by issues that are closed)
- **Contributor Motivation** (how well agents interact and based on their initial level as well)

These metrics help in evaluating the impact of various practices and their level of sustainibility of open-source communities.

## Additional Resources

- **Project Report:** Read more about LLAMOSC in the detailed GSoC 2024 report: [Sarrah's Blog](https://github.com/sarrah-basta/blogs/blob/gh-pages/_posts/2024-08-24-GSoC_'24_OREL_INCF_Project_Report.md)

## Future Work

- **Collaborative Issue Solving:** Implement collaboration algorithms to enable multiple agents to work together on a single issue, simulating complex teamwork dynamics. [Issue Link](https://github.com/OREL-group/GSoC/issues/64)
- **Dynamic Issue Creation:** Utilize `IssueCreatorAgent` to dynamically generate new issues during simulation, better mimicking evolving open-source projects. [Issue Link](https://github.com/OREL-group/GSoC/issues/63)
- **ConversationSpace (Slack Simulation):** Introduce `ConversationSpace` to replicate real-time team communications, enhancing the realism of agent interaction. [Issue Link](https://github.com/OREL-group/GSoC/issues/60)
- **RAG Integration:** Add Retrieval-Augmented Generation capabilities to both `ConversationSpace` and GitHub Discussions for more context-aware, relevant agent interactions. [Issue Link](https://github.com/OREL-group/GSoC/issues/62)
- **Engagement Metrics:** Incorporate metrics based on `ConversationSpace` to analyze interaction quality and collaboration levels. [Issue Link](https://github.com/OREL-group/GSoC/issues/61)

## References 

## References

- Shanahan, M., McDonell, K., & Reynolds, L. (2023, May 25). *Role-Play with Large Language Models*. [arXiv.org](https://arxiv.org/abs/2305.16960)

- Xi, Z., Chen, W., Guo, X., He, W., Ding, Y., Hong, B., Zhang, M., Wang, J., Jin, S., Zhou, E., Zheng, R., Fan, X., Wang, X., Xiong, L., Zhou, Y., Wang, W., Jiang, C., Zou, Y., Liu, X., … Gui, T. (2023, September 14). *The Rise and Potential of Large Language Model Based Agents: A Survey*. [arXiv.org](https://arxiv.org/abs/2309.07864)

- The **CodeSpace Environment** is based on the paper *“AutoCodeRover: Autonomous Program Improvement”* and its open-source code implementation [on Github](https://github.com/nus-apr/auto-code-rover), which has been used as a dependency in this project.

- For decentralized and authoritarian algorithm approaches: [Langchain Use Cases - Agent Simulations](https://docs.langchain.com/docs/use-cases/agent-simulations/)

- For information about **benevolent-dictator** and **meritocratic** open-source governance models: [OSS Watch - Governance Models](http://oss-watch.ac.uk/resources/)

