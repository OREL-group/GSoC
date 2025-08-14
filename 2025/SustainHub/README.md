# SustainHub

**SustainHub** is a Reinforcement Learning–powered simulation for studying and enhancing the sustainability of open-source communities. It models real-world OSS dynamics through a combination of Multi-Armed Bandits (MAB) for task allocation and SARSA for agent-level learning and decision-making.

The system is built around four specialized agents representing common roles in OSS: Maintainer, Contributor, Innovator, and Knowledge Curator.

---

## Objectives

- Simulate dynamic OSS task allocation and contributor behavior
- Optimize engagement using MAB (global) and SARSA (local)
- Promote sustainable collaboration through adaptive decision-making
- Track community health using metrics like Harmony Index, Resilience Quotient, and Reassignment Overhead

---

## Key Components

### Multi-Armed Bandit (MAB)
Used by the Maintainer to assign tasks. MAB uses Thompson Sampling to learn which agents perform best on which task types over time.

> 📁 Source: `tasks/mab.py`

### SARSA Learning
Each learning agent (Contributor, Innovator, Curator) uses SARSA to adapt task responses based on rewards and past experiences.

> 📁 Source: `agents/sarsa.py`

---

## 👥 Agent Roles

| Agent             | Specialization                        |
|-------------------|---------------------------------------|
| **Maintainer**        | Allocates tasks using MAB strategy     |
| **Contributor**       | Fixes bugs and learns via SARSA        |
| **Innovator**         | Develops features with adaptive logic  |
| **Knowledge Curator** | Handles documentation and curation     |

---

## How It Works

1. The Maintainer selects agents using the MAB allocator.
2. Agents accept/reject tasks and learn actions via SARSA.
3. Tasks may be **reassigned** if an agent cannot complete them (tracked via RO).
4. Task outcomes provide rewards to guide future decisions.
5. Community health is tracked through Harmony Index, Resilience Quotient, and Reassignment Overhead.

---

## 📊 Tracked Metrics

### **Harmony Index (HI)**
- **Measures**: Balance in task distribution and success rates.
- **Formula**:  
  \[
  HI = 0.6 \times \text{Avg Success Rate} + 0.4 \times \frac{1}{1 + \text{Load Variance}}
  \]
- **Range**: `0` (poor balance) → `1` (perfect balance)  
> 📁 `metrics.compute_harmony_index`

---

### **Resilience Quotient (RQ)**
- **Measures**: Recovery from disruptions like agent dropouts.
- **Formula**:  
  \[
  RQ = 0.4 \times TRE + 0.3 \times SRR + 0.3 \times HS
  \]
  - **TRE**: Task Reallocation Efficiency  
  - **SRR**: Success Rate Recovery  
  - **HS**: Harmony Stability  
- **Range**: `0` (low resilience) → `1` (high resilience)  
> 📁 `metrics.compute_resilience_quotient`

---

### **Reassignment Overhead (RO)**
- **Measures**: Frequency of task reassignments.
- **Formula**:  
  \[
  RO = \frac{\text{Reassigned Tasks}}{\text{Total Tasks Assigned}}
  \]
- **Low RO** = Efficient allocation, **High RO** = Frequent reassignments.  
> 📁 `metrics.calculate_reassignment_overhead`

---

### **Task Success Rate**
- **Measures**: % of tasks completed successfully.
- **Formula**:  
  \[
  SR = \frac{\text{Successful Tasks}}{\text{Total Tasks Assigned}}
  \]
- High SR means better role-task matching.
mance trends.

---

## 🎛 New Simulation Controls (UI Sliders)

SustainHub now includes interactive UI sliders for more dynamic experimentation:

| Control             | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| **Dropouts per Step** | Sets the number of agents that leave the system in each simulation step, modeling contributor churn. |
| **Tasks per Step**    | Controls how many new tasks are introduced per step, simulating workload variations. |

### Benefits:
- Simulate realistic OSS conditions (e.g., workload spikes, contributor dropout)
- Analyze sustainability under different stress scenarios
- Tune task-agent balance for optimal performance
- Visualize impact of community changes over time

---

## ▶ How to Run 

1. Clone the repository
2. Navigate to the directory
3. Run the GUI

```bash
git clone https://github.com/yourusername/sustainhub.git
cd sustainhub
python gui.py
