# TODO : A script that combines all the functions of the LLAMOSC project
# (currently in reviewed_pr_.. scripts and new ones)
# TODO :to run the simulation with the options taken from user
# like no of agents, no of issues, no of tasks, etc. - TODO done except for issue
# TODO : automatically makes issues
# TODO optional : dynamic like new issues as well

# TODO : add code quality metric, llm response and graph
# TODO : begin personalization part

# was working on reviewed_pr-auth - experience metric done rest remaining

# TODO : Make docker optional - TODO done.
# TODO : takes options for choosing between authoritarian and decentralized - TODO done

# TODO : add metrics - contributor experience & simulation issues - TODO done
# TODO : stores data at every time step and prints graphical representation of the simulation with all metrics - doing, working code but after fiorst timestep plot is not nice
import shutil
import random

from matplotlib.axes import Axes

from LLAMOSC.agents.contributor import ContributorAgent
from LLAMOSC.agents.maintainer import MaintainerAgent
from LLAMOSC.simulation.issue import Issue
from LLAMOSC.simulation.sim import Simulation
from LLAMOSC.utils import *
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def init_plot(axis: Axes, x_label, y_label, x_max, y_max, title, lines):
    axis.set_xlim(0, x_max)
    axis.set_ylim(0, y_max + 10)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    axis.legend()
    return lines.values()


