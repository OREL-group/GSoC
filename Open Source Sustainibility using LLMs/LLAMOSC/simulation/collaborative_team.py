from LLAMOSC.utils import log_and_print
from LLAMOSC.simulation.rating_and_bidding import simulate_llm_bidding

def form_collaborative_team(eligible_contributors, issue, discussion_history):
    """
    Forms a collaborative team by assigning Lead, Reviewer, and Support roles.
    """
    log_and_print(f"Forming collaborative team for Issue #{issue.id}...")
    
    ## getting contributar to help rank sutibalilty
    bids = simulate_llm_bidding(eligible_contributors, issue, discussion_history)
    ## ranking contributar by merit = bid score+experience
    ranked = sorted(
        eligible_contributors, 
        key=lambda c: (bids.get(str(c.id), 0) + c.experience), 
        reverse=True
    )
    ## assign role on the basis of merit
    if len(ranked) >= 3:
        team = {
            "Lead": ranked[0],
            "Reviewer": ranked[1],
            "Support": ranked[-1] 
        }
    else:
        ## fallback for small pools
        team = {
            "Lead": ranked[0],
            "Reviewer": ranked[min(1, len(ranked)-1)],
            "Support": ranked[-1]
        }

    log_and_print(f"Team: Lead={team['Lead'].name}, Reviewer={team['Reviewer'].name}, Support={team['Support'].name}")
    return team
