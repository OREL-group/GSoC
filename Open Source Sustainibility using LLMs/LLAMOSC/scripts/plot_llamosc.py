# working code but only shown at end

# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import os
# import random


# class Contributor:
#     def __init__(self, name, experience):
#         self.name = name
#         self.experience = experience


# # Sample contributors
# contributors = [
#     Contributor("Alice", 1),
#     Contributor("Bob", 2),
#     Contributor("Charlie", 3),
#     Contributor("Dave", 4),
# ]

# # Sample issues (not used in this example)
# issues = range(10)  # Placeholder for issues

# time = 0


# def log_and_print(message):
#     print(message)


# # Initialize dictionary to store experience over time for each contributor
# experience_over_time = {contributor.name: [] for contributor in contributors}


# # Function to store experience data
# def store_experience(contributors):
#     for contributor in contributors:
#         experience_over_time[contributor.name].append(contributor.experience)


# # Function to update experience
# def update_experience():
#     global time
#     log_and_print(f"\nTime Step: {time}\n")
#     log_and_print("Experience of all contributors:")
#     log_and_print(
#         [(contributor.name, contributor.experience) for contributor in contributors]
#     )

#     # Store the experience data at the current time step
#     store_experience(contributors)

#     # Simulate some experience increase for a random contributor
#     selected_contributor = random.choice(contributors)
#     selected_contributor.experience += random.randint(1, 3)

#     time += 1


# # Function to update the plot
# def update_plot(frame):
#     update_experience()

#     plt.clf()
#     for name, experiences in experience_over_time.items():
#         plt.plot(range(len(experiences)), experiences, label=name)

#     plt.xlabel("Time Steps")
#     plt.ylabel("Experience")
#     plt.title("Experience of Contributors Over Time")
#     plt.legend()


# log_and_print(
#     f"\nStarting simulation with {len(issues)} issues and {len(contributors)} contributors.\n"
# )

# # Create the plot
# fig = plt.figure(figsize=(10, 5))

# # Create the animation
# ani = animation.FuncAnimation(fig, update_plot, frames=len(issues), repeat=False)

# # Show the plot
# plt.show()

# working code with updating experience correctly

import matplotlib.pyplot as plt
import os
import time


# Sample class definitions
class Contributor:
    def __init__(self, name, experience):
        self.name = name
        self.experience = experience


# Sample log_and_print function
def log_and_print(message):
    print(message)


# Sample data
contributors = [
    Contributor("Alice", 5),
    Contributor("Bob", 3),
    Contributor("Charlie", 4),
]
issues = [1, 2, 3]
use_acr = True
algorithm = "example_algorithm"
project_dir = "./"

# Initialize time and experience history
timestep = 0
experience_history = {
    contributor.name: [contributor.experience] for contributor in contributors
}
time_history = [0]

log_and_print(
    f"\nStarting simulation with {len(issues)} issues and {len(contributors)} contributors with ACR : {use_acr} and Algorithm : {algorithm}.\n"
)

# Setup for matplotlib animation
fig, ax = plt.subplots()
lines = {
    contributor.name: ax.plot([], [], label=contributor.name)[0]
    for contributor in contributors
}


def init():
    ax.set_xlim(0, len(issues))
    ax.set_ylim(0, max(contributor.experience for contributor in contributors) + 10)
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Experience")
    ax.legend()
    return lines.values()


def update():
    global timestep
    log_and_print(f"\nTime Step: {timestep}\n")
    log_and_print("Experience of all contributors:")
    log_and_print(
        [(contributor.name, contributor.experience) for contributor in contributors]
    )

    # Update experience of contributors for demonstration (replace with actual logic)
    for contributor in contributors:
        contributor.experience += 1  # Example logic to increment experience

    # Append new experiences to history
    timestep += 1
    time_history.append(timestep)
    for contributor in contributors:
        experience_history[contributor.name].append(contributor.experience)

    # Update lines data
    for contributor in contributors:
        lines[contributor.name].set_data(
            time_history, experience_history[contributor.name]
        )

    # Draw the updated plot
    plt.draw()
    plt.pause(0.1)

    time.sleep(5)


init()

# Main simulation loop
for issue in issues:
    update()

plt.show()
