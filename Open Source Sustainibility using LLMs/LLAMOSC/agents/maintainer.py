import os

from LLAMOSC.utils import *
from LLAMOSC.simulation.bid_output_parser import BidOutputParser

from langchain_community.chat_models import ChatOllama
from langchain.schema import SystemMessage, HumanMessage


class MaintainerAgent:
    def __init__(self, id, experience, name):
        self.id = id
        self.experience = experience
        self.available = True
        self.current_task = None
        self.name = name

    def eligible_for_issue(self, issue):
        return self.available and self.experience >= issue.difficulty

    def allot_task(self, issue):
        self.current_task = issue
        self.available = False
        log_and_print(f"Maintainer {self.name} has been allotted Issue #{issue.id}.\n")
        return self.current_task

    def unassign_task(self):
        self.current_task = None
        self.available = True

    def review_pull_request(self, pull_request_dir, local_repo_dir):
        pr_file_path = os.path.join(pull_request_dir, "pr.md")
        diff_file_path = os.path.join(
            pull_request_dir,
            [f for f in os.listdir(pull_request_dir) if f.endswith(".diff")][0],
        )

        with open(pr_file_path, "r") as pr_file:
            pr_content = pr_file.read()

        # Query OLLAMA to review the pull request content
        prompt = f"""As a maintainer in an open source environment, your role is to 
        review pull requests submitted by contributors. 
        Here is a pull request description:\n{pr_content}\n
        Based on the description, should this pull request be accepted, i.e does it accurately solve the given issue? 
        Please provide a brief review. Only respond with 'approve' or 'reject'."""

        review_result = query_ollama(prompt=prompt)
        log_and_print(f"Review result: {review_result}")

        if "approve" in review_result.lower():
            code_quality = self.rate_code_quality(pr_content)
            # Apply the diff to the local repository
            repo_apply_diff_and_commit(local_repo_dir, diff_file_path)
            # commit the changes made i.e applying the diff
            self.unassign_task()
            return code_quality
        else:
            self.unassign_task()
            return False

    def rate_code_quality(self, pull_request_content):
        # Query OLLAMA to rate the code quality
        prompt = f"""As a maintainer in an open source environment, your role is to 
        review the code quality of the code submitted by contributors. 
        Please provide a brief review of the code quality in the pull_request {pull_request_content}."""

        review_result = query_ollama(prompt=prompt)
        log_and_print(f"Code quality review result: {review_result}")
        return review_result
