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

1. Follow the instructions in the `autocoderover_setup.md` file located in the project directory: `OREL-GSoC/Open Source Sustainibility using LLMs/Environment_Creation/`.

## Step 3: Running the Python File

The Python file `reviewed_pr.py` which aims to create a ContributorAgent and have it create a acceptable Pull Request to solve a issue, and have a MaintainerAgent to accept the request and merge it, is currently still under development.
