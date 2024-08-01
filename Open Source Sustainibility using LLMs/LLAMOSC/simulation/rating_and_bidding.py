from LLAMOSC.utils import *
from LLAMOSC.simulation.bid_output_parser import BidOutputParser

from langchain_community.chat_models import ChatOllama
from langchain.schema import SystemMessage, HumanMessage


# TODO : use personalization in the prompt to get dofferent bidding response for different contributors
# def generate_character_system_message(character_name, character_header):
#     return SystemMessage(
#         content=(
#             f"""{character_header}
# You will speak in the style of {character_name}, and exaggerate their personality.
# You will come up with creative ideas related to {topic}.
# Do not say the same things over and over again.
# Speak in the first person from the perspective of {character_name}
# For describing your own body movements, wrap your description in '*'.
# Do not change roles!
# Do not speak from the perspective of anyone else.
# Speak only from the perspective of {character_name}.
# Stop speaking the moment you finish speaking from your perspective.
# Never forget to keep your response to {word_limit} words!
# Do not add anything else.
#     """
#         )
#     )


def rate_contributors_for_issue(maintainer, github_discussion) -> str:

    log_and_print(
        f"Choosing Contributor for Issue #{maintainer.current_task.id} based on the discussion.\n"
    )
    bids = {}
    model = ChatOllama(model="llama3")
    bid_parser = BidOutputParser(
        regex=r"<(\d+)>", output_keys=["bid"], default_output_key="bid"
    )
    bidding_template = f"""
    {{contributor_content}}
    Based on the above comment of the contributor, on a scale of 1 to 10, where 1 is not suitable at all and 10 is extremely suitable, rate the contributor's suitability for the following issue:
    Issue #{maintainer.current_task.id}: {open(maintainer.current_task.filepath).read()}
    Difficulty: {maintainer.current_task.difficulty}

    The rating should be inversely proportional to the matching_level, which is the difference between {{contributor_role}} and {maintainer.current_task.difficulty}. If the matching_level is low, bud high. If the matching_level is high, bid very low.     

    {bid_parser.get_format_instructions()}
    Do nothing else.
    """

    for entry in github_discussion:
        if entry["role"] == "system":
            continue
        contributor_role = entry["role"]
        contributor_content = entry["content"]
        bid_message = bidding_template.format(
            contributor_content=contributor_content,
            contributor_role=contributor_role,
        )
        system_message = SystemMessage(
            content=f"You are a maintainer in an open-source community rating the ability of different contributors to contribute to the issue based on their comments on it."
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

    log_and_print(f"\nRatings for Issue #{maintainer.current_task.id}: {bids}\n")
    return bids


def format_discussion_history(discussion_history):
    formatted_history = "\nDiscussion History:\n"
    for entry in discussion_history:
        role = entry["role"]
        if role == "system":
            continue  # skip system messages
        content = entry["content"]
        formatted_history += f"{role}:\n{content}\n\n"
    return formatted_history


def simulate_github_discussion(eligible_contributors, issue):
    log_and_print(f"\nStarting GitHub-style discussion for Issue #{issue.id}.\n")
    model = ChatOllama(model="llama3")
    discussion_history = []
    issue_description = open(issue.filepath).read()
    initial_prompt = f"""
    Issue #{issue.id}: {issue_description}
    Difficulty: {issue.difficulty}
    """
    discussion_history.append({"role": "system", "content": initial_prompt})
    contributor_discussion_template = f"""
    {{discussion_history}}
    Based on the above discussion, please reply with your thoughts on the issue in the style of {{contributor_name}} in 50 words or less, that addresses an approach to solve the issue, provides a unique perspective, and also helps prove your suitability/desire to participate in solving the following issue.
    Issue #{issue.id}: {issue_description}
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
            content=f"You are {contributor.name}, a contributor in open source with experience {contributor.experience} discussing an issue."
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
    issue_description = open(issue.filepath).read()
    bidding_template = f"""
    {{discussion_history}}
    Based on the above discussion, where your comment is {{contributor_content}}, on a scale of 1 to 10, where 1 is not suitable at all and 10 is extremely suitable, rate your suitability compared to all the others for the following issue:
    Issue #{issue.id}: {issue_description}
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
