import shutil
import random

from LLAMOSC.agents.contributor import ContributorAgent
from LLAMOSC.agents.maintainer import MaintainerAgent
from LLAMOSC.simulation.issue import Issue
from LLAMOSC.simulation.sim import Simulation
from LLAMOSC.simulation.rating_and_bidding import *
from LLAMOSC.utils import *


def main():
    issues = []
    current_folder = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(
        current_folder, "..", "..", "..", "..", "calculator_project"
    )
    # initialize_git_repo_and_commit(project_dir)
    repo_commit_current_changes(project_dir)

    log_and_print("Reading issues from the issues folder...")
    # Get the path to the issues folder
    # current folder
    issues_parent_folder = os.path.join(project_dir, "issues")
    issues_folder = os.path.join(issues_parent_folder, "pending")
    issue_counter = 0
    # Loop through all the files in the issues folder
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

    # Create reuired agents
    # TODO : Later make this number choosable
    n_contributors = 5
    contributors = [
        ContributorAgent(i, random.randint(1, 5), f"Contributor_{i}")
        for i in range(n_contributors)
    ]
    n_mainainers = 3
    maintainers = [
        MaintainerAgent(i, random.randint(4, 5), f"Maintainer_{i}")
        for i in range(n_mainainers)  # 3 maintainers
    ]

    log_and_print(f"Created agents: contributors and maintainers")

    sim = Simulation(contributors)
    time = 0

    log_and_print(
        f"\nStarting simulation with {len(issues)} issues and {len(contributors)} contributors.\n"
    )

    # Loop through all the issues in the issues list
    # Review the pull requests
    pull_requests_dir = os.path.join(project_dir, "pull_requests")
    for issue in issues:
        log_and_print(f"\nTime Step: {time}\n")
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
        selected_contributor = sim.select_contributor_decentralized(issue)
        # Assign an issue from the available issues to the agent
        if selected_contributor:
            # TODO : if no eligible contributors, loop until the issue is solved
            selected_contributor.assign_issue(issue)
            task_solved = selected_contributor.solve_issue(project_dir)
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
                    continue
                log_and_print("Solved the assigned issue")
                pull_request_dirs.sort(key=lambda x: int(x.split("_v")[-1]))
                most_recent_pull_request = pull_request_dirs[-1]
                pull_request_dir = os.path.join(
                    pull_requests_dir, most_recent_pull_request
                )

                pr_accepted = selected_maintainer.review_pull_request(
                    pull_request_dir, project_dir
                )
                if pr_accepted:
                    log_and_print(
                        f"Maintainer {selected_maintainer.name} has merged pull request for Issue #{issue.id}.\n"
                    )
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
            time += 1

        else:
            selected_contributor = [
                contributor
                for contributor in contributors
                if contributor.eligible_for_issue(issue)
            ][0]
            time += 1

        # Print a separator for better readability
        print("\n", "-" * 100, "\n")


if __name__ == "__main__":
    main()
