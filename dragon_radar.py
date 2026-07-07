import random

DRAGON_BALL_MAX = 7
ALL_STARS = ["1-Star", "2-Star", "3-Star", "4-Star", "5-Star", "6-Star", "7-Star"]

def calculate_dragon_ball_drop(difficulty, profile_data):
    """Rolls for a drop and returns the star name if found, else None."""
    if "dragon_balls" not in profile_data:
        profile_data["dragon_balls"] = []
        
    current_balls = profile_data["dragon_balls"]
    if len(current_balls) >= DRAGON_BALL_MAX:
        return None
        
    # 🟢 Recalibrated to match the Trinity Core's explicit layout tiers:
    drop_chances = {
        "relaxed": 0.08, 
        "heated": 0.18, 
        "overwhelming": 0.35
    }
    
    roll = random.random()
    
    # Safely match lowercase difficulty strings
    if roll < drop_chances.get(difficulty.lower(), 0.05):
        remaining_stars = [s for s in ALL_STARS if s not in current_balls]
        if not remaining_stars:
            return None
        
        new_star = random.choice(remaining_stars)
        profile_data["dragon_balls"].append(new_star)
        return new_star
    return None

def summon_shenron(profile_data, selected_wish_id):
    if len(profile_data.get("dragon_balls", [])) < DRAGON_BALL_MAX:
        return {"success": False, "message": "The sky remains clear."}
    
    # Wish logic and reset
    profile_data["dragon_balls"] = []
    # ... (other wish logic)
    return {"success": True}
