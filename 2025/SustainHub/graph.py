import os
import matplotlib.pyplot as plt
import seaborn as sns

TASK_TYPES = ["bug", "feature", "docs"]

def plot_sarsa_agents(agents, save_dir, harmony_index_history=None, rq_history=None, ro_history=None):
    os.makedirs(save_dir, exist_ok=True)

    sarsa_agents = [a for a in agents if hasattr(a, "sarsa") and sum(a.total_counts) > 0]

    if not sarsa_agents:
        print("No SARSA agents with task history found to visualize.")
        return

    #Success Rate Heatmap.
    success_matrix = []
    agent_labels = []

    for agent in sarsa_agents:
        success_row = []
        for i in range(len(TASK_TYPES)):
            total = agent.total_counts[i]
            success = agent.success_counts[i]
            rate = (success / total * 100) if total > 0 else 0
            success_row.append(rate)
        success_matrix.append(success_row)
        agent_labels.append(agent.name)

    plt.figure(figsize=(10, max(4, len(sarsa_agents) * 0.6)))
    sns.heatmap(success_matrix, annot=True, fmt=".1f", cmap="YlGnBu",
                xticklabels=TASK_TYPES, yticklabels=agent_labels)
    plt.title("Success Rate (%) per Task Type for SARSA Agents")
    plt.xlabel("Task Type")
    plt.ylabel("Agent")
    heatmap_path = os.path.join(save_dir, "success_rate_heatmap.png")
    plt.tight_layout()
    plt.savefig(heatmap_path)
    plt.show()
    print(f"✅ Success rate heatmap saved to: {heatmap_path}")

    # Harmony Index Line Plot
    if harmony_index_history:
        plot_harmony_index_over_time(harmony_index_history, save_dir)

    # Resilience Quotient Line Plot
    if rq_history:
        plot_resilience_quotient_over_time(rq_history, save_dir)

    # Reassignment Overhead Line Plot
    if ro_history:
        plot_reassignment_overhead_over_time(ro_history, save_dir)


def plot_harmony_index_over_time(harmony_values, save_dir):
    steps = list(range(1, len(harmony_values) + 1))
    plt.figure(figsize=(8, 5))
    plt.plot(steps, harmony_values, marker="o", color="teal", linewidth=2)
    plt.title("Harmony Index Over Simulation Steps")
    plt.xlabel("Simulation Step")
    plt.ylabel("Harmony Index")
    plt.ylim(0, 1)
    plt.grid(True)
    path = os.path.join(save_dir, "harmony_index_over_time.png")
    plt.tight_layout()
    plt.savefig(path)
    plt.show()
    print(f"✅ Harmony Index trend saved to: {path}")


def plot_resilience_quotient_over_time(rq_values, save_dir):
    steps = list(range(1, len(rq_values) + 1))
    plt.figure(figsize=(8, 5))
    plt.plot(steps, rq_values, marker="o", color="crimson", linewidth=2)
    plt.title("Resilience Quotient Over Simulation Steps")
    plt.xlabel("Simulation Step")
    plt.ylabel("Resilience Quotient")
    plt.grid(True)
    path = os.path.join(save_dir, "resilience_quotient_over_time.png")
    plt.tight_layout()
    plt.savefig(path)
    plt.show()
    print(f"✅ Resilience Quotient trend saved to: {path}")


def plot_reassignment_overhead_over_time(ro_values, save_dir):
    steps = list(range(1, len(ro_values) + 1))
    plt.figure(figsize=(8, 5))
    plt.plot(steps, ro_values, marker="o", color="purple", linewidth=2)
    plt.title("Reassignment Overhead Over Simulation Steps")
    plt.xlabel("Simulation Step")
    plt.ylabel("Reassignment Overhead")
    plt.grid(True)
    path = os.path.join(save_dir, "reassignment_overhead_over_time.png")
    plt.tight_layout()
    plt.savefig(path)
    plt.show()
    print(f"✅ Reassignment Overhead trend saved to: {path}")
