# SustainHub

**SustainHub** is a Reinforcement Learning–powered simulation for studying and enhancing the sustainability of open-source communities. It models real-world OSS dynamics through a combination of Multi-Armed Bandits (MAB) for task allocation and SARSA for agent-level learning and decision-making.

The system is built around four specialized agents representing common roles in OSS: Maintainer, Contributor, Innovator, and Knowledge Curator.

---

## Objectives

- Simulate dynamic OSS task allocation and contributor behavior
- Optimize engagement using MAB (global) and SARSA (local)
- Promote sustainable collaboration through adaptive decision-making
- Track community health using metrics like Harmony Index and Resilience Quotient

---

## Key Components

### Multi-Armed Bandit (MAB)
Used by the Maintainer to assign tasks. MAB uses Thompson Sampling to learn which agents perform best on which task types over time.

> Source: `tasks/mab.py`

### SARSA Learning
Each learning agent (Contributor, Innovator, Curator) uses SARSA to adapt task responses based on rewards and past experiences.

> Source: `agents/sarsa.py`

---

## Agent Roles

| Agent             | Specialization                        |
|------------------|----------------------------------------|
| Maintainer        | Allocates tasks using MAB strategy     |
| Contributor       | Fixes bugs and learns via SARSA        |
| Innovator         | Develops features with adaptive logic  |
| Knowledge Curator | Handles documentation and curation     |

---

## How It Works

1. The Maintainer selects agents using the MAB allocator.
2. Agents accept/reject tasks and learn actions via SARSA.
3. Task outcomes provide rewards to guide future decisions.
4. Community health is tracked through Harmony Index and Resilience Quotient.

---

## Tracked Metrics

- Task success rate (per agent and per task type)
- Harmony Index: evaluates collaboration smoothness and fairness
- Resilience Quotient (coming soon): measures robustness under stress
- Heatmaps and line charts for success, harmony, and trends
- Resilience Quotient 

---

## How to run this
- clone the repository
- click and run the gui.py
- this helps you view the user interface.

## Installation

```bash
git clone https://github.com/yourusername/sustainhub.git
cd sustainhub

