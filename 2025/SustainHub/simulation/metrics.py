def compute_harmony_index(agents):
    """
    Compute Harmony Index based on:
    1. Task distribution balance
    2. Success rates
    3. Load distribution fairness
    """

    import numpy as np

    task_success_rates = []
    task_loads = []
    task_distribution_balance = []

    total_success = 0
    total_tasks = 0

    for agent in agents:
        # Get total and success per agent
        total = sum(agent.total_counts)
        success = sum(agent.success_counts)
        load = agent.task_load

        # Avoid division by zero
        success_rate = success / total if total > 0 else 0

        task_success_rates.append(success_rate)
        task_loads.append(load)

        total_success += success
        total_tasks += total

    # Mean success rate across agents
    avg_success_rate = np.mean(task_success_rates)

    # Fairness in load distribution: inverse of variance
    load_variance = np.var(task_loads)
    load_balance_score = 1 / (1 + load_variance)  # To keep it in (0,1)

    # Harmony Index: weighted sum (you can tune weights)
    HI = 0.6 * avg_success_rate + 0.4 * load_balance_score
    return round(HI, 3)
