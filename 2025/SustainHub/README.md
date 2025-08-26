# SustainHub

**SustainHub** is a Reinforcement Learning–driven simulation framework for modeling, analyzing, and improving the sustainability of **open-source communities (OSS)**.  

The system captures realistic OSS dynamics using a **dual-layer reinforcement learning approach**:  
1. **Multi-Armed Bandits (MAB)** for global task allocation and role matching.  
2. **SARSA (State–Action–Reward–State–Action)** for local agent decision-making and task handling.  

Through this design, SustainHub provides insights into **fairness, adaptability, resilience, and efficiency** in collaborative communities.  

---

## 1. Project Motivation

Open-source ecosystems rely on distributed collaboration, but they face sustainability challenges such as:  
- Uneven workload distribution leading to burnout.  
- Contributor dropouts and churn.  
- Inefficiencies in task allocation.  
- Knowledge silos reducing long-term engagement.  

SustainHub addresses these issues by simulating OSS communities as **agent-based models** that balance **efficiency (tasks completed)** and **sustainability (fairness, adaptability, inclusivity)**.  

---

## 2. Objectives

- Simulate realistic OSS task allocation and contributor behavior.  
- Balance **exploration (testing new contributors)** and **exploitation (using proven contributors)**.  
- Model individual learning and role specialization through SARSA.  
- Track community sustainability with **quantitative health metrics**.  
- Provide interactive experimentation through a GUI with simulation controls and visualizations.  

---

## 3. Reinforcement Learning Framework

### 3.1 Multi-Armed Bandits (MAB)

- **Role**: Used by the **Maintainer** to allocate tasks among available agents.  
- **Algorithm**: **Thompson Sampling** is applied to model the **exploration–exploitation tradeoff**.  
- **Mechanism**:  
  - Agents = levers in the bandit problem.  
  - Tasks = pulls on levers.  
  - Success/failure of task completion = observed reward.  

- **Benefits**:  
  - Ensures fairness by giving opportunities to less-used agents.  
  - Prevents stagnation by encouraging exploration.  
  - Adapts to evolving agent performance over time.  

---

### 3.2 SARSA (State–Action–Reward–State–Action)

- **Role**: Governs how individual agents respond to assigned tasks.  
- **Algorithm**: On-policy **Temporal Difference (TD) learning** method.  
- **State Representation**: Defined by  
  - Task type (bug, feature, documentation, other)  
  - Current workload (light, moderate, heavy)  
  - Historical success rate  

- **Actions**:  
  - Accept and attempt task.  
  - Skip task (idle).  
  - Attempt task outside specialization.  

- **Reward System**:  
  - +3 for success in specialized tasks.  
  - +1 for success in non-specialized tasks.  
  - 0 for skipping tasks.  
  - −1 for failed tasks.  

- **Advantages**:  
  - Encourages specialization while allowing flexibility.  
  - Penalizes idleness and failures.  
  - Models real OSS behavior where contributors adapt over time.  

---

### 3.3 Synergy of MAB and SARSA

- **MAB (Global Layer)**: Decides **who gets the task** based on role performance.  
- **SARSA (Local Layer)**: Decides **how the assigned agent responds** to the task.  

This layered reinforcement learning system ensures:  
- Fair global allocation of tasks.  
- Adaptive local agent learning and behavior refinement.  
- More realistic modeling of OSS collaboration.  

---

## 4. Agents

SustainHub models four specialized agent types, reflecting common OSS roles.  

| Agent Type        | Specialization                  | Reward (Success)     | Reward (Failure / Skip) |
|-------------------|---------------------------------|----------------------|--------------------------|
| **Maintainer**        | Allocates tasks using MAB        | Indirect via efficiency | — |
| **Contributor**       | Bug fixing and stability         | +3 (bugs), +1 (others) | −1 / 0 |
| **Innovator**         | Feature design and implementation| +3 (features), +1 (others) | −1 / 0 |
| **Knowledge Curator** | Documentation and knowledge mgmt | +3 (docs), +1 (others) | −1 / 0 |

### Why these agents?
- **Maintainer**: Ensures efficiency and fairness in task allocation.  
- **Contributor**: Keeps the project stable by resolving bugs.  
- **Innovator**: Drives growth by adding new features.  
- **Knowledge Curator**: Maintains documentation, ensuring accessibility and long-term engagement.  

Together, they capture the **division of labor and collaboration patterns** in OSS.  

---

## 5. Community Health Metrics

SustainHub introduces three quantitative metrics to measure sustainability:

### 5.1 Harmony Index (HI)
- **Purpose**: Captures workload balance and task success rate.  
- **Formula**:  
  \[
  HI = 0.6 \times \text{Avg Success Rate} + 0.4 \times \frac{1}{1 + \text{Load Variance}}
  \]  
- **Range**: 0 (imbalanced) → 1 (perfect balance).  
- **Insight**: High HI indicates fairness and prevents burnout.  

---

### 5.2 Resilience Quotient (RQ)
- **Purpose**: Measures adaptability during disruptions (dropouts, workload spikes).  
- **Formula**:  
  \[
  RQ = 0.4 \times TRE + 0.3 \times SRR + 0.3 \times HS
  \]  
  - TRE = Task Reallocation Efficiency  
  - SRR = Success Rate Recovery  
  - HS = Harmony Stability  

- **Range**: 0 (low) → 1 (high resilience).  
- **Insight**: High RQ = system can recover smoothly from disruptions.  

---

### 5.3 Reassignment Overhead (RO)
- **Purpose**: Tracks inefficiency caused by reassigning tasks.  
- **Formula**:  
  \[
  RO = \frac{\text{Reassigned Tasks}}{\text{Total Tasks Assigned}}
  \]  
- **Range**: 0 (efficient) → 1 (highly inefficient).  
- **Insight**: Lower RO means effective first-time task allocation.  

---

## 6. Graphical User Interface (GUI)

Implemented in **Tkinter** with GitHub-inspired dark theme. Divided into three tabs:

### 6.1 Logs Tab
- Configure simulation parameters: steps, agents, tasks per step, dropouts per step.  
- Real-time textual logs in a terminal-like style.  
- Export logs as `.txt`.  

### 6.2 Graphs Tab
- Interactive performance graphs for **HI, RQ, and RO** using Matplotlib.  
- Export graphs as `.png` files.  
- Color-coded metrics for clarity.  

### 6.3 Visualizer Tab
- Agents visualized as **blue circles** and tasks as **yellow squares**.  
- Animated movements simulate task allocation and completion.  
- Optional **NetLogo integration** for advanced visualizations.  

---

## 7. Simulation Controls

- **Tasks per Step**: Simulates workload variation.  
- **Dropouts per Step**: Models contributor churn.  

These controls allow stress-testing of OSS dynamics under different conditions.    

---

## 8. How to Run

1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/sustainhub.git
   cd SustainHub 
  