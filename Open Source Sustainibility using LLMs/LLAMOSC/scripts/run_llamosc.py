# A script that combines all the functions of the LLAMOSC project
# (currently in reviewed_pr_.. scripts and new ones)
# to run the simulation with the options taken from user

# TODO : put reading issues part in a function and store both pending and solved
# TODO optional : use above function to make dynamic like new issues in the middle of the simulation as well
# TODO : put full run_simulation in a function that just takes args from here and plots everything
# was working on reviewed_pr-auth - experience metric done rest remaining

# TODO DOING
# TODO : plot issues (pending,solved,moon-shot-earthshotetc) and
# TODO : plot motivation_level metric


# TODO : Make docker optional - TODO done.
# TODO : takes options for choosing between authoritarian and decentralized - TODO done
# TODO : add metrics - contributor experience & simulation issues - TODO done
# TODO : in average code quality show both current code quality and average code quality - TODO done
# TODO : add code quality metric, llm response and graph - TODO done
# TODO : parser args no of agents, no of issues, no of tasks, etc. - TODO done
# TODO : automatically makes issues - TODO done issue_creator agent
# TODO : personalization for each contributor - TODO done
# TODO : add motivation_level metric - TODO done

import shutil
import random

from matplotlib.axes import Axes

from LLAMOSC.agents.contributor import ContributorAgent
from LLAMOSC.agents.maintainer import MaintainerAgent
from LLAMOSC.agents.issue_creator import IssueCreatorAgent
from LLAMOSC.simulation.issue import Issue
from LLAMOSC.simulation.sim import Simulation
from LLAMOSC.utils import *
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def init_plot(axis: Axes, x_label, y_label, x_max, y_max, title, lines):
    axis.set_xlim(0, x_max + 1)
    axis.set_ylim(0, y_max + 1)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    axis.set_title(title)
    axis.legend()
    # return lines.values()


def main():

    parser = argparse.ArgumentParser(description="LLAMOSC Simulation")
    parser.add_argument(
        "--contributors", type=int, default=5, help="Number of contributors"
    )
    parser.add_argument(
        "--maintainers", type=int, default=3, help="Number of maintainers"
    )
    parser.add_argument("--issues", type=int, default=5, help="Number of issues")
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
    n_issues = args.issues
    # n_tasks = args.tasks
    use_acr = args.use_acr
    algorithm = args.algorithm

    issues = []
    current_folder = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(
        current_folder, "..", "..", "..", "..", "calculator_project"
    )

    # Clear the project directory
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
        # TODO: Better way to get issue difficulty
        issue = Issue(issue_id, (issue_id + 1) % 5, file_path)

        # Add the issue to the issues list
        issues.append(issue)

    if len(issues) < n_issues:
        issue_creator = IssueCreatorAgent(name="Issue Creator")
        existing_code = """"""

        for root, _, files in os.walk(project_dir):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file), "r") as code_file:
                        existing_code += code_file.read() + "\n"

        # create the required number of issues
        for _ in range(len(issues) + 1, n_issues + 1):
            issue = issue_creator.create_issue(issues, existing_code, issues_folder)
            issues.append(issue)

    # Create required agents
    contributors = [
        ContributorAgent(i, random.randint(1, 4), f"Contributor_{i}")
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
    timestep = 0
    experience_history = {
        contributor.name: [contributor.experience] for contributor in contributors
    }
    code_qal_history = [2.5]  # just a basic average to start with
    code_qal_curr_history = [2.5]  # just a basic average to start with
    time_history = [0]

    log_and_print(
        f"\nStarting simulation with {len(issues)} issues and {len(contributors)} contributors with ACR : {use_acr} and Algorithm : {algorithm}.\n"
    )

    fig, (ax_cont_exp, ax_code_qal) = plt.subplots(2, 1)
    lines_cont_exp = {
        contributor.name: ax_cont_exp.plot(
            time_history, experience_history[contributor.name], label=contributor.name
        )[0]
        for contributor in contributors
    }
    lines_code_qal = {
        "avg": ax_code_qal.plot(
            time_history, code_qal_history, label="Average Code Quality", color="blue"
        )[0],
        "curr": ax_code_qal.plot(
            time_history,
            code_qal_curr_history,
            label="Current Code Quality",
            color="red",
        )[0],
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
            selected_contributor = sim.select_contributor_decentralized(issue)[0]
        else:
            selected_contributor = sim.select_contributor_authoritarian(
                selected_maintainer
            )[0]

        # Assign an issue from the available issues to the agent
        if not selected_contributor:
            selected_contributor = [
                contributor
                for contributor in contributors
                if contributor.eligible_for_issue(issue)
            ][0]

        log(selected_contributor.name)
        # TODO : if no eligible contributors, loop until the issue is solved
        # for other contributors who bid/rated but not selected

        for other_contributor in contributors:
            if other_contributor.id == selected_contributor.id:
                continue
            elif not other_contributor.eligible_for_issue(issue):
                continue
            other_contributor.update_motivation_level(bid_selected=False)

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
                selected_contributor.increase_experience(1, issue.difficulty)
                # increase no of pull requests and calculate new average code quality of the simulation
                try:
                    sim.update_code_quality(pr_accepted)
                except:

                    pr_accepted = sim.update_code_quality(random.randint(1, 3))

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

        # update selected_contributor motivation level
        selected_contributor.update_motivation_level(
            success=pr_accepted,
            bid_selected=True,
            task_difficulty=issue.difficulty,
            code_quality=pr_accepted if pr_accepted else random.randrange(0, 3),
        )

        # Append new experiences to history
        time_history.append(timestep)
        for contributor in contributors:
            experience_history[contributor.name].append(contributor.experience)
        code_qal_history.append(sim.avg_code_quality)
        (
            code_qal_curr_history.append(pr_accepted)
            if pr_accepted
            else code_qal_curr_history.append(random.randint(1, 3))
        )
        log(time_history), log(experience_history), log(code_qal_history)

        # Update contributor_exp metric lines data
        for contributor in contributors:
            lines_cont_exp[contributor.name].set_data(
                time_history, experience_history[contributor.name]
            )

        # Update code_quality metric line data
        lines_code_qal["avg"].set_data(time_history, code_qal_history)
        lines_code_qal["curr"].set_data(time_history, code_qal_curr_history)

        # Draw the updated plot
        plt.draw()
        plt.pause(0.1)

    # init metrics 1 plot
    init_plot(
        axis=ax_cont_exp,
        x_label="Time Step",
        y_label="Contributor Experience",
        x_max=len(issues),
        y_max=5,
        title="Contributor Experience Metric",
        lines=lines_cont_exp,
    )

    init_plot(
        axis=ax_code_qal,
        x_label="Time Step",
        y_label="Code Quality",
        x_max=len(issues),
        y_max=5,
        title="Simulation Average Code Quality Metric",
        lines=lines_code_qal,
    )

    # draw the initial plot
    plt.draw()
    plt.pause(0.1)

    # Loop through all the issues in the issues list
    # Review the pull requests
    pull_requests_dir = os.path.join(project_dir, "pull_requests")
    for issue in issues:
        timestep += 1
        update(timestep)
        # Print a separator for better readability
        print("\n", "-" * 100, "\n")

    plt.show()


if __name__ == "__main__":
    main()
