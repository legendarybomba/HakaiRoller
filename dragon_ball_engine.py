import random

# Global Configuration
DRAGON_BALL_MAX = 7
XP_PER_LEVEL = 100

def calculate_dragon_ball_drop(difficulty, current_balls):
    if current_balls >= DRAGON_BALL_MAX:
        return False
    drop_chances = {"easy": 0.08, "medium": 0.18, "hard": 0.35}
    roll = random.random()
    return roll < drop_chances.get(difficulty.lower(), 0.05)

def trigger_divine_veto(profile_data):
    profile_data["active_contract"] = None
    profile_data["active_contract_stack"] = []
    return "Shenron's Divine Veto activated! Current board state completely vaporized with zero penalty."

def roll_random_passive():
    passives = [
        {"name": "The Eternal Dragon’s Grace", "effect": "Double XP tracking enabled for the next 3 contracts."},
        {"name": "Super Dragon Radar", "effect": "Drop rates increased by 15% for 24 hours."},
        {"name": "Destroyer's Truce", "effect": "Sudden Death Overtime penalty suppressed."}
    ]
    return random.choice(passives)

def execute_shenron_wish(wish_id, profile_data):
    wish_id = wish_id.strip()
    if wish_id == "1":
        profile_data["senzu_beans"] = 3
        return "Your compliance is granted. Your Senzu Bean inventory has been restored to 3!"
    elif wish_id == "2":
        profile_data["veto_cooldown_active"] = False
        return "Your compliance is granted. The Veto matrix is completely unsealed!"
    elif wish_id == "3":
        levels_granted = random.randint(2, 10)
        profile_data["gamer_rank"] = profile_data.get("gamer_rank", 1) + levels_granted
        return f"Your compliance is granted! +{levels_granted} Ranks instantly!"
    else:
        return "The Dragon glares. Choose a valid wish."

def summon_shenron(profile_data, selected_wish_id):
    current_balls = profile_data.get("dragon_balls", 0)
    if current_balls < DRAGON_BALL_MAX:
        return {"success": False, "message": f"The sky remains clear. You only have {current_balls}/{DRAGON_BALL_MAX} Dragon Balls."}
        
    telemetry_log = []
    profile_data["can_summon_shenron"] = True
    telemetry_log.append("[ANIMATION_TRIGGER] Shenron opacity fade-in sequence started.")
    
    veto_msg = trigger_divine_veto(profile_data)
    telemetry_log.append(veto_msg)
    
    cosmic_passive = roll_random_passive()
    profile_data["active_passive_buff"] = cosmic_passive["name"]
    telemetry_log.append(f"Cosmic Blessing Rolled: {cosmic_passive['name']} ({cosmic_passive['effect']})")
    
    wish_outcome = execute_shenron_wish(selected_wish_id, profile_data)
    telemetry_log.append(wish_outcome)
    
    profile_data["dragon_balls"] = 0
    profile_data["can_summon_shenron"] = False
    
    telemetry_log.append('\n"I HAVE GRANTED YOUR WISH. FAREWELL."')
    telemetry_log.append("[ANIMATION_TRIGGER] 7 Dragon Balls scatter in random directions.")
    
    return {"success": True, "log": telemetry_log, "updated_profile": profile_data}


# =====================================================================
# THE TEST HARNESS (Attached perfectly right here at the bottom!)
# =====================================================================
if __name__ == "__main__":
    print("--- STARTING HOLD TEST SIMULATION ---")
    
    # Setup mock user who already has 6 balls and a nasty objective
    mock_profile = {
        "gamer_rank": 22,
        "dragon_balls": 6,
        "active_contract": "Farm Bottled Water in The Division 2 (OracleFish is trolling)"
    }
    
    print(f"Starting Inventory: {mock_profile['dragon_balls']}/7 Dragon Balls.")
    print(f"Current Headache: {mock_profile['active_contract']}")
    
    # 1. Simulate finding the 7th ball
    print("\n[Action] Simulating contract completion... Found the 7th Dragon Ball!")
    mock_profile["dragon_balls"] = 7
    print(f"Inventory status: {mock_profile['dragon_balls']}/7. (Holding safely!)")
    
    # 2. Trigger the manual hold execution
    print("\n[Action] Slamming the emergency button! Summoning Shenron manually and picking Wish #3 (Level Boost)...")
    print("-" * 50)
    
    result = summon_shenron(mock_profile, "3")
    
    # 3. Print the output results
    for line in result["log"]:
        print(line)
        
    print("-" * 50)
    print("--- FINAL PROFILE STATE AFTER SYSTEM RESET ---")
    print(f"Active Contract: {mock_profile['active_contract']} (Clean slate!)")
    print(f"New Rank: {mock_profile['gamer_rank']}")
    print(f"Dragon Balls Reset To: {mock_profile['dragon_balls']}/7")