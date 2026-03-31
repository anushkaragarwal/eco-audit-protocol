def calculate_true_esg(base_score, events):
    penalty = 0
    
    for event in events:
        reason = event.get("reason", "").lower()
        
        if "environment" in reason:
            penalty += 10
        elif "legal" in reason:
            penalty += 7
        elif "green" in reason:
            penalty -= 5  # good news bonus
    
    final_score = base_score - penalty
    
    # limits
    if final_score > 100:
        final_score = 100
    if final_score < 0:
        final_score = 0
        
    return final_score
def get_risk_level(score):
    if score >= 80:
        return "LOW"
    elif score >= 60:
        return "MEDIUM"
    else:
        return "HIGH"