def main():

    parser = argparse.ArgumentParser(description="LLAMOSC Simulation")
    parser.add_argument(
        "--contributors", type=int, default=5, help="Number of contributors"
    )
    parser.add_argument(
        "--maintainers", type=int, default=3, help="Number of maintainers"
    )
    # parser.add_argument('--issues', type=int, default=10, help='Number of issues')
    # parser.add_argument('--issues_filepaths', type=str, default='issues', help='Path to the issues folder')
    parser.add_argument(
        "--use_acr",
        action="store_true",
        default=False,
        help="Use ACR (AutoCodeRover which requires Docker setup) for Issue Resolution instead of doing it randomly",
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        default="a",
        choices=["a", "d"],
        help="Choose decision making algorithm, options are 'a' or 'd' | 'a' (default) : authoritarian benevolent dictator model | 'd' : decentralized meritocratic governance model",
    )

    args = parser.parse_args()

    n_contributors = args.contributors
    n_maintainers = args.maintainers
    # n_issues = args.issues
    # n_tasks = args.tasks
    use_acr = args.use_acr
    algorithm = args.algorithm

    issues = []
    current_folder = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(
        current_folder, "..", "..", "..", "..", "calculator_project"
    )
    repo_commit_current_changes(project_dir)

    # Get the path to the issues folder
    # current folder
    issues_parent_folder = os.path.join(project_dir, "issues")
    issues_folder = os.path.join(issues_parent_folder, "pending")
    # Loop through all the files in the issues folder
    log_and_print("Reading issues from the issues folder...")
    for filename in os.listdir(issues_folder):
        # Create the file path
        file_path = os.path.join(issues_folder, filename)

        # Extract the issue id from the filename
        issue_id = int(filename.split("_")[1].split(".")[0])

        # Create the issue object
        # TODO: Better way to get issue difficulty maybe % 5 atleast
        issue = Issue(issue_id, issue_id + 1, file_path)

        # Add the issue to the issues list
        issues.append(issue)

    # Create required agents
    contributors = [
        ContributorAgent(i, random.randint(1, 5), f"Contributor_{i}")
        for i in range(n_contributors)  # 5 contributors by default
    ]
    maintainers = [
        MaintainerAgent(i, random.randint(4, 5), f"Maintainer_{i}")
        for i in range(n_maintainers)  # 3 maintainers by default
    ]

    log_and_print(f"Created agents: contributors and maintainers")

    sim = Simulation(contributors)

    # Initialize time and experience history
    global timestep
    timestep = 1
    experience_history = {
        contributor.name: [contributor.experience] for contributor in contributors
    }
    time_history = [0]

    log_and_print(
        f"\nStarting simulation with {len(issues)} issues and {len(contributors)} contributors with ACR : {use_acr} and Algorithm : {algorithm}.\n"
    )

    # Setup for matplotlib animation
    fig_cont_exp, ax_cont_exp = plt.subplots()
    lines_cont_exp = {
        contributor.name: ax_cont_exp.plot([], [], label=contributor.name)[0]
        for contributor in contributors
    }

    def update(timestep):

        # Contributor metrics
        log_and_print(f"\nTime Step: {timestep}\n")
        log_and_print("Experience of all contributors:")
        log_and_print(
            [(contributor.name, contributor.experience) for contributor in contributors]
        )

        # Simulation metrics
        # TODO : Add this in Sim class
        issues_pending = len(os.listdir(issues_folder))
        if os.path.exists(os.path.join(issues_parent_folder, "solved")):
            issues_solved = len(
                os.listdir(os.path.join(issues_parent_folder, "solved"))
            )
        else:
            issues_solved = 0
        log_and_print(
            f"\nIssues status : Pending - {issues_pending} Solved = {issues_solved}"
        )

        issue_description = open(issue.filepath).read()
        log_and_print(
            f"\nIssue #{issue.id} (Difficulty ({issue.difficulty})): {issue_description}\n"
        )

        # from the maintainers, select the maintainer who will be responsible for the issue by random from avilable & eligible maintainers
        selected_maintainer = random.choice(
            [
                maintainer
                for maintainer in maintainers
                if maintainer.eligible_for_issue(issue)
            ]
        )
        selected_maintainer.allot_task(issue)
        if algorithm == "d":
            selected_contributor = sim.select_contributor_decentralized(issue)
        else:
            selected_contributor = sim.select_contributor_authoritarian(
                selected_maintainer
            )

        # Assign an issue from the available issues to the agent
        if not selected_contributor:
            selected_contributor = [
                contributor
                for contributor in contributors
                if contributor.eligible_for_issue(issue)
            ][0]

        log(selected_contributor.name)
        # TODO : if no eligible contributors, loop until the issue is solved
        selected_contributor.assign_issue(issue)
        task_solved = (
            selected_contributor.solve_issue(project_dir)
            if use_acr
            else selected_contributor.solve_issue_without_acr(project_dir)
        )
        if task_solved:

            # Find the most recent pull request for the given task_id
            task_id = issue.id
            pull_request_dirs = [
                f
                for f in os.listdir(pull_requests_dir)
                if f.startswith(f"pull_request_{task_id}")
            ]
            if len(pull_request_dirs) == 0:
                log_and_print(f"No pull requests found for task ID: {task_id}")
                return

            log_and_print("Solved the assigned issue")
            pull_request_dirs.sort(key=lambda x: int(x.split("_v")[-1]))
            most_recent_pull_request = pull_request_dirs[-1]
            pull_request_dir = os.path.join(pull_requests_dir, most_recent_pull_request)

            pr_accepted = selected_maintainer.review_pull_request(
                pull_request_dir, project_dir
            )
            if pr_accepted:
                log_and_print(
                    f"Maintainer {selected_maintainer.name} has merged pull request for Issue #{issue.id}.\n"
                )
                # increase experience of the contributor
                selected_contributor.increase_experience(1)
                # increase no of pull requests and calculate new average code quality of the simulation
                try:
                    sim.update_pull_requests(int(pr_accepted))
                except:
                    sim.update_code_quality(random.randint(1, 5))

                # make a "merged" folder in the pull_requests folder and move the merged pull request there
                merged_dir = os.path.join(project_dir, "pull_requests", "merged")
                os.makedirs(merged_dir, exist_ok=True)
                merged_pull_request_dir = os.path.join(
                    merged_dir, most_recent_pull_request
                )
                os.rename(pull_request_dir, merged_pull_request_dir)
                # delete the other versions of the pull request for the same task_id
                for pr_dir in pull_request_dirs:
                    if pr_dir == most_recent_pull_request:
                        continue
                    if pr_dir.startswith(f"pull_request_{task_id}"):
                        pr_dir_path = os.path.join(pull_requests_dir, pr_dir)
                        shutil.rmtree(pr_dir_path)

                # make a "solved" folder in the issues folder and move the solved issue there
                solved_dir = os.path.join(project_dir, "issues", "solved")
                os.makedirs(solved_dir, exist_ok=True)
                solved_issue_path = os.path.join(solved_dir, f"task_{task_id}.md")
                os.rename(issue.filepath, solved_issue_path)
                repo_commit_current_changes(project_dir)

            else:
                log_and_print(
                    f"Maintainer {selected_maintainer.name} has rejected pull request for Issue #{issue.id}.\n"
                )
                # TODO : make a "rejected" folder in the pull_requests folder and move the rejected pull request there

        else:
            log_and_print("Error solving the assigned issue")
            return
        # print sim metrics : pull_requests and code_quality
        log_and_print(
            f"\nSimulation metrics: Pull Requests = {sim.num_pull_requests} Average Code Quality = {sim.avg_code_quality}\n"
        )

        # Append new experiences to history
        time_history.append(timestep)
        for contributor in contributors:
            experience_history[contributor.name].append(contributor.experience)

        # Update lines data
        for contributor in contributors:
            lines_cont_exp[contributor.name].set_data(
                time_history, experience_history[contributor.name]
            )

        # Draw the updated plot
        plt.draw()
        plt.pause(0.1)

    init_plot(
        axis=ax_cont_exp,
        x_label="Time Step",
        y_label="Contributor Experience",
        y_max=max(contributor.experience for contributor in contributors),
        title="Contributor Experience Metric",
        lines=lines_cont_exp,
    )
    # Loop through all the issues in the issues list
    # Review the pull requests
    pull_requests_dir = os.path.join(project_dir, "pull_requests")
    for issue in issues:
        update(timestep)
        timestep += 1
        # Print a separator for better readability
        print("\n", "-" * 100, "\n")

    plt.show()


if __name__ == "__main__":
    main()
