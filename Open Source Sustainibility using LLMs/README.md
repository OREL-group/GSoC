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

## Running the relevant scripts 

### Running the Authoritarian Algorithm

The authoritarian algorithm is a decision-making algorithm used in Multi Agent Decision Making (MADM) systems. It handles situations where there is a single decision-maker, known as the "authoritarian agent," who makes decisions on behalf of a group of agents. More information can be found in `Open Source Sustainibility using LLMs\Multi_Agent_Decision_Making\README.md`

To run the authoritarian algorithm using the LLAMOSC framework, make sure you navigate to the root directory of the LLAMOSC package and use the following command:

```bash
python .\LLAMOSC\scripts\reviewed_pr_authoritatian.py
```
### Running the Decentralized Algorithm

The decentralized algorithm is a decision-making algorithm used in Multi Agent Decision Making (MADM) systems. It allows for distributed decision-making among multiple agents, eliminating the need for a single decision-maker. More information can be found in `Open Source Sustainibility using LLMs\Multi_Agent_Decision_Making\README.md`.

To run the decentralized algorithm using the LLAMOSC framework, make sure you navigate to the root directory of the LLAMOSC package and use the following command:

```bash
python .\LLAMOSC\scripts\reviewed_pr_decentralized.py
```
## References 

- For [decentralized](https://python.langchain.com.cn/docs/use_cases/agent_simulations/multiagent_bidding) and [authoritarian](https://python.langchain.com.cn/docs/use_cases/agent_simulations/multiagent_authoritarian) algorithm approaches : [Langchain Use Cases : Agent Simulations](https://python.langchain.com.cn/docs/use_cases/agent_simulations/)
- For information about [benevelont-dictator](http://oss-watch.ac.uk/resources/benevolentdictatorgovernancemodel) and [meritocratic](http://oss-watch.ac.uk/resources/meritocraticgovernancemodel) open-source goverenance models : http://oss-watch.ac.uk/resources/ 
- This environment is based on a paper "AutoCodeRover: Autonomous Program Improvement" and it's open-source code implementation [on github](https://github.com/nus-apr/auto-code-rover) has been used as a dependency in my project .
