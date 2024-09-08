
# MARLOSC : Multi-Agent Reinforcement Learning Model for Open Source Communities

This repository demonstrates the application of Reinforcement Learning(RL) using the Mesa agent-based modelling framework. These implementations were developed as part of my Summer Cohort 2024 project under Orthogonal Research and Education Laboratory(OREL).


## Getting Started

### Installation

Given the number of dependencies required, we recommend starting by creating a Conda or a Python virtual environment

1. Clone the project

```bash
  git clone https://github.com/OREL-group/GSoC.git
```

2. Go to the project directory

```bash
  cd Open\ Source\ Sustainability\ using\ RL/
```

3. Install RLlib for Multi-Agent Training

```bash
  pip install "ray[rllib]" tensorflow torch
```

4. Install Addition Dependencies

```bash
  pip install -r requirements.txt
```

### Running the Model
To run the model simply execute `example.py`

```bash
  python example.py
```
Note: Pre-trained models might not work in some cases because of different library versions. In such cases, you can train your own model and use it.

After the training of the agents is complete you will see a folder `checkpoints` in the project directory that consists of trained models. Furthermore, you will also see a file `results.txt` that consits of the training results. 




## Contributing

Contributions are always welcome!

Please adhere to this project's `code of conduct`.

