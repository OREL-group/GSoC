# LLAMOSC : LLM-Powered Agent-Based Model for Open Source Communities

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

### Certainly! Here's how you can rewrite Step 3 in the `README.md` to instruct users to download the files from the GitHub repository and place them correctly.

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
