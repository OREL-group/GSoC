import sys
import sys
from dataclasses import dataclass
import os
import docker
from datetime import datetime

import tarfile
import io


from langchain_community.llms import Ollama


@dataclass
class Issue:
    issue_no: int
    issue_id: str
    file_path: str


# Global list of issues
issues = []


def query_ollama(prompt):
    llm = Ollama(model="llama3")
    res = llm.invoke(prompt, stop=["<|eot_id|>"])
    print(f"OLLAMA response: {res}")
    return res


class ContributorAgent:
    def __init__(self, name):
        self.name = name
        self.assigned_issue = None
        self.docker_container_id = (
            "17f9d0abecaac64204efa32621118366cb5fe8471f2e9d0537293b6b4b4f5b85"
        )

    def assign_issue(self, issue):
        self.assigned_issue = issue

    def unassign_issue(self, issue):
        self.assigned_issue = None

    def solve_issue(self):
        if self.assigned_issue is not None:
            # Initialize Docker client
            client = docker.from_env()

            # Start and attach to the Docker container
            try:
                container = client.containers.get(self.docker_container_id)
                if container.status != "running":
                    container.start()
                    print(f"Container {self.docker_container_id} started.")
                else:
                    print(f"Container {self.docker_container_id} is already running.")
            except Exception as e:
                print(f"Error starting container: {e}")
                exit(1)
            task_id = self.assigned_issue.issue_id
            # Command to activate conda environment and run Python script
            commands = [
                "/bin/bash",
                "-c",
                f"source activate auto-code-rover && PYTHONPATH=. python app/main.py local-issue --output-dir output --model llama3 --task-id {task_id} --local-repo /home/calculator_project --issue-file /home/calculator_project/issues/task_{task_id}.md",
            ]

            # Execute command inside the container and stream output
        try:
            # exec_log = container.exec_run(commands, stream=True, tty=True)

            # # Stream the output to the terminal
            # for line in exec_log.output:
            #     try:
            #         l = line.decode()
            #     except Exception:
            #         l = line

            #     print(l, end="")

            # Find the most recent .diff file in the container
            task_id = self.assigned_issue.issue_id
            print(f"Finding the most recent .diff file for task ID: {task_id}...")
            output_dir = "/opt/auto-code-rover/output"
            output_files = (
                container.exec_run(["ls", output_dir]).output.decode().split("\n")
            )
            task_dirs = [f for f in output_files if f.startswith(f"{task_id}_")]

            if not task_dirs:
                print("No directories found for the given task ID.")
                return

            # Sort the directories by their timestamp and select the most recent one
            task_dirs.sort(
                key=lambda x: datetime.strptime(
                    x.split("_")[1] + "_" + x.split("_")[2], "%Y-%m-%d_%H-%M-%S"
                ),
                reverse=True,
            )
            most_recent_dir = task_dirs[0]

            # Find the .diff file in the most recent directory
            diff_file_path = None
            recent_dir_files = (
                container.exec_run(["ls", f"{output_dir}/{most_recent_dir}"])
                .output.decode()
                .split("\n")
            )
            for file_name in recent_dir_files:
                if file_name.endswith(".diff"):
                    diff_file_path = f"{output_dir}/{most_recent_dir}/{file_name}"
                    break

            if diff_file_path is None:
                print("No .diff file found in the most recent directory.")
                return

            local_pull_requests_dir = ".\calculator_project\pull_requests"
            if not os.path.exists(local_pull_requests_dir):
                os.makedirs(local_pull_requests_dir)

            task_id = self.assigned_issue.issue_id
            pull_request_name = f"pull_request_{task_id}"
            local_pull_request_dir = os.path.join(
                local_pull_requests_dir, pull_request_name
            )
            os.makedirs(local_pull_request_dir, exist_ok=True)

            local_diff_file_path = os.path.join(
                local_pull_request_dir, f"{pull_request_name}.diff"
            )

            # Copy the file from container to local system using docker-py
            bits, stat = container.get_archive(diff_file_path)
            tar_stream = io.BytesIO(b"".join(bits))
            with tarfile.open(fileobj=tar_stream) as tar:
                tar.extractall(path=local_pull_request_dir)

            # Rename the extracted file to the desired name
            extracted_file_path = os.path.join(
                local_pull_request_dir, os.path.basename(diff_file_path)
            )
            os.rename(extracted_file_path, local_diff_file_path)
            # container.stop()
            print(f"Copied .diff file to {local_diff_file_path}")

            # Make a pr.md file for in the pull_request folder

            with open(self.assigned_issue.file_path, "r") as issue_file:
                issue_content = issue_file.read()
                print(f"Read issue content: {issue_content}")

            with open(local_diff_file_path, "r") as diff_file:
                diff_content = diff_file.read()
                print(f"Read diff content: {diff_content}")

            # Query OLLAMA to generate appropriate PR content based on the diff
            prompt = f"""As a contributor in an open source environment, your role is to 
            participate in the development process by solving assigned issues 
            and creating pull requests. 
            You have currently solved issue : {issue_content} and stored its result in the diff file. 
            Generate a pull request based on the following diff file: {diff_content}. 
            Please provide a brief description of the changes made.
            Keep ypur answer to a maximum of 10 sentenecs and don't include any actual code in it.
            Use the following template for the pull request:
            Issue Summary: \n\n       Approach:    \n\n"""

            pr_content = query_ollama(prompt=prompt)
            print(f"Generated pull request content: {pr_content}")
            pr_file_path = os.path.join(local_pull_request_dir, "pr.md")
            with open(pr_file_path, "w") as pr_file:
                pr_file.write(pr_content)
            print(f"Created pull request file: {pr_file_path}")

        except Exception as e:
            print(f"Error executing command in container: {e}")
            exit(1)


# class MaintainerAgent:
#     # a agent that will review the pull request and if accepted


def main():
    # Get the path to the issues folder
    print("Getting the path to the issues folder...")
    issues_folder = ".\\calculator_project\\issues"
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

        # Print the assigned issue
        print(f"Assigned issue: {agent.assigned_issue}")

        # Solve the assigned issue
        agent.solve_issue()
        print("Solved the assigned issue")

        # Print a separator for better readability
        print("-" * 50)

        agent.unassign_issue(issue)


if __name__ == "__main__":
    main()
