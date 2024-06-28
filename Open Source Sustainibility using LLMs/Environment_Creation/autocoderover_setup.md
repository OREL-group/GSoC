## About AutoCodeRover and it's role in the Open Source Sustainibility using LLMs Project.
I was working on creating an environment for the agents, ie. allowing them to navigate codespaces and solve issues, and did some research for the same during which I came across the following papers : CodeR (https://arxiv.org/pdf/2406.01304), SWE-Agent (https://arxiv.org/abs/2405.15793) and AutoCodeRover (https://arxiv.org/abs/2404.05427)
Among these I feel the best fit for the project at hand is trying to implementing AutoCodeRover with a toy repo, and I'm working on the same.

### Description
This environment is based on a paper "AutoCodeRover: Autonomous Program Improvement" and it's open-source code implementation [on github](https://github.com/nus-apr/auto-code-rover) has been used as a dependency in my project .
- It combines LLMs with analysis and debugging capabilities to prioritize patch locations ultimately leading to a patch.
- AutoCodeRover works in two stages:
- - Context retrieval: The LLM is provided with code search APIs to navigate the codebase and collect relevant context.
- - Patch generation: The LLM tries to write a patch, based on retrieved context.
- AutoCodeRover has two unique features:
- - Code search APIs are Program Structure Aware. Instead of searching over files by plain string matching, AutoCodeRover searches for relevant code context (methods/classes) in the abstract syntax tree.
- - When a test suite is available, AutoCodeRover can take advantage of test cases to achieve an even higher repair rate, by performing statistical fault localization.

## Steps to Reproduce my Efforts
I may later add the [auto-code-rover repo](https://github.com/nus-apr/auto-code-rover) to my project as a dependency or publish a docker image of it on the web, currently I have cloned the repository and working within it. The steps to reproduce are as follows :

### Ollama Installation
Please install [ollama](https://ollama.com/) and download the corresponding models with ollama (e.g. `ollama pull mistral`).

### Download Docker Desktop 
Since my setup is  ollama in host + ACR in its container, I follow the recommendation to install Docker Desktop on the host, in addition to the Docker Engine.
Docker Desktop contains Docker Engine, and also has a virtual machine which makes it easier to access the host ports from within a container. With Docker Desktop, this setup will work without additional effort.

Download Docker Desktop and setup accopridng to instructions provided [here](https://docs.docker.com/desktop/install/windows-install/)

### Git Clone
Please clone [my fork of the repository](https://github.com/sarrah-basta/auto-code-rover-for-llama37b.git) instead of the original as I have made some fixes to help it work better with locally hosted models especially llama3 7B using ollama. Without these fixes the correct answers will not be obtained.

```
git clone https://github.com/sarrah-basta/auto-code-rover-for-llama37b.git
cd auto-code-rover
```

### Setup environment

Since this project is using Ollama to host a open-source model locally, there is no need to setup an API key. 
In the event of wanting to use this project with API's provided by OpenAI, Claude or GROQ, the instructions can be found [here](https://github.com/nus-apr/auto-code-rover#-setup--running).

We recommend running AutoCodeRover in a Docker container.

Build and start the docker image:

```
docker build -f Dockerfile -t acr .
docker run -it -p 3000:3000 -p 5000:5000 acr
```

### Inference using locally hosted model

Now, we can run ollama server on the host machine, and ACR in its container. ACR will attempt to communicate to the ollama server on host. 

ACR (AutoCodeRover) is set up to be used only with the Llama3 (8B and 70B) model via Ollama. Hence, we will call it with the `llama3` model.

```
cd /opt/auto-code-rover
conda activate auto-code-rover
PYTHONPATH=. python app/main.py github-issue --output-dir output --setup-dir setup --model llama3 --task-id <task id> --clone-link <link for cloning the project> --commit-hash <any version that has the issue> --issue-link <link to issue page>
```

Here is an example command for running ACR on an issue from the langchain GitHub issue tracker using the llama3 model hosted locally using Ollama:
```
PYTHONPATH=. python app/main.py github-issue --output-dir output --setup-dir setup --model llama3 --task-id langchain-20453 --clone-link https://github.com/langchain-ai/langchain.git --commit-hash cb6e5e5 --issue-link https://github.com/langchain-ai/langchain/issues/20453 
```

## Toy Repo such as can be used in our simulation

## Toy Repo for Simulation

In order to simulate the agent-based modeling approach and experiment with the AutoCodeRover, it is beneficial to have a toy repository. This allows us to focus on the core functionalities of the agent and the AutoCodeRover without the computational cost associated with real-world projects.

For this purpose, I have created a toy repository that implements a calculator. The repository has been designed with a well-defined file structure to ensure clarity and ease of experimentation. The calculator toy repository is a basic example for our simulation. It helps us explore agent capabilities in a controlled environment. 

### ACR In Local issue mode : Set up and run on local repositories and local issues

To run ACR on the local issue and local codebase of our toy repository,we need to first provide the docker container with access to the local folder (here "calculator_project"). To do so, add the following flag and arguments to the `docker run -it -p 3000:3000 -p 5000:5000 acr` command: 
```
-v "absolute//path//to//calculator_project":/calculator_project 
```

Alternatively, for Command Prompt on Windows the command will become :

```
docker run -it -p 3000:3000 -p 5000:5000 -v "%CD%\calculator_project":/home/calculator_project acr
```

Then, follow the following steps : 
1. Navigate to the `/opt/auto-code-rover` directory within the docker container as instructed above.
2. Activate the `auto-code-rover` conda environment via `conda activate auto-code-rover`.
3. Run the following command:
    ```
    PYTHONPATH=. python app/main.py local-issue --output-dir output --model llama3 --task-id <task id> --local-repo /path/to/calculator_project --issue-file /path/to/issue_description.md
    ```
    Make sure to replace `<task id>` with the desired task ID, `/path/to/calculator_project` with the path to your local project repository (using relative path for the "calculator_project" folder present here it would be : `calculator_project`), and `/path/to/issue_description.md` with the path to the file containing the issue description (using relative path for the "calculator_project" folder present here it would be : `calculator_project/issues/task_1.md`) .

PYTHONPATH=. python app/main.py local-issue --output-dir output --model llama3 --task-id 1 --local-repo /home/calculator_project --issue-file /home/calculator_project/issues/task_1.md

If the patch generation is successful, the path to the generated patch will be printed at the end.
