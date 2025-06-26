# 🌱 SustainHub

**SustainHub** is a Reinforcement Learning–powered simulation for studying and enhancing the sustainability of open-source communities. It models real-world OSS dynamics through a combination of **Multi-Armed Bandits (MAB)** for task allocation and **SARSA** for agent-level learning and decision-making.

The system is built around four specialized agents representing common roles in OSS: **Maintainer**, **Contributor**, **Innovator**, and **Knowledge Curator**.

---

## 🎯 Objectives

- Simulate task allocation and agent behavior in OSS environments.
- Optimize contributor engagement using MAB and SARSA.
- Promote sustainable collaboration through intelligent agent decisions.
- Track community health via custom metrics like **Harmony Index** and **Resilience Quotient**.

---

## 🧠 Key Components

### 🔁 Multi-Armed Bandit (MAB)

Used by the **Maintainer** to allocate tasks to agents. MAB uses **Thompson Sampling** to balance exploration and exploitation based on agent performance on different task types.

> 📄 See: `mab.py`

### 🧬 SARSA Learning

Each agent (Contributor, Innovator, Knowledge Curator) uses **SARSA** to learn optimal actions from interaction history — enabling them to improve their task responses over time.

> 📄 See: `sarsa.py`

---

## 👥 Agent Roles

| Agent            | Description |
|------------------|-------------|
| 🧑‍🔧 **Maintainer**         | Allocates tasks using a MAB-based strategy that adapts over time. |
| 🐛 **Contributor**        | Specializes in bug fixes; learns which bugs to tackle using SARSA. |
| 🌟 **Innovator**          | Builds new features; learns how to prioritize ideas effectively. |
| 📚 **Knowledge Curator**  | Improves documentation; learns how to respond to doc-related tasks. |

---

## ⚙️ How It Works

1. **Maintainer** uses MAB to assign tasks to available agents.
2. Each agent (Contributor, Innovator, Curator) learns using the SARSA algorithm:
   - States can include current load, last task success, etc.
   - Actions include accepting/rejecting or prioritizing tasks.
3. Task outcomes are scored, affecting the reward signal.
4. Harmony and Resilience metrics are tracked and logged.

---

## 📈 Metrics Tracked

- ✅ Task success rate per agent type
- 🤝 Collaboration harmony between agents
- 🔁 Adaptability of agent choices over episodes
- ⚖️ Resilience to overload or contributor dropout

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/sustainhub.git
cd sustainhub
pip install -r requirements.txt
