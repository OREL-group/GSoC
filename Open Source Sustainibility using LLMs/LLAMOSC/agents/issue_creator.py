# TODO : create and return Issue object
# TODO : integrate into run_llamosc, with --issues option, and (optional : continous rechecking of issues in /penmding at eevry timestep)
# TODO : Add llm-in-loop check with option to re-run
# TODO : Add human-in-the-loop check with option to re-run
# TODO : Add issue difficulty

import os

from LLAMOSC.simulation.issue import Issue
from LLAMOSC.utils import *


class IssueCreatorAgent:
    def __init__(self, name):
        self.name = name

    def create_issue(self, existing_issues, existing_code, issues_folder):
        # Create prompt for generating the issue title
        title_prompt = f"""
        You are an experienced user of this project. Your task is to create a unique and creative title for a new issue based on the provided calculator project code:
        {existing_code}
        
        Ensure that the issue is distinct from the abpve implemented existing_code and existing issues:
        {existing_issues}

        Provide a unique title for the new issue. 

        Only return the title which should be less than 10 words, dont include anything extra.
        """
        issue_title = query_ollama(prompt=title_prompt).strip()

        log_and_print(f"Generated Issue Title: {issue_title}")

        # Create prompt for generating the issue description
        description_prompt = f"""
        Using the following title as a reference: "{issue_title}", write a detailed description for this issue. Describe why this feature is needed, how it would improve the project, and any other relevant information.
        
        This is the existing code: {existing_code}

        Only return the description which should be less than 30 words.
        """
        issue_description = query_ollama(prompt=description_prompt).strip()

        log_and_print(f"Generated Issue Description: {issue_description}")

        # Create prompt for generating the example code
        example_code_prompt = f"""
        For the issue titled "{issue_title}", provide an example code snippet that demonstrates the proposed functionality or change. The code should be relevant to the description provided and show how the new feature can be implemented within the existing code {existing_code}.

        Only return the expected pseudocode changes which should be less than 100 words and startign with ```python.
        """
        example_code = query_ollama(prompt=example_code_prompt).strip()

        log_and_print(f"Generated Example Code: {example_code}")

        # Create prompt for generating the "Checked Other Resources?" section
        checked_resources_prompt = f"""
        For the issue titled "{issue_title}", write a section that confirms the user has checked other resources to ensure that this feature request is unique. Mention that no similar issues or implementations were found and that this request is an enhancement, not a bug report.

        Only return the section which should be less than 20 words.
        """
        checked_resources = query_ollama(prompt=checked_resources_prompt).strip()
        log_and_print(f"Checked Other Resources: {checked_resources}")

        # Create prompt for generating the system information
        system_info_prompt = f"""
        Provide system information that might be relevant to the issue titled "{issue_title}". Include details like the project version, Python version, and operating system.
        
        Only return the system info which should be less than 12 words.
        """
        system_info = query_ollama(prompt=system_info_prompt).strip()

        # Log the results for debugging and monitoring
        log_and_print(f"Generated System Info: {system_info}")

        # Construct the issue object
        new_issue = {
            "title": issue_title,
            "description": issue_description,
            "example_code": example_code,
            "checked_resources": checked_resources,
            "system_info": system_info,
        }

        # Create prompt for generating the system information
        final_issue_prompt = f"""
        You are an experienced user of this project, and want to help improve it with features and identifying bugs. Your task is to create new, creative, and distinct issues for a calculator project based on the provided code.
#         Here is the current state of the project:
#         {existing_code}
        Using the following data {new_issue}, write a issue in MARKDOWN ONLY that can be added to the project's issue tracker. Include the title, description, example code, checked resources, and system information in the appropriate sections.
        Here is an existing issue for reference:
        {existing_issues[0]}
        The entire issue should be less than 300 words.
        """
        final_issue = query_ollama(prompt=final_issue_prompt).strip()
        log_and_print(f"Final Issue: {final_issue}")
        # Optionally, save the issue to a file or add it to the existing issues list
        # issues_folder = "issues_folder"
        issue_filename = f"task_{len(existing_issues) + 1}.md"
        with open(os.path.join(issues_folder, issue_filename), "w") as issue_file:
            # issue_file.write(
            #     f"# {new_issue['title']}\n\n"
            #     f"Description:\n{new_issue['description']}\n\n"
            #     f"Checked Other Resources:\n{new_issue['checked_resources']}\n\n"
            #     f"Example Code:\n```python\n{new_issue['example_code']}\n```\n\n"
            #     f"System Info:\n{new_issue['system_info']}"
            # )
            issue_file.write(final_issue)
        return final_issue


def main():
    # Initialize the IssueCreatorAgent
    agent = IssueCreatorAgent(name="Issue Creator")

    # Read existing issues from the issues folder
    issues = []
    current_folder = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(
        current_folder, "..", "..", "..", "..", "calculator_project"
    )
    repo_commit_current_changes(project_dir)

    # Get the path to the issues folder
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
        # TODO: Better way to get issue difficulty maybe % 5 at least
        issue = Issue(issue_id, issue_id + 1, file_path)

        # Add the issue to the issues list
        issues.append(issue)

    log_and_print("Reading existing code from the toy_repo folder...")
    # Read existing code from the calculator project
    current_folder = os.path.dirname(__file__)
    project_dir = os.path.join(
        current_folder, "..", "..", "..", "..", "calculator_project"
    )

    existing_code = """"""

    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r") as code_file:
                    existing_code += code_file.read() + "\n"

    # Create a new issue based on the existing issues and code
    new_issue = agent.create_issue(issues, existing_code, issues_folder)
    log_and_print(f"New Issue Created: {new_issue}")


if __name__ == "__main__":
    main()
