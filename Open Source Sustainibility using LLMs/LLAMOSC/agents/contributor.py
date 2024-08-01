import os
import docker
from datetime import datetime
import tarfile
import io
import random

from LLAMOSC.utils import *

# TODO : add personalization to the prompt to put story for each contributor
# game_description = f"""Here is the topic for a Dungeons & Dragons game: {quest}.
#         The characters are: {*character_names,}.
#         The story is narrated by the storyteller, {storyteller_name}."""

# player_descriptor_system_message = SystemMessage(
#     content="You can add detail to the description of a Dungeons & Dragons player."
# )


# def generate_character_description(character_name):
#     character_specifier_prompt = [
#         player_descriptor_system_message,
#         HumanMessage(
#             content=f"""{game_description}
#             Please reply with a creative description of the character, {character_name}, in {word_limit} words or less.
#             Speak directly to {character_name}.
#             Do not add anything else."""
#         ),
#     ]
#     character_description = ChatOpenAI(temperature=1.0)(
#         character_specifier_prompt
#     ).content
#     return character_description


# def generate_character_system_message(character_name, character_description):
#     return SystemMessage(
#         content=(
#             f"""{game_description}
#     Your name is {character_name}.
#     Your character description is as follows: {character_description}.
#     You will propose actions you plan to take and {storyteller_name} will explain what happens when you take those actions.
#     Speak in the first person from the perspective of {character_name}.
#     For describing your own body movements, wrap your description in '*'.
#     Do not change roles!
#     Do not speak from the perspective of anyone else.
#     Remember you are {character_name}.
#     Stop speaking the moment you finish speaking from your perspective.
#     Never forget to keep your response to {word_limit} words!
#     Do not add anything else.
#     """
#         )
#     )


# character_descriptions = [
#     generate_character_description(character_name) for character_name in character_names
# ]
# character_system_messages = [
#     generate_character_system_message(character_name, character_description)
#     for character_name, character_description in zip(
#         character_names, character_descriptions
#     )
# ]

# storyteller_specifier_prompt = [
#     player_descriptor_system_message,
#     HumanMessage(
#         content=f"""{game_description}
#         Please reply with a creative description of the storyteller, {storyteller_name}, in {word_limit} words or less.
#         Speak directly to {storyteller_name}.
#         Do not add anything else."""
#     ),
# ]
# storyteller_description = ChatOpenAI(temperature=1.0)(
#     storyteller_specifier_prompt
# ).content


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

    def increase_experience(self, exp=1):
        if self.experience < 5:
            self.experience += exp  # Increase experience by 1
        # maximum experience can be 5

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
                log(f"Error starting container: {e}")
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
            output_dir = "/opt/auto-code-rover/output"
            output_files = (
                container.exec_run(["ls", output_dir]).output.decode().split("\n")
            )
            task_dirs = [f for f in output_files if f.startswith(f"{task_id}_")]

            if not task_dirs:
                log("No directories found for the given task ID.")
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
                log("No .diff file found in the most recent directory.")
                return

            local_pull_requests_dir = os.path.join(project_dir, "pull_requests")
            if not os.path.exists(local_pull_requests_dir):
                log(
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

            container.stop()
            container.remove()

            # Make a pr.md file for in the pull_request folder

            with open(self.assigned_issue.filepath, "r") as issue_file:
                issue_content = issue_file.read()

            with open(local_diff_file_path, "r") as diff_file:
                diff_content = diff_file.read()

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
            log_and_print(f"Error executing command in container: {e}")
            stop_running_containers()
            self.unassign_issue()
            return False
            exit(1)

    def solve_issue_without_acr(self, project_dir):
        if self.assigned_issue is not None:
            task_id = self.assigned_issue.id

        # Instead of executing acr to solve the issue, we will use rng to decide if the issue is solved or not
        # if random.randint(0, 1) == 1: # 50 % cance is too little

        if True:

            # Find the most recent .diff file in the container
            task_id = self.assigned_issue.id

            local_pull_requests_dir = os.path.join(project_dir, "pull_requests")
            if not os.path.exists(local_pull_requests_dir):
                log(
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

            # Since there is no real diff file to copy, we will leave our diff file empty
            with open(local_diff_file_path, "w") as diff_file:
                diff_file.write("")
            log_and_print(f"Created empty diff file: {local_diff_file_path}")

            # Make a pr.md file for in the pull_request folder

            with open(self.assigned_issue.filepath, "r") as issue_file:
                issue_content = issue_file.read()

            with open(local_diff_file_path, "r") as diff_file:
                diff_content = diff_file.read()  # will be empty

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

        else:
            log_and_print(f"Some error while trying to solve issue")
            self.unassign_issue()
            return False
            exit(1)


# c = ContributorAgent(1, 2, "John")
# current_folder = os.path.dirname(os.path.abspath(__file__))
# project_dir = os.path.join(current_folder, "..", "..", "..", "..", "calculator_project")
# c.solve_issue_without_acr(project_dir)
