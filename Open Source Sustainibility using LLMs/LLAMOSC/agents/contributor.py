import os
import docker
from datetime import datetime
import tarfile
import io

from LLAMOSC.utils import *


class ContributorAgent:
    def __init__(self, id, experience, name):
        self.id = id
        self.experience = experience
        self.available = True
        self.name = name
        self.assigned_issue = None

    def eligible_for_issue(self, issue):
        return self.available and self.experience >= issue.difficulty

    def assign_issue(self, issue):
        self.assigned_issue = issue
        self.available = False
        log_and_print(f"Contributor {self.name} has been allotted Issue #{issue.id}.\n")
        return self.assigned_issue

    def unassign_issue(self):
        self.assigned_issue = None
        self.available = True

    def solve_issue(self, project_dir):
        if self.assigned_issue is not None:
            # Initialize Docker client
            client = docker.from_env()

            # stop any running containers
            stop_running_containers()
            # Create and start a new Docker container
            try:
                volume_bindings = {
                    project_dir: {
                        "bind": "/home/calculator_project",
                        "mode": "rw",
                    }
                }

                ports = {"3000/tcp": 3000, "5000/tcp": 5000}

                container = client.containers.run(
                    "acr1",
                    ports=ports,
                    volumes=volume_bindings,
                    detach=True,
                    tty=True,
                )
            except Exception as e:
                print(f"Error starting container: {e}")
                stop_running_containers()
                exit(1)

            task_id = self.assigned_issue.id
            # Command to activate conda environment and run Python script
            commands = [
                "/bin/bash",
                "-c",
                f"source activate auto-code-rover && PYTHONPATH=. python app/main.py local-issue --output-dir output --model llama3 --enable-validation --conv-round-limit 5 --task-id {task_id} --local-repo /home/calculator_project --issue-file /home/calculator_project/issues/pending/task_{task_id}.md",
            ]

            # Execute command inside the container and stream output
        try:
            exec_log = container.exec_run(commands, stream=True, tty=True)

            # Stream the output to the terminal
            for line in exec_log.output:
                try:
                    l = line.decode()
                except Exception:
                    l = line

                print(l, end="")

            # Find the most recent .diff file in the container
            task_id = self.assigned_issue.id
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

            local_pull_requests_dir = os.path.join(project_dir, "pull_requests")
            if not os.path.exists(local_pull_requests_dir):
                print(
                    f"Creating directory: {local_pull_requests_dir} as it does not already exist"
                )
                os.makedirs(local_pull_requests_dir)

            task_id = self.assigned_issue.id
            version = len(
                [
                    f
                    for f in os.listdir(local_pull_requests_dir)
                    if f.startswith(f"pull_request_{task_id}")
                ]
            )
            pull_request_name = f"pull_request_{task_id}_v{version+1}"
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

            container.stop()
            container.remove()

            # Make a pr.md file for in the pull_request folder

            with open(self.assigned_issue.filepath, "r") as issue_file:
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
            log_and_print(f"Generated pull request content: {pr_content}")
            pr_file_path = os.path.join(local_pull_request_dir, "pr.md")
            with open(pr_file_path, "w") as pr_file:
                pr_file.write(pr_content)
            log_and_print(f"Created pull request file: {pr_file_path}")

            # commit the changes made i.e adding the pull_requests folder and the pull request file
            repo_commit_current_changes(project_dir)
            log_and_print(
                f"Contributor {self.name} has created pull request for Issue #{self.assigned_issue.id}.\n"
            )
            self.unassign_issue()
            return True

        except Exception as e:
            print(f"Error executing command in container: {e}")
            stop_running_containers()
            self.unassign_issue()
            return False
            exit(1)
