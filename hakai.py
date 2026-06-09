import collections
import datetime
import getpass  # Added for hidden input tracking!
import os
import random
import sys
import time

# --- CONFIG & CONTROLS ---
TESTING_MODE = True  # Set to False to log your official lifetime stream records!
GAME_POOL = [
    "Fallout 76", "The Division 2", "The First Descendant", "Helldivers 2",
    "Titanfall 2", "Doom Eternal", "Soulcalibur 6", "DB Xenoverse 2",
    "Gears 5", "Rainbow Six Vegas 2"
]
COOP_GAMES = ["Fallout 76", "The Division 2", "The First Descendant", "Helldivers 2", "Gears 5", "Rainbow Six Vegas 2"]
HISTORY_FILE = "game_history.txt"
ACHIEVEMENTS_FILE = "achievements.txt"  
COMPLETED_FILE = "completed_achievements.txt"  
ACHIEVEMENT_FILE = "gamer_profile.txt"
SHORT_TERM_COOL_DOWN = 3

def load_objectives():
    objectives_db = {game: {"Easy": [], "Hard": []} for game in GAME_POOL}
    completed_pool = set()
    if os.path.exists(COMPLETED_FILE):
        with open(COMPLETED_FILE, "r") as f:
            completed_pool = {line.strip() for line in f if line.strip()}

    if not os.path.exists(ACHIEVEMENTS_FILE):
        return objectives_db
        
    current_game = None
    with open(ACHIEVEMENTS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            if line.startswith("[") and line.endswith("]"):
                game_name = line[1:-1]
                current_game = game_name if game_name in GAME_POOL else None
            elif current_game and "|" in line:
                diff, challenge = line.split("|", 1)
                diff = diff.strip()
                challenge = challenge.strip()
                if diff in ["Easy", "Hard"] and challenge not in completed_pool:
                    objectives_db[current_game][diff].append(challenge)
    return objectives_db

WILDCARDS_DB = load_objectives()

# --- INITIAL DATA LOAD ---
if TESTING_MODE:
    print("🧪 --- TESTING MODE ACTIVE: Using Simulated History Data --- 🧪")
    all_history = ["The Division 2", "Helldivers 2", "Titanfall 2"]
else:
    if not os.path.exists(HISTORY_FILE): open(HISTORY_FILE, "w").close()
    with open(HISTORY_FILE, "r") as f:
        all_history = [line.strip() for line in f if line.strip() in GAME_POOL]

recent_blocks = all_history[-SHORT_TERM_COOL_DOWN:] if all_history else []

gamer_score = 0
if os.path.exists(ACHIEVEMENT_FILE):
    with open(ACHIEVEMENT_FILE, "r") as f:
        for line in f:
            if line.startswith("TOTAL_GAMER_SCORE:"):
                gamer_score = int(line.split(":")[1].strip())

# --- MENU ROUTER ---
print("--- Session Parameters ---")
print("[1] Solo Night (Full Library)")
print("[2] Co-Op Night (Squad Only)")
print("[3] Double Feature (Warmup + Main Event)")

while True:
    session_choice = input("Select parameters (1, 2, or 3): ").strip()
    if session_choice in ["1", "2", "3"]:
        break
    print("⚠️  Invalid parameters. Please type 1, 2, or 3.")

if session_choice == "2":
    available_games = [g for g in GAME_POOL if g in COOP_GAMES]
else:
    available_games = GAME_POOL[:]

available_games = [g for g in available_games if g not in recent_blocks] or GAME_POOL[:]

is_double_feature = (session_choice == "3")
rolls_queue = []

if is_double_feature:
    rolls_queue.extend([("Easy", "🟢 ACT I: WARMUP"), ("Hard", "🔴 ACT II: MAIN EVENT")])
else:
    print("\n--- Intensity Matrix ---")
    print("[1] Chill Session (Easy Objectives)")
    print("[2] Sweat Session (Hard Objectives)")
    while True:
        intensity_choice = input("Select difficulty (1 or 2): ").strip()
        if intensity_choice in ["1", "2"]:
            break
        print("⚠️  Invalid intensity selection. Type 1 or 2.")
    single_diff = "Hard" if intensity_choice == "2" else "Easy"
    rolls_queue.append((single_diff, "🎮 SINGLE FEATURE"))

# --- PHASE 1: SPIN & STACK ENGINE ---
current_day = datetime.datetime.now().weekday()
counts = collections.Counter(all_history)
max_plays = max(counts.values()) if counts else 0

selected_session_games = []
game_difficulties = {}
game_stacked_objectives = {}

while rolls_queue:
    target_difficulty, act_title = rolls_queue.pop(0)
    weights = []
    
    for game in available_games:
        if game in selected_session_games:
            weights.append(0)
            continue
            
        base_weight = (max_plays - counts[game]) + 1
        multiplier = 1.0
        if current_day == 1 and game in ["Fallout 76", "The Division 2"]: multiplier *= 3.0
        elif current_day == 3 and game == "The First Descendant": multiplier *= 3.0
        
        recent_streak = all_history[-5:].count(game) if all_history else 0
        if recent_streak >= 2: multiplier *= (0.5 if recent_streak == 2 else 0.2)
        weights.append(base_weight * multiplier)

    print(f"\n{act_title}")
    print("---------------------------------")
    for delay in [0.05]*8 + [0.1]*4 + [0.2]*2 + [0.5]:
        sys.stdout.write(f"\r🎲 Spin: {random.choice(available_games)[:15].ljust(15)}")
        sys.stdout.flush()
        time.sleep(delay)

    sys.stdout.write("\r" + " " * 30 + "\r")
    sys.stdout.flush()

    winner = random.choices(available_games, weights=weights, k=1)[0]
    selected_session_games.append(winner)
    game_difficulties[winner] = target_difficulty
    
    print(f"Target Locked: {winner.upper()}")
    pool_options = WILDCARDS_DB[winner][target_difficulty]
    
    active_deck = []
    if pool_options:
        active_deck.append(random.choice(pool_options))
    else:
        active_deck.append("Sandbox Freeplay Night")
        
    print(f"🎯 Objective 1: {active_deck[0]}")
    
    while len(active_deck) < 3 and pool_options:
        valid_choices = [o for o in pool_options if o not in active_deck]
        if not valid_choices: break
        
        while True:
            stack_choice = input(f"🔥 Feel like stacking? Add another [{target_difficulty}] objective to this run? (y/n): ").strip().lower()
            if stack_choice in ['y', 'n']:
                break
            print("⚠️  Response blocked. Enter 'y' for Yes or 'n' for No.")
            
        if stack_choice == 'y':
            fresh_obj = random.choice(valid_choices)
            active_deck.append(fresh_obj)
            print(f"⚡ Objective {len(active_deck)} Stacked: {fresh_obj}")
        else:
            break
            
    game_stacked_objectives[winner] = active_deck
    print("---------------------------------")

    if not rolls_queue and len(selected_session_games) < len(available_games):
        print("\n=================================")
        while True:
            overtime = input("Press [Enter] to lock itinerary, or type [+] for an extra game: ").strip()
            if overtime in ["", "+"]:
                break
            print("⚠️  Command unrecognized. Press [Enter] to lock or type [+] to add a game.")
            
        if overtime == "+":
            next_act_num = len(selected_session_games) + 1
            bonus_diff = random.choice(["Easy", "Hard"])
            rolls_queue.append((bonus_diff, f"✨ ACT {next_act_num}: THE ENCORE ({bonus_diff})"))

# --- PHASE 2: GO PLAY / DEBRIEF AFTER-ACTION REPORT ---
print("\n🎮 ITINERARY LOCKED. GO STREAM / PLAY YOUR SESSIONS! 🎮")

# 👻 THE GHOST INPUT GATE: Completely invisible key verification 
while True:
    gate_check = getpass.getpass(prompt="Press [Enter] when you have finished gaming to open the After-Action Report...").strip()
    if gate_check == "":
        break
    print("⚠️  Input detected. Please press ONLY the Enter key to continue.")

print("\n🏆 DEBRIEFING: AFTER-ACTION REPORT 🏆")
print("---------------------------------")
new_points = 0
cleared_this_session = []

for game in selected_session_games:
    print(f"\n⚔️  REVIEWING DEPLOYMENT FOR {game.upper()}:")
    deck = game_stacked_objectives[game]
    
    for idx, obj in enumerate(deck, 1):
        if obj == "Sandbox Freeplay Night": continue
            
        while True:
            check = input(f"   👉 Did you clear Objective {idx}? [{obj}] (y/n): ").strip().lower()
            if check in ['y', 'n']:
                break
            print("      ⚠️  Invalid entry. Please respond with exactly 'y' or 'n'.")
            
        if check == 'y':
            new_points += 10
            cleared_this_session.append(obj)  
            print("      ✨ Clear! +10G Added.")
        else:
            print("      💤 Logged. No points assigned for this card.")

# --- FINAL SCORE & METRICS LAYER SAVE ---
print("\n=================================")
if new_points > 0:
    gamer_score += new_points
    if not TESTING_MODE:
        with open(ACHIEVEMENT_FILE, "w") as f:
            f.write(f"TOTAL_GAMER_SCORE: {gamer_score}\n")
            f.write(f"LAST_UPDATED: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
        with open(COMPLETED_FILE, "a") as f:
            for accomplished_card in cleared_this_session:
                f.write(f"{accomplished_card}\n")
                
        print(f"🎉 PROFILE UPDATED! You earned {new_points}G tonight.")
        print(f"👑 Current Total Gamer Score: {gamer_score}G")
        print(f"🗂️  Conquered cards logged to {COMPLETED_FILE} and retired from pool!")
    else:
        print(f"🧪 SIMULATION: You earned {new_points}G during this test.")
        print(f"🧪 Simulated Total: {gamer_score}G (No files altered)")
        print(f"🧪 Simulated Retirement: {len(cleared_this_session)} cards would have been locked away.")
else:
    print(f"🎮 Session concluded. Standing Total Gamer Score: {gamer_score}G")
print("=================================")

if not TESTING_MODE:
    all_history.extend(selected_session_games)
    with open(HISTORY_FILE, "w") as f:
        for game in all_history: f.write(f"{game}\n")
