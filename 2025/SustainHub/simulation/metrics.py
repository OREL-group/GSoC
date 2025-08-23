def compute_harmony_index(agents):
    """
    Compute Harmony Index (HI) based on:
    1. Task distribution balance
    2. Success rates
    3. Load distribution fairness
 
    Returns:
        float: HI value between 0 and 1
    """
    import numpy as np

    task_success_rates = []
    task_loads = []

    total_success = 0
    total_tasks = 0

    for agent in agents:
        total = sum(agent.total_counts)
        success = sum(agent.success_counts)
        load = agent.task_load

        success_rate = success / total if total > 0 else 0
        task_success_rates.append(success_rate)
        task_loads.append(load)

        total_success += success
        total_tasks += total

    avg_success_rate = np.mean(task_success_rates)
    load_variance = np.var(task_loads)
    load_balance_score = 1 / (1 + load_variance)

    HI = 0.6 * avg_success_rate + 0.4 * load_balance_score
    return round(HI, 3)


def compute_resilience_quotient(agents, previous_success_rate, previous_harmony, dropout_count):
    """
    Resilience Quotient (RQ) = 
        0.4 * Task Reallocation Efficiency +
        0.3 * Success Rate Recovery +
        0.3 * Harmony Stability
  
    Returns:
        float: RQ value between 0 and 1
    """
    import numpy as np

    # Task Reallocation Efficiency
    total_dropped = 0
    total_reassigned = 0

    for agent in agents:
        total_dropped += getattr(agent, "dropped_tasks", 0)
        total_reassigned += getattr(agent, "reassigned_tasks", 0)

    if total_dropped == 0:
        TRE = 1.0  # No dropouts = perfectly resilient
    else:
        TRE = total_reassigned / total_dropped

    # Success Rate Recovery
    success_rates = [
        sum(agent.success_counts) / sum(agent.total_counts)
        for agent in agents if sum(agent.total_counts) > 0
    ]
    current_success_rate = np.mean(success_rates) if success_rates else 0
    SRR = 1 - abs(current_success_rate - previous_success_rate)

    # Harmony Stability
    current_harmony = compute_harmony_index(agents)
    HS = 1 - abs(current_harmony - previous_harmony)

    # Final score
    RQ = 0.4 * TRE + 0.3 * SRR + 0.3 * HS
    return round(RQ, 3)


def calculate_reassignment_overhead(num_reassigned: int, total_tasks: int) -> float:
    """
    Calculate Reassignment Overhead (RO)

    RO = (Number of reassigned tasks) / (Total tasks assigned)

    Args:
        num_reassigned (int): Number of tasks that were reassigned.
        total_tasks (int): Total number of tasks assigned.

    Returns:
        float: RO value between 0 and 1 
    """
    if total_tasks == 0:
        return 0.0
    return round(num_reassigned / total_tasks, 3)
