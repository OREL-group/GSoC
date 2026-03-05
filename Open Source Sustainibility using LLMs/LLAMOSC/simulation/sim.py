from LLAMOSC.utils import *
from LLAMOSC.simulation.rating_and_bidding import (
    rate_contributors_for_issue,
    simulate_github_discussion,
    simulate_llm_bidding,
    form_collaborative_team,
)
from LLAMOSC.simulation.issue import Issue
from LLAMOSC.simulation.conversation_space import ConversationSpace
from LLAMOSC.agents.maintainer import MaintainerAgent
from LLAMOSC.agents.contributor import ContributorAgent
import random


class Simulation:
    def __init__(self, contributors):
        self.contributors = contributors
        self.avg_code_quality = 4
        self.num_pull_requests = 0
        self.time_step = 0
        self.conversation_space = ConversationSpace(channel_name="general")

    def update_code_quality(self, new_quality):
        self.num_pull_requests += 1
        log(f"Initial code quality: {self.avg_code_quality}")
        log(f"Recieved new code quality: {new_quality}")
        if self.num_pull_requests == 1:
            self.avg_code_quality = new_quality
            log(f"Number of pull requests: {self.num_pull_requests}")
            log(f"New code quality: {self.avg_code_quality}")
        else:
            self.avg_code_quality = (
                (self.avg_code_quality * (self.num_pull_requests - 1)) + new_quality
            ) / self.num_pull_requests
            log(f"Number of pull requests: {self.num_pull_requests}")
            log(f"New code quality: {self.avg_code_quality}")

    def select_contributor_authoritarian(
        self, maintainer: MaintainerAgent
    ) -> ContributorAgent:
        issue = maintainer.current_task
        eligible_contributors = [
            contributor
            for contributor in self.contributors
            if contributor.eligible_for_issue(issue)
        ]
        if not eligible_contributors:
            return None

        log_and_print(
            f"\nEligibility Check: Contributors for Issue #{issue.id}:\n{[(contributor.name, contributor.experience) for contributor in eligible_contributors]}\n"
        )

        discussion_history = simulate_github_discussion(eligible_contributors, issue)
        bids = rate_contributors_for_issue(
            eligible_contributors, maintainer, discussion_history
        )

        max_value = max(bids.values())
        highest_bidder_ids = [
            bid_id for bid_id, bid in bids.items() if bid == max_value
        ]
        highest_bidder_id = int(random.choice(highest_bidder_ids))
        selected_contributor = [
            contributor
            for contributor in self.contributors
            if contributor.id == highest_bidder_id
        ][0]

        log_and_print(
            f"\nSelected Contributor for Issue #{issue.id}: {selected_contributor.name} with maintainer's rating of {max_value}\n"
        )

        self.conversation_space.post_message(
            sender="system",
            content=f"Issue #{issue.id} assigned to {selected_contributor.name}."
        )

        return selected_contributor, discussion_history

    def select_contributor_decentralized(self, issue: Issue):
        eligible_contributors = [
            contributor
            for contributor in self.contributors
            if contributor.eligible_for_issue(issue)
        ]
        if not eligible_contributors:
            return None

        log_and_print(
            f"\nEligibility Check: Contributors for Issue #{issue.id}:\n{[(contributor.name, contributor.experience) for contributor in eligible_contributors]}\n"
        )

        discussion_history = simulate_github_discussion(eligible_contributors, issue)
        bids = simulate_llm_bidding(eligible_contributors, issue, discussion_history)

        max_value = max(bids.values())
        highest_bidder_ids = [
            bid_id for bid_id, bid in bids.items() if bid == max_value
        ]
        highest_bidder_id = int(random.choice(highest_bidder_ids))
        selected_contributor = [
            contributor
            for contributor in self.contributors
            if contributor.id == highest_bidder_id
        ][0]

        log_and_print(
            f"\nSelected Contributor for Issue #{issue.id}: {selected_contributor.name} with a bid of {max_value}\n"
        )

        self.conversation_space.post_message(
            sender="system",
            content=f"Issue #{issue.id} assigned to {selected_contributor.name}."
        )

        return selected_contributor, discussion_history
