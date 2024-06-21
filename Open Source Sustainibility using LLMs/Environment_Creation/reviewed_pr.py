import sys
import sys
from dataclasses import dataclass
import os
import docker


@dataclass
class Issue:
    issue_no: int
    issue_id: str
    file_path: str


# Global list of issues
issues = []


class ContributorAgent:
    def __init__(self, name, docker_container_id):
        self.name = name
        self.assigned_issue = None
        self.docker_container_id = (
            "17f9d0abecaac64204efa32621118366cb5fe8471f2e9d0537293b6b4b4f5b85"
        )

    def assign_issue(self, issue):
        self.assigned_issue = issue

    def solve_issue(self):
        if self.assigned_issue is not None:
            # working on command line
            #             import docker
            # >>> client = docker.from_env()
            # >>> container = client.containers.get('17f9d0abecaa')
            # >>> container.exec_run('pwd') # problem : conda command not working
            # >>> container.stop()

            # Call autocoderover command
            command = f"docker start -i -a {self.docker_container_id}"
            # Execute the command
            # os.system(command)
            # Execute the command and print the output
            output = os.popen(command).read()
            print(output)
            command = " conda activate auto-code-rover"
            command += f" && PYTHONPATH=. python app/main.py local-issue --output-dir output --model llama3 --task-id 1 --local-repo /home/calculator_project --issue-file /home/calculator_project/issues/task_1.md"
            # Execute the command and print the output
            output = os.popen(command).read()
            print(output)
            # # Write pull request based on the path created by autocderover
            # # ...
            # pull_request_path = os.path.join("output", "pull_request.md")
            # with open(pull_request_path, "r") as file:
            #     pull_request_content = file.read()

            # # Do something with the pull request content
            # # ...
            # # For example, print the pull request content
            # print(pull_request_content)

            # Write pull request based on the path created by autocderover
            # ...


def main():
    # Get the path to the issues folder
    print("Getting the path to the issues folder...")
    issues_folder = "./calculator_project/issues"
    issue_counter = 0
    print(f"Issues folder: {issues_folder}")

    # Loop through all the files in the issues folder
    print("Looping through all the files in the issues folder...")
    for filename in os.listdir(issues_folder):
        # Create the file path
        file_path = os.path.join(issues_folder, filename)
        print(f"File path: {file_path}")

        # Extract the issue id from the filename
        issue_id = filename.split("_")[1].split(".")[0]
        print(f"Issue ID: {issue_id}")

        # Create the issue object
        issue_counter += 1
        issue = Issue(issue_counter, issue_id, file_path)
        print(f"Created issue: {issue}")

        # Add the issue to the issues list
        issues.append(issue)
        print("Added issue to the issues list")

    # Create an agent
    agent = ContributorAgent("Contributor_1")
    print(f"Created agent: {agent}")

    # Loop through all the issues in the issues list
    print("Looping through all the issues in the issues list...")
    for issue in issues:
        # Assign an issue from the available issues to the agent
        agent.assign_issue(issue)
        print(f"Assigned issue to agent: {issue}")

        # Solve the assigned issue
        agent.solve_issue()
        print("Solved the assigned issue")

        # Print the assigned issue
        print(f"Assigned issue: {agent.assigned_issue}")

        # Print a separator for better readability
        print("-" * 50)


if __name__ == "__main__":
    main()
