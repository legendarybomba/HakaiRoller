import collections
import datetime
import os
import random
import sys
import time
import textwrap

# =========================================================
# CONFIGURATION & SOURCE OF TRUTH GATES
# =========================================================
TESTING_MODE = True  # Set to False to log official records!
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

# Terminal safety width for mobile viewports
MAX_WIDTH = 32

def display_wrapped_objective(prefix, text):
    """Wraps long challenge strings cleanly to prevent edge cutting."""
    initial_indent = prefix
    subsequent_indent = " " * len(prefix)
    wrapped = textwrap.fill(text, width=MAX_WIDTH, initial_indent=initial_indent, subsequent_indent=subsequent_indent)
    print(wrapped, flush=True)

# =========================================================
# SELF-HEALING ARCHITECTURE MATRIX (REFLOW STABLE)
# =========================================================
def heal_environment():
    """Validates and restores local structure without layout reflow bugs."""
    healed_any = False
    print("🛠️  Running system diagnostic...", flush=True)
    
    # 1. Heal Profile File
    if not os.path.exists(ACHIEVEMENT_FILE):
        with open(ACHIEVEMENT_FILE, "w", encoding="utf-8") as f:
            f.write("TOTAL_GAMER_SCORE: 0\n")
            f.write(f"LAST_UPDATED: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        healed_any = True

    # 2. Heal History Log
    if not os.path.exists(HISTORY_FILE):
        open(HISTORY_FILE, "w", encoding="utf-8").close()
        healed_any = True

    # 3. Heal Completed Cards Registry
    if not os.path.exists(COMPLETED_FILE):
        open(COMPLETED_FILE, "w", encoding="utf-8").close()
        healed_any = True

    # 4. Heal Core Master Achievements Deck
    if not os.path.exists(ACHIEVEMENTS_FILE):
        with open(ACHIEVEMENTS_FILE, "w", encoding="utf-8") as f:
            f.write("# =========================================================\n")
            f.write("# HAKAI WILD CARDS DECK MATRIX\n")
            f.write("# Format: Difficulty | Challenge Description\n")
            f.write("# =========================================================\n\n")
            for game in GAME_POOL:
                f.write(f"[{game}]\n")
                f.write("Easy | Complete 1 Daily Challenge or Bounty\n")
                f.write("Hard | Clear an Endgame Mission or High-Tier Boss\n\n")
        healed_any = True

    if healed_any:
        print("✨ Diagnostic: Assets restored. [OK]\n", flush=True)
    else:
        print("✨ Diagnostic: Verified. [OK]\n", flush=True)

# Run the self-healing layout sweep before loading downstream data
heal_environment()

# =========================================================
# CORE MODULES & DATA LOAD
# =========================================================
def load_objectives():
    objectives_db = {game: {"Easy": [], "Hard": []} for game in GAME_POOL}
    completed_pool = set()
    
    with open(COMPLETED_FILE, "r", encoding="utf-8") as f:
        completed_pool = {line.strip() for line in f if line.strip()}

    current_game = None
    with open(ACHIEVEMENTS_FILE, "r", encoding="utf-8") as f:
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
    print("🧪 --- TESTING MODE ACTIVE --- 🧪", flush=True)
    print("Using Simulated History Data...\n", flush=True)
    all_history = ["The Division 2", "Helldivers 2", "Titanfall 2"]
else:
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        all_history = [line.strip() for line in f if line.strip() in GAME_POOL]

recent_blocks = all_history[-SHORT_TERM_COOL_DOWN:] if all_history else []

gamer_score = 0
with open(ACHIEVEMENT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("TOTAL_GAMER_SCORE:"):
            gamer_score = int(line.split(":")[1].strip())

# --- MENU ROUTER ---
print("--- Session Parameters ---", flush=True)
print("[1] Solo Night (Full Library)", flush=True)
print("[2] Co-Op Night (Squad Only)", flush=True)
print("[3] Double Feature (Warmup+Main)", flush=True)

while True:
    session_choice = input("\nSelect choice (1, 2, 3): ").strip()
    if session_choice in ["1", "2", "3"]:
        break
    print("⚠️  Invalid entry. Use 1, 2, or 3.", flush=True)

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
    print("\n--- Intensity Matrix ---", flush=True)
    print("[1] Chill Session (Easy)", flush=True)
    print("[2] Sweat Session (Hard)", flush=True)
    while True:
        intensity_choice = input("\nSelect difficulty (1-2): ").strip()
        if intensity_choice in ["1", "2"]:
            break
        print("⚠️  Invalid choice. Use 1 or 2.", flush=True)
    single_diff = "Hard" if intensity_choice == "2" else "Easy"
    rolls_queue.append((single_diff, "🎮 SINGLE FEATURE"))

# --- PHASE 1: SPIN & STACK ENGINE ---
current_day = datetime.datetime.now().weekday()
counts = collections.Counter(all_history)
max_plays = max(counts.values()) if counts else 0

selected_session_games = []
game_difficulties = {}
game_stacked_objectives = {}

print("\n⚙️  Initializing selection engine matrices...", flush=True)
time.sleep(0.4)

while rolls_queue:
    target_difficulty, act_title = rolls_queue.pop(0)
    weights = []
    
    for game in available_games:
        if game in selected_session_games:
            weights.append(0)
            continue
            
        base_weight = (max_plays - counts[game]) + 1
        multiplier = 1.0
        if current_day == 1 and game in ["Fallout 76", "The Division 2"]: 
            multiplier *= 3.0
        elif current_day == 3 and game == "The First Descendant": 
            multiplier *= 3.0
        
        recent_streak = all_history[-5:].count(game) if all_history else 0
        if recent_streak >= 2: 
            multiplier *= (0.5 if recent_streak == 2 else 0.2)
        weights.append(base_weight * multiplier)

    print(f"\n{act_title}", flush=True)
    print("--------------------------------", flush=True)

    winner = random.choices(available_games, weights=weights, k=1)[0]
    selected_session_games.append(winner)
    game_difficulties[winner] = target_difficulty
    
    # 🎰 STREAMLINED COMPACT REEL
    steps = [
        (0.04, "🎰 [ REEL SPIN ] >>> CALCULATING..."),
        (0.05, "🎲 [ CYCLING   ] >>> FILTERING POOL.."),
        (0.07, "✨ [ DECELERATE] >>> WEIGHING STREAKS."),
        (0.12, "⚡ [ SLOWING   ] >>> SHUFFLING DECK.."),
        (0.22, "🔍 [ SELECTING ] >>> LOCKING COORD..."),
        (0.45, "🎯 [ PLUGGING  ] >>> SEQUENCE COMPLETE")
    ]
    
    for delay, status in steps:
        print(f" {status}", flush=True)
        time.sleep(delay)

    print("--------------------------------", flush=True)
    print(f"🎯 TARGET LOCKED: {winner.upper()}\n", flush=True)
    
    pool_options = WILDCARDS_DB[winner][target_difficulty]
    active_deck = []
    if pool_options:
        active_deck.append(random.choice(pool_options))
    else:
        active_deck.append("Sandbox Freeplay Night")
        
    display_wrapped_objective("💎 Obj 1: ", active_deck[0])
    
    while len(active_deck) < 3 and pool_options:
        valid_choices = [o for o in pool_options if o not in active_deck]
        if not valid_choices: break
        
        while True:
            stack_choice = input(f"\n🔥 Stack [{target_difficulty}] card? (y/n): ").strip().lower()
            if stack_choice in ['y', 'n']:
                break
            print("⚠️  Use 'y' or 'n'.", flush=True)
            
        if stack_choice == 'y':
            fresh_obj = random.choice(valid_choices)
            active_deck.append(fresh_obj)
            display_wrapped_objective(f"⚡ Obj {len(active_deck)} Stacked: ", fresh_obj)
        else:
            break
            
    game_stacked_objectives[winner] = active_deck
    print("--------------------------------", flush=True)

    if not rolls_queue and len(selected_session_games) < len(available_games):
        print("\n================================", flush=True)
        while True:
            overtime = input("\n[Enter] Lock / [+] Encore: ").strip()
            if overtime in ["", "+"]:
                break
            print("⚠️  Command unrecognized.", flush=True)
            
        if overtime == "+":
            next_act_num = len(selected_session_games) + 1
            bonus_diff = random.choice(["Easy", "Hard"])
            rolls_queue.append((bonus_diff, f"✨ ACT {next_act_num}: ENCORE ({bonus_diff})"))

# --- PHASE 2: GO PLAY / DEBRIEF AFTER-ACTION REPORT ---
print("\n🎮 ITINERARY LOCKED. GOOD LUCK! 🎮", flush=True)
print("================================", flush=True)

while True:
    gate_check = input("Type [c] + Enter to open After-Action Report: ").strip().lower()
    if gate_check == "c":
        break
    print("⚠️  Type 'c' to open debrief.", flush=True)

print("\n🏆 DEBRIEFING: AFTER-ACTION REPORT 🏆", flush=True)
print("--------------------------------", flush=True)
new_points = 0
cleared_this_session = []

for game in selected_session_games:
    print(f"\n⚔️  REVIEW: {game.upper()}", flush=True)
    deck = game_stacked_objectives[game]
    
    for idx, obj in enumerate(deck, 1):
        if obj == "Sandbox Freeplay Night": 
            print("   👉 Sandbox Freeplay Night completed.", flush=True)
            continue
            
        while True:
            print(f"\n   👉 Clear Obj {idx}? (y/n):", flush=True)
            display_wrapped_objective("   [", f"{obj}]")
            check = input("   >> ").strip().lower()
            if check in ['y', 'n']:
                break
            print("      ⚠️  Enter 'y' or 'n'.", flush=True)
            
        if check == 'y':
            new_points += 10
            cleared_this_session.append(obj)  
            print("      ✨ Clear! +10G Added.", flush=True)
        else:
            print("      💤 Logged. No points.")

# --- FINAL SCORE & METRICS LAYER SAVE ---
print("\n================================", flush=True)
if new_points > 0:
    gamer_score += new_points
    if not TESTING_MODE:
        with open(ACHIEVEMENT_FILE, "w", encoding="utf-8") as f:
            f.write(f"TOTAL_GAMER_SCORE: {gamer_score}\n")
            f.write(f"LAST_UPDATED: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
        with open(COMPLETED_FILE, "a", encoding="utf-8") as f:
            for accomplished_card in cleared_this_session:
                f.write(f"{accomplished_card}\n")
                
        print(f"🎉 UPDATED! Earned +{new_points}G.", flush=True)
        print(f"👑 Total Score: {gamer_score}G", flush=True)
        print("🗂️  Cards retired safely.", flush=True)
    else:
        print(f"🧪 SIMULATION: You earned {new_points}G.", flush=True)
        print(f"🧪 Simulated Total: {gamer_score}G (Files safe)", flush=True)
        print(f"🧪 Retired: {len(cleared_this_session)} cards.", flush=True)
else:
    print(f"🎮 Session over. Total Gamer Score: {gamer_score}G", flush=True)
print("================================", flush=True)

if not TESTING_MODE:
    all_history.extend(selected_session_games)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        for game in all_history: f.write(f"{game}\n")
