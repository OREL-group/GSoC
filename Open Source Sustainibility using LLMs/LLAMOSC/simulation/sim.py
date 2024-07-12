from LLAMOSC.utils import *
from LLAMOSC.simulation.rating_and_bidding import rate_contributors_for_issue
from LLAMOSC.simulation.rating_and_bidding import simulate_github_discussion

import random


class Simulation:
    def __init__(self, contributors):
        self.contributors = contributors
        self.time_step = 0

    def select_contributor(self, maintainer):
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
        bids = rate_contributors_for_issue(maintainer, discussion_history)

        max_value = max(bids.values())
        highest_bidder_ids = [
            bid_id for bid_id, bid in bids.items() if bid == max_value
        ]
        highest_bidder_id = int(random.choice(highest_bidder_ids))
        # log_and_print(f"Highest Bidder ID: {highest_bidder_id}")
        selected_contributor = [
            contributor
            for contributor in self.contributors
            if contributor.id == highest_bidder_id
        ][0]

        log_and_print(
            f"\nSelected Contributor for Issue #{issue.id}: {selected_contributor.name} with maintainer's rating of {max_value}\n"
        )
        return selected_contributor
