import os
import docker
from datetime import datetime

import tarfile
import io
import random

from LLAMOSC.utils import *
from LLAMOSC.simulation.bid_output_parser import QualityRatingParser
from LLAMOSC.simulation.issue import Issue
from langchain.schema import SystemMessage, HumanMessage

community_description = (
    "Our open-source community is focused on collaborative learning and innovation."
)


class ContributorAgent:
    def __init__(self, id, experience, name, testing=False):
        self.id = id
        self.experience = experience
        self.available = True
        self.motivation_level = type(int)  # 0 to 5
        self.motivation_history = []
        self.name = name
        self.assigned_issue = type(Issue)

        if testing:
            self.role_description = "This is a test role description."
            self.system_message = SystemMessage(
                content="This is a test system message."
            )
            self.motivation_level = random.randint(3, 10)
            self.motivation_history.append(self.motivation_level)
            return

        # Generate a personalized role and system message
        self.role_description = self.generate_role_description()
        log_and_print(
            f"Generated role description for {self.name}:\n{self.role_description}\n"
        )
        self.system_message = self.generate_role_system_message(community_description)
        log_and_print(
            f"Generated system message for {self.name}:\n{self.system_message.content}\n"
        )
        self.motivation_level = self.generate_initial_motivation_level()
        self.motivation_history.append(
            self.motivation_level
        )  # append initial motivation level

    def generate_role_description(self, word_limit=50):
        """
        Generates a creative description for a role in the open-source community based on experience.
        """
        role_specifier_prompt = f"""
        Welcome to our open-source community! This is a place where people of all backgrounds and 
        experiences come together to collaborate, learn, and grow.
        The role you are creating is Contributor, and the experience level is {self.experience}.
        Your response should be one of "positive or negative or neutral" sentiment, NOT ALWAYS POSITIVE.
        Some contributors can eb explorers, some can be lurkers, some can be potential leaders & mentors, 
        some incentivized by funded programs, some just plain selfish. It is your job to pick one of these, 
        not ALWAYS POSITIVE and do the following based on it. 
        Please reply with a creative description and unique, different-for-everyone 
        backstory of the role, Contributor {self.name}. 
        Especially how they must have entered the community if they are a very low experience level (between 1 t 3)
        and how involved they are in it now & why if they are at a high experience level.
        Speak about the motivation to stay (this can be incentivized rarely as well)
        and engage and how they contribute to the community considering their experience level.
        Keep the description within {word_limit} words. Speak directly to {self.name}.
        Do not add anything else.
        """

        role_description = query_ollama(role_specifier_prompt)
        return role_description

    def generate_role_system_message(self, community_description, word_limit=50):
        """
        Generates a system message for the role, guiding their interactions in the community based on their experience.
        """
        return SystemMessage(
            content=(
                f"""{community_description}
        Your name is {self.name}.
        Your role description is as follows: {self.role_description}.
        You have {self.experience} experience in the field.
        You will interact in the community as Contributor {self.name}, 
        taking actions like commiting code via pull requests and contributing to discussions.
        Speak in the first person from the perspective of Contributor {self.name}.
        For describing your own body movements, wrap your description in '*'.
        Do not change roles!
        Do not speak from the perspective of anyone else.
        Remember you are Contributor {self.name}.
        Stop speaking the moment you finish speaking from your perspective.
        Never forget to keep your response to {word_limit} words!
        Do not add anything else.
        """
            )
        )

    def generate_initial_motivation_level(self):
        """
        Generates a motivation level for the contributor based on their role description by using parser.
        """
        # Define the motivation level parser
        motivation_parser = QualityRatingParser(
            regex=r"<(\d)>", output_keys=["rating"], default_output_key="rating"
        )

        # Query OLLAMA to generate the motivation level
        prompt_motivation = f"""As a contributor in an open-source community, your role is to 
        participate in the development process by solving assigned issues and creating pull requests. 
        Based on your following role description: {self.role_description}, rate your motivation level from 0 to 10, 
        where 0 is very low and 10 is very high. 
        Your motivation level should be reflective of the role description you have created. 
        For example, lurkers usually have low motivation whereas potential leaders have high motivation.
        Explorers have medium motivation and so on.
        {motivation_parser.get_format_instructions()}
        Do nothing else.
        """
        motivation_level_desc = query_ollama(prompt=prompt_motivation)
        try:
            motivation_level = float(
                motivation_parser.parse(motivation_level_desc)["rating"]
            )
        except:
            motivation_level = 5  # neutral motivation level
        log(f"Generated initial motivation level: {motivation_level}")
        return motivation_level

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

    def increase_experience(self, adding_exp=1, task_difficulty=5):
        # Calculate the base experience increase
        base_increase = min(5 - self.experience, adding_exp)

        # Apply variability: experience increase could be a bit more or less than the base
        variability = random.uniform(0.4, 0.6)  # Adjusted to ensure at least 0.5 change
        variability_adjusted_increase = base_increase + variability

        # Scale the increase based on task difficulty (optional: adjust scaling factor)
        difficulty_adjusted_increase = variability_adjusted_increase * (
            task_difficulty / 5
        )

        # Clip experience increase to ensure it does not exceed the max allowed experience
        final_increase = min(difficulty_adjusted_increase, 5 - self.experience)

        # Increase experience
        self.experience += round(final_increase, 2)

        # Optional: Print or log experience changes for debugging
        print(f"Experience increased by: {round(final_increase, 2):.2f}")

    def update_motivation_level(
        self, success=True, bid_selected=False, task_difficulty=3, code_quality=4
    ):
        # Use the history of motivation to adjust the current motivation level
        if len(self.motivation_history) > 0:
            average_past_motivation = sum(self.motivation_history) / len(
                self.motivation_history
            )
            # Adjust motivation increase/decrease based on past trends
            motivation_trend = (self.motivation_level - average_past_motivation) * 0.2
        else:
            motivation_trend = 0

        # If the contributor was not selected for the task
        if not bid_selected:
            # Decrease motivation based on not being selected
            motivation_decrease = max(
                min(self.motivation_level, 0.05 * task_difficulty), 0.5
            )
            self.motivation_level -= motivation_decrease
            # Skip other updates related to success, task_difficulty, and code_quality
        else:
            # Adjust motivation based on whether the contributor's PR was merged
            if success:
                motivation_increase = max(
                    min(10 - self.motivation_level, 0.1 * task_difficulty), 0.5
                )
                self.motivation_level += motivation_increase
            else:
                motivation_decrease = max(
                    min(self.motivation_level, 0.1 * task_difficulty), 0.5
                )
                self.motivation_level -= motivation_decrease

            # Adjust motivation based on code quality (0-5 scale)
            if code_quality > 4:
                motivation_increase = max(0.1 * (code_quality - 4), 0.5)
                self.motivation_level += motivation_increase
            elif code_quality < 2:
                motivation_decrease = max(0.1 * (2 - code_quality), 0.5)
                self.motivation_level -= motivation_decrease
            else:  # Code quality between 2 and 4
                if code_quality <= 3:
                    motivation_decrease = max(0.05 * (3 - code_quality), 0.5)
                    self.motivation_level -= motivation_decrease
                elif code_quality > 3:
                    motivation_increase = max(0.05 * (code_quality - 3), 0.5)
                    self.motivation_level += motivation_increase

        # Apply small random fluctuation to simulate real-life variability
        fluctuation = random.uniform(0.4, 0.6)  # Ensures at least 0.5 change
        self.motivation_level += (
            fluctuation if random.choice([True, False]) else -fluctuation
        )

        # Incorporate historical trend adjustment
        self.motivation_level += motivation_trend

        # Clip motivation level to stay within 0 to 10
        self.motivation_level = max(0, min(10, round(self.motivation_level, 2)))

        # Track the history of motivation
        self.motivation_history.append(self.motivation_level)
        log("!!-------------------------------------------------!!")
        log_and_print(
            f"Motivation level for contributor {self.name}: {self.motivation_history}"
        )

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
            Keep your answer to a maximum of 10 sentences and don't include any actual code in it.
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

    def solve_issue_without_acr(self, project_dir, is_test=False):
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
            Keep your answer to a maximum of 10 sentences and don't include any actual code in it.
            Use the following template for the pull request:
            Issue Summary: \n\n       Approach:    \n\n"""
            if is_test:
                pr_content = prompt
            else:
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


# # Example Usage
# if __name__ == "__main__":

#     # Create a ContributorAgent instance
#     contributor = ContributorAgent(id=1, experience=4, name="John Doe")

#     current_folder = os.path.dirname(os.path.abspath(__file__))
#     project_dir = os.path.join(
#         current_folder, "..", "..", "..", "..", "calculator_project"
#     )

#     # Assign a mock issue (assuming issue object with id and difficulty attributes)
#     issue = type(
#         "Issue",
#         (object,),
#         {
#             "id": 101,
#             "difficulty": 2,
#             "filepath": "D:\Personal_Projects\GSoC_24\calculator_project_base_copy\issues\task_2.md",
#         },
#     )
#     contributor.assign_issue(issue)

#     # # Solve the issue
#     # contributor.solve_issue_without_acr(project_dir)


# c = ContributorAgent(1, 2, "John")
# current_folder = os.path.dirname(os.path.abspath(__file__))
# project_dir = os.path.join(current_folder, "..", "..", "..", "..", "calculator_project")
# c.solve_issue_without_acr(project_dir)
