from LLAMOSC.utils import *
from LLAMOSC.simulation.rating_and_bidding import (
    rate_contributors_for_issue,
    simulate_github_discussion,
    simulate_llm_bidding,
)
from LLAMOSC.simulation.collaborative_team import form_collaborative_team
from LLAMOSC.simulation.issue import Issue
from LLAMOSC.simulation.conversation_space import ConversationSpace
from LLAMOSC.agents.maintainer import MaintainerAgent
from LLAMOSC.agents.contributor import ContributorAgent
from langchain_community.chat_models import ChatOllama
from langchain.schema import SystemMessage, HumanMessage
import random
import logging

logger = logging.getLogger("LLAMOSC")


class Simulation:
    def __init__(self, contributors):
        self.contributors = contributors
        self.avg_code_quality = 4
        self.num_pull_requests = 0
        self.time_step = 0

        self.issues_solved = 0
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
            f"\\nEligibility Check: Contributors for Issue #{issue.id}:\\n{[(contributor.name, contributor.experience) for contributor in eligible_contributors]}\\n"
        )

        discussion_history = simulate_github_discussion(eligible_contributors, issue)

        # Log discussion messages to conversation space
        for entry in discussion_history:
            if entry["role"] != "system":
                self.conversation_space.post_message(
                    sender=entry["role"],
                    content=entry["content"]
                )

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
            f"\\nSelected Contributor for Issue #{issue.id}: {selected_contributor.name} with maintainer's rating of {max_value}\\n"
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
            f"\\nEligibility Check: Contributors for Issue #{issue.id}:\\n{[(contributor.name, contributor.experience) for contributor in eligible_contributors]}\\n"
        )

        discussion_history = simulate_github_discussion(eligible_contributors, issue)

        # Log discussion messages to conversation space
        for entry in discussion_history:
            if entry["role"] != "system":
                self.conversation_space.post_message(
                    sender=entry["role"],
                    content=entry["content"]
                )

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
            f"\\nSelected Contributor for Issue #{issue.id}: {selected_contributor.name} with a bid of {max_value}\\n"
        )

        self.conversation_space.post_message(
            sender="system",
            content=f"Issue #{issue.id} assigned to {selected_contributor.name}."
        )

        return selected_contributor, discussion_history

    def simulate_collaborative_work(self, team, issue: Issue):
        log_and_print(f"Simulating collaboration for Issue #{issue.id}...")
        ## Announce team in a channle
        for role, member in team.items():
            self.conversation_space.post_message(
                sender="system",
                content=f"Team: {role} -> {member.name}"
            )
        model = ChatOllama(model="llama3")
        issue_text = open(issue.filepath).read()
        prompt = f"""
        Simulate a brief dev conversation and work summary for:
        Issue: {issue_text}
        Team:
        - Lead: {team['Lead'].name}
        - Reviewer: {team['Reviewer'].name}
        - Support: {team['Support'].name}
        
        Output a short log (max 150 words) showing the Lead coding, Reviewer suggesting a fix, and Support helping. Do not include any timestamps or system dates in the output.
        """
        
        ctx = SystemMessage(content="You generate realistic developer collaboration logs.")
        log = model.invoke([ctx, HumanMessage(content=prompt)]).content
        
        log_and_print(f"\\n--- Collaboration Log (#{issue.id}) ---\\n{log}\\n")
        self.conversation_space.post_message(sender="system", content=f"Resolved Issue #{issue.id}. Lead preparing PR.")

        return team['Lead']

    def select_contributor_collaborative(self, issue: Issue):
        """Issue #64: 2-agent collaboration (improves PR #118)"""
        eligible = [c for c in self.contributors if c.eligible_for_issue(issue)]
        if not eligible:
            return None
        
        log_and_print(f"Eligible for #{issue.id}: {[c.name for c in eligible]}")
        
        # Step 1: Discussion (reuse existing)
        history = simulate_github_discussion(eligible, issue)
        
        # Step 2: NEW Issue #64 logic - pick lead + collaborator
        lead_agent = max(eligible, key=lambda c: c.experience)
        
        if lead_agent.should_collaborate(issue):
            collaborator = lead_agent.find_collaborator(self.contributors)
            if collaborator:
                # Split & assign subtasks
                issue.split_for_collaboration(lead_agent, collaborator)
                
                # Simulate collaborative discussion
                team = {'Lead': lead_agent, 'Support': collaborator}
                lead = self.simulate_collaborative_work(team, issue)
                
                # Issue #64: Individual subtasks + proportional credit
                for subtask in issue.subtasks:
                    agent = subtask['agent']
                    agent.handle_subtask(issue, subtask['description'])
                    agent.unassign_issue()
                    # Award proportional credit
                    credit = issue.difficulty / len(issue.subtasks)
                    agent.increase_experience(adding_exp=credit)
                
                self.conversation_space.post_message(
                    sender="system", 
                    content=f"Issue #{issue.id} resolved collaboratively by {lead_agent.name}+{collaborator.name}"
                )
                return lead_agent, history
            else:
                print(f"No collaborator for {lead_agent.name}, fallback solo")
        
        # Fallback solo (backwards compatible)
        lead_agent.assign_issue(issue)
        pr_content = lead_agent.solve_issue(project_dir="path/to/project")
        lead_agent.unassign_issue()
        lead_agent.increase_experience(adding_exp=issue.difficulty)
        return lead_agent, history

    def try_dynamic_issue_creation(self, issue_creator, issue_queue, existing_issues, existing_code, issues_folder):
        # Build simulation state dict
        simulation_state = {
            'issues_solved': self.issues_solved,
            'pending_issues': len(existing_issues),
            'avg_code_quality': self.avg_code_quality,
            'active_contributors': len([c for c in self.contributors if c.available]),
            'time_step': self.time_step
        }
        
        # Call issue creator to check if new issue should be created
        should_create = issue_creator.should_create_issue(simulation_state)
        
        if should_create:
            try:
                new_issue = issue_creator.create_issue(existing_issues, existing_code, issues_folder)
                if new_issue:
                    issue_queue.append(new_issue)
                    existing_issues.append(new_issue)
                    issue_creator.dynamic_issues_created += 1
                    issue_creator.steps_since_last_creation = 0
                    log_and_print(f"Created new dynamic issue: #{new_issue.id}")
                else:
                    logger.warning("Issue creator returned None, no new issue created")
            except Exception as e:
                logger.error(f"Error creating dynamic issue: {e}")
        else:
            # Increment steps since last creation even when not creating
            issue_creator.steps_since_last_creation += 1
