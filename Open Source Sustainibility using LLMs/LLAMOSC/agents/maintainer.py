import os
import random
import logging
import re

from LLAMOSC.utils import *
from LLAMOSC.simulation.bid_output_parser import BidOutputParser, QualityRatingParser

from langchain_community.chat_models import ChatOllama
from langchain.schema import SystemMessage, HumanMessage

logger = logging.getLogger("LLAMOSC")

DEFAULT_REVIEW = (
    "The pull request has been reviewed. The implementation is functional "
    "and meets the basic requirements. No critical issues were identified. "
    "[Note: Auto-generated fallback review due to LLM unavailability]"
)

DEFAULT_QUALITY_RATING = 3


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
        diff_files = [f for f in os.listdir(pull_request_dir) if f.endswith(".diff")]
        if not diff_files:
            log_and_print(f"No .diff file found in {pull_request_dir}, skipping review.")
            return False
        diff_file_path = os.path.join(pull_request_dir, diff_files[0])

        with open(pr_file_path, "r") as pr_file:
            pr_content = pr_file.read()

        # Extract issue ID from pull request directory name
        issue_id = pull_request_dir.split("_")[-2] if "_" in pull_request_dir else "unknown"

        # Query OLLAMA to review the pull request content
        try:
            prompt_code_review = f"""As a maintainer in an open source environment, your role is to 
            review pull requests of the code submitted by contributors. 
            Please provide a brief review of the code quality in the pull request {pr_content}."""
            review_result = query_ollama(prompt=prompt_code_review)
            
            if review_result is None:
                logger.warning(f"[Maintainer {self.id}] LLM unavailable for PR review on Issue #{issue_id}. Using default review.")
                review_result = DEFAULT_REVIEW
                
            log_and_print(f"Raw code quality review result: {review_result}")

            prompt = f"""As an org admin with repository rights. it is your job to decide which pull 
            requests should be merged.
            Based on the following review of a pull request by a repository maintainer : {review_result},
            decide where the merge the merge should be approved or rejected. 
            Only give a 1 word response with 'approve' or 'reject'."""

            org_admin_result = query_ollama(prompt=prompt)
            
            if org_admin_result is None:
                logger.warning(f"[Maintainer {self.id}] LLM unavailable for approval decision on Issue #{issue_id}. Defaulting to approve.")
                org_admin_result = "approve"

        except Exception as e:
            logger.error(f"[Maintainer {self.id}] Error during PR review on Issue #{issue_id}: {e}")
            review_result = DEFAULT_REVIEW
            org_admin_result = "approve"

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
        try:
            # Case 1 - Empty input
            if review_result is None or not review_result.strip():
                logger.warning(f"[Maintainer {self.id}] Empty review text. Using default rating.")
                return DEFAULT_QUALITY_RATING
            
            review_text = review_result.strip()
            
            # Case 2 - Valid 1-5 rating found
            valid_match = re.search(r'\b([1-5])\b', review_text)
            if valid_match:
                rating = int(valid_match.group(1))
                return max(1, min(5, rating))
            
            # Case 3 - Out-of-range number found
            number_match = re.search(r'\b(\d+)\b', review_text)
            if number_match:
                raw = int(number_match.group(1))
                if raw > 5:
                    scaled = round(raw / 2)
                    scaled = max(1, min(5, scaled))
                    logger.warning(f"[Maintainer {self.id}] Out-of-range rating {raw} detected. Scaled to {scaled}.")
                    return scaled
            
            # Case 4 - No number found at all
            logger.warning(f"[Maintainer {self.id}] Could not parse rating. Using default.")
            return DEFAULT_QUALITY_RATING
            
        except Exception as e:
            # Case 5 - Unexpected exception
            logger.error(f"[Maintainer {self.id}] Error parsing rating: {e}")
            return random.randint(1, 5)
