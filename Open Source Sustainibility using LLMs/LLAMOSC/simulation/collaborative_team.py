from LLAMOSC.utils import log_and_print
from LLAMOSC.simulation.rating_and_bidding import simulate_llm_bidding

def form_collaborative_team(eligible_contributors, issue, discussion_history):
    """
    Forms a collaborative team by assigning Lead, Reviewer, and Support roles.
    Uses a merit-based approach (Bid Score + Experience) for reliability and speed.
    """
    log_and_print(f"Forming collaborative team for Issue #{issue.id}...")
    
    # Get contributor bids to help rank suitability
    bids = simulate_llm_bidding(eligible_contributors, issue, discussion_history)
    
    # Rank contributors by Merit = Bid Score + Experience
    ranked = sorted(
        eligible_contributors, 
        key=lambda c: (bids.get(str(c.id), 0) + c.experience), 
        reverse=True
    )
    
    # Assign roles based on merit ranking
    if len(ranked) >= 3:
        team = {
            "Lead": ranked[0],
            "Reviewer": ranked[1],
            "Support": ranked[-1] # Support can be the person with lowest merit or lowest exp
        }
    else:
        # Fallback for small pools: reuse members or pick best available
        team = {
            "Lead": ranked[0],
            "Reviewer": ranked[min(1, len(ranked)-1)],
            "Support": ranked[-1]
        }

    log_and_print(f"Team: Lead={team['Lead'].name}, Reviewer={team['Reviewer'].name}, Support={team['Support'].name}")
    return team
