# Project Name: Open Source Sustainability using LLMs

This README file provides instructions on how to reproduce the code for the Environment Creation within the project "Open Source Sustainability using LLMs". Please follow the steps below:

## Step 1: Setting up the Virtual Environment

1. Make sure you have Python installed on your system.
2. Open a terminal or command prompt.
3. Navigate to the correct directory: `OREL-GSoC/Open Source Sustainibility using LLMs/Environment_Creation/`.
4. Run the following command to create a virtual environment:

```shell
python -m venv oss_llm
```

5. Activate the virtual environment:

- For Windows:

```shell
oss_llm\Scripts\activate
```

- For macOS/Linux:

```shell
source oss_llm/bin/activate
```

6. Install the required dependencies by running the following command:

```shell
pip install -r requirements.txt
```

## Step 2: Setting up Autocoderover

1. Install [ollama](https://ollama.com/) and download the corresponding models with ollama (e.g. `ollama pull llama3`).

2. Download Docker Desktop and setup accopridng to instructions provided [here](https://docs.docker.com/desktop/install/windows-install/)

*first time installation will need you to restart your pc.

3. Clone [this modified fork of the auto-code-rover](https://github.com/sarrah-basta/auto-code-rover-for-llama37b.git) instead of the original as some fixes were made to help it work better with locally hosted models especially llama3 7B using ollama. Without these fixes the correct answers will not be obtained.

```shell
cd ../../..
git clone https://github.com/sarrah-basta/auto-code-rover-for-llama37b.git
cd auto-code-rover-for-llama37b
```

4. Since this project is using Ollama to host a open-source model locally, there is no need to setup an API key. 
In the event of wanting to use this project with API's provided by OpenAI, Claude or GROQ, the instructions can be found [here](https://github.com/nus-apr/auto-code-rover#-setup--running).

We recommend running AutoCodeRover in a Docker container.

Build and start the docker image:

```shell
docker build -f Dockerfile -t acr1 .
docker run -it -p 3000:3000 -p 5000:5000 acr1
```
5. Now, we can run ollama server on the host machine, and ACR in its container. ACR will attempt to communicate to the ollama server on host. 

ACR (AutoCodeRover) is set up to be used only with the Llama3 (8B and 70B) model via Ollama. Hence, we will call it with the `llama3` model.
```shell
cd /opt/auto-code-rover
conda activate auto-code-rover
PYTHONPATH=. python app/main.py github-issue --output-dir output --setup-dir setup --model llama3 --task-id <task id> --clone-link <link for cloning the project> --commit-hash <any version that has the issue> --issue-link <link to issue page>
```
Here is an example command for running ACR on an issue from the langchain GitHub issue tracker using the llama3 model hosted locally using Ollama:
```shell
PYTHONPATH=. python app/main.py github-issue --output-dir output --setup-dir setup --model llama3 --task-id langchain-20453 --clone-link https://github.com/langchain-ai/langchain.git --commit-hash cb6e5e5 --issue-link https://github.com/langchain-ai/langchain/issues/20453 
```

for more information please look into [autocoderover_setup.md](./autocoderover_setup.md)

## Step 3: Running the Python File

The Python file `reviewed_pr.py` which aims to create a ContributorAgent and have it create a acceptable Pull Request to solve a issue, and have a MaintainerAgent to accept the request and merge it, is currently still under development.
