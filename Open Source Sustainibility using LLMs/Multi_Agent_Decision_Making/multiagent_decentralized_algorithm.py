from langchain_community.chat_models import ChatOllama
from langchain.schema import SystemMessage, HumanMessage
from langchain.output_parsers import RegexParser
import random
import numpy as np
import os
from utils import log_and_print


class Issue:
    def __init__(self, id, difficulty, description):
        self.id = id
        self.difficulty = difficulty
        self.status = "open"
        self.description = description


class Contributor:
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
        log_and_print(f"Contributor {self.name} has been allotted Issue #{issue.id}.\n")
        return self.current_task

    def solve_task(self):
        # Empty implementation for now, will integrate with earlier code from Environment_Creation later
        log_and_print(
            f"Contributor {self.name} has created pull request for Issue #{self.current_task.id}.\n"
        )
        self.current_task = None
        self.available = True
        return True


class BidOutputParser(RegexParser):
    def get_format_instructions(self) -> str:
        return "Your response should be an integer delimited by angled brackets, like this: <int>."


def format_discussion_history(discussion_history):
    formatted_history = "\nDiscussion History:\n"
    for entry in discussion_history:
        role = entry["role"]
        if role == "system":
            continue
        content = entry["content"]
        formatted_history += f"{role}:\n{content}\n\n"
    return formatted_history


def simulate_github_discussion(eligible_contributors, issue):
    log_and_print(f"\nStarting GitHub-style discussion for Issue #{issue.id}.\n")
    model = ChatOllama(model="llama3")
    discussion_history = []

    initial_prompt = f"""
    Issue #{issue.id}: {issue.description}
    Difficulty: {issue.difficulty}
    """
    discussion_history.append({"role": "system", "content": initial_prompt})
    contributor_discussion_template = f"""
    {{discussion_history}}
    Based on the above discussion, please reply with your thoughts on the issue in the style of {{contributor_name}} in 50 words or less, that addresses an approach to solve the issue, provides a unique perspective, and also helps prove your suitability/desire to participate in solving the following issue.
    Issue #{issue.id}: {issue.description}
    Difficulty: {issue.difficulty}
    """

    for contributor in eligible_contributors:

        contributor_discussion_prompt = contributor_discussion_template.format(
            discussion_history="\n".join(
                f"{entry['role']}: {entry['content']}" for entry in discussion_history
            ),
            contributor_name=contributor.name,
            contributor_experience=contributor.experience,
        )
        system_message = SystemMessage(
            content=f"You are {contributor.name}, a contributor in open source with experience of {contributor.experience} years discussing an issue."
        )
        response = model.invoke(
            [
                system_message,
                HumanMessage(content=contributor_discussion_prompt),
            ]
        ).content
        discussion_history.append(
            {
                "role": f"{contributor.name} (id : {contributor.id}) (Experience: {contributor.experience}):",
                "content": response,
            }
        )

    formatted_history = format_discussion_history(discussion_history)
    log_and_print(formatted_history)
    return discussion_history


def simulate_llm_bidding(eligible_contributors, issue, discussion_history):
    log_and_print(f"Starting bidding for Issue #{issue.id} based on the discussion.\n")
    model = ChatOllama(model="llama3")
    bid_parser = BidOutputParser(
        regex=r"<(\d+)>", output_keys=["bid"], default_output_key="bid"
    )
    bidding_template = f"""
    {{discussion_history}}
    Based on the above discussion, where your comment is {{contributor_content}}, on a scale of 1 to 10, where 1 is not suitable at all and 10 is extremely suitable, rate your suitability compared to all the others for the following issue:
    Issue #{issue.id}: {issue.description}
    Difficulty: {issue.difficulty}

    The bid should be inversely proportional to the matching_level, which is the difference between {{contributor_role}} and {issue.difficulty}. If the matching_level is low, bud high. If the matching_level is high, bid very low.     

    {bid_parser.get_format_instructions()}
    Do nothing else.
    """

    bids = {}

    for entry in discussion_history:
        if entry["role"] == "system":
            continue
        contributor_role = entry["role"]
        contributor_content = entry["content"]
        bid_message = bidding_template.format(
            discussion_history="\n".join(
                f"{entry['role']}: {entry['content']}" for entry in discussion_history
            ),
            contributor_content=contributor_content,
            contributor_role=contributor_role,
        )
        system_message = SystemMessage(
            content=f"You are contributor {contributor_role} bidding on an issue s to contribute to it in an open-source community based on yopur comments in the github_discussion on it."
        )
        response = model.invoke(
            [
                system_message,
                HumanMessage(content=bid_message),
            ]
        ).content
        bid_value = int(bid_parser.parse(response)["bid"])
        contributor_id = (
            contributor_role.split(":")[1].strip().split(" ")[0].strip("()")
        )
        bids[contributor_id] = bid_value

    log_and_print(f"\nBids for Issue #{issue.id}: {bids}\n")
    return bids


class Simulation:
    def __init__(self, contributors):
        self.contributors = contributors
        self.time_step = 0

    def select_contributor(self, issue):
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

        # randomly select among multiple agents with the same bid

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
        return selected_contributor


# Implementations of the classes and functions are done. Now, we will run the simulation.

issues = [
    Issue(0, 2, open(os.path.join(os.path.dirname(__file__), "task_1.md")).read()),
    Issue(1, 4, open(os.path.join(os.path.dirname(__file__), "task_2.md")).read()),
]

contributors = [
    Contributor(i, random.randint(1, 5), f"Contributor_{i}") for i in range(5)
]

sim = Simulation(contributors)
time = 0

log_and_print(
    f"\nStarting simulation with {len(issues)} issues and {len(contributors)} contributors.\n"
)

# since going through issues linearly, not adding a while loop and deleting solved issues for now.
for issue in issues:
    log_and_print(f"\nTime Step: {time}\n")

    log_and_print(f"\nIssue #{issue.id}: {issue.description}\n")
    selected_contributor = sim.select_contributor(issue)
    if selected_contributor:
        selected_contributor.allot_task(issue)
        task_solved = selected_contributor.solve_task()
        if task_solved:
            log_and_print(
                f"Maintainer has merged pull request for Issue #{issue.id}.\n"
            )
        time += 1
    else:
        selected_contributor = [
            Contributor
            for contributor in contributors
            if contributor.eligible_for_issue(issue)
        ][0]
        time += 1
