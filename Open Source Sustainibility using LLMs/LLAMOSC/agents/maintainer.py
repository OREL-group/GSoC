import os
import random

from LLAMOSC.utils import *
from LLAMOSC.simulation.bid_output_parser import BidOutputParser, QualityRatingParser

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
        prompt_code_review = f"""As a maintainer in an open source environment, your role is to 
        review pull requests of the code submitted by contributors. 
        Please provide a brief review of the code quality in the pull request {pr_content}."""
        review_result = query_ollama(prompt=prompt_code_review)
        log_and_print(f"Raw code quality review result: {review_result}")

        prompt = f"""As an org admin with repository rights. it is your job to decide which pull 
        requests should be merged.
        Based on the following review of a pull request by a repository maintainer : {review_result},
        decide where the merge the merge should be approved or rejected. 
        Only give a 1 word response with 'approve' or 'reject'."""

        org_admin_result = query_ollama(prompt=prompt)

        if "approve" in org_admin_result.lower():
            code_quality = self.rate_code_quality(review_result)
            # Apply the diff to the local repository
            repo_apply_diff_and_commit(local_repo_dir, diff_file_path)
            # commit the changes made i.e applying the diff
            self.unassign_task()
            return code_quality
        else:
            self.unassign_task()
            return False

    def rate_code_quality(self, review_result):
        # Define the quality rating parser
        quality_parser = QualityRatingParser(
            regex=r"<(\d)>", output_keys=["rating"], default_output_key="rating"
        )

        # Query OLLAMA to rate the code quality
        prompt_code_quality = f"""On a scale of 1 to 5, where 1 is very poor and 5 is excellent,
        provide a quality rating for the code based on the review {review_result}.
        The rating should be unique and very reflective of the quality of the code,
        and how the given code solves the issue.
        {quality_parser.get_format_instructions()}"""

        review_result = query_ollama(prompt=prompt_code_quality)
        log_and_print(f"Code quality rating result: {review_result}")

        # Parse the review result to get the rating
        parsed_result = quality_parser.parse(review_result)

        # Extract the rating
        rating = parsed_result.get(
            "rating", random.randint(1, 5)
        )  # Default to random if parsing fails

        log_and_print(f"Parsed code quality rating: {rating}")
        if type(rating) != int:
            rating = random.randrange(2, 5)

        return rating
