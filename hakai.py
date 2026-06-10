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
    
    if not os.path.exists(ACHIEVEMENT_FILE):
        with open(ACHIEVEMENT_FILE, "w", encoding="utf-8") as f:
            f.write("TOTAL_GAMER_SCORE: 0\n")
            f.write(f"LAST_UPDATED: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        healed_any = True

    if not os.path.exists(HISTORY_FILE):
        open(HISTORY_FILE, "w", encoding="utf-8").close()
        healed_any = True

    if not os.path.exists(COMPLETED_FILE):
        open(COMPLETED_FILE, "w", encoding="utf-8").close()
        healed_any = True

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

# Run diagnostics at boot
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

# --- INITIAL MODE ROUTER ---
print("--- Select Execution Mode ---", flush=True)
print("[1] Simulation (Test Run)", flush=True)
print("[2] Production (Live Records)", flush=True)

while True:
    mode_choice = input("\nSelect mode (1 or 2): ").strip()
    if mode_choice in ["1", "2"]:
        break
    print("⚠️  Invalid entry. Use 1 or 2.", flush=True)

TESTING_MODE = (mode_choice == "1")

# --- DATA ROUTING LAYER ---
if TESTING_MODE:
    print("\n🧪 --- TESTING MODE ACTIVE --- 🧪", flush=True)
    print("Using Simulated History Data...\n", flush=True)
    all_history = ["The Division 2", "Helldivers 2", "Titanfall 2"]
else:
    print("\n⚡ --- LIVE RUNTIME ENGAGED --- ⚡", flush=True)
    print("Accessing Production Ecosystem...\n", flush=True)
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
    print("⚠️  Invalid entry. Use 1 or 2.", flush=True)

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

# Setup session history metrics
current_day = datetime.datetime.now().weekday()
counts = collections.Counter(all_history)
max_plays = max(counts.values()) if counts else 0

selected_session_games = []
game_difficulties = {}
game_stacked_objectives = {}

# 🧠 ESCALATION ENGINE DATA LAYER
session_points_earned = 0
session_cleared_cards = []
encore_mode_active = False
encore_count = 0
is_sudden_death = False

# =========================================================
# THE ENGINE EXECUTION LOOP
# =========================================================
while True:
    # --- PHASE 1: SPIN ENGINE ---
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

        print(f"\n{act_title}", flush=True)
        print("--------------------------------", flush=True)

        winner = random.choices(available_games, weights=weights, k=1)[0]
        selected_session_games.append(winner)
        game_difficulties[winner] = target_difficulty
        
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
        
        while len(active_deck) < 3 and pool_options and not is_sudden_death:
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

    # --- PHASE 2: AFTER-ACTION REPORT DEBRIEF ---
    print("\n🎮 ITINERARY LOCKED. GO STREAM SESSIONS! 🎮", flush=True)
    print("================================", flush=True)

    while True:
        gate_check = input("Type [c] + Enter to open After-Action Report: ").strip().lower()
        if gate_check == "c":
            break
        print("⚠️  Type 'c' to open debrief.", flush=True)

    print("\n🏆 DEBRIEFING: AFTER-ACTION REPORT 🏆", flush=True)
    print("--------------------------------", flush=True)
    
    total_attempted_cards = 0
    total_cleared_cards = 0
    current_review_games = selected_session_games[-1:] if encore_mode_active else selected_session_games

    for game in current_review_games:
        print(f"\n⚔️  REVIEW: {game.upper()}", flush=True)
        deck = game_stacked_objectives[game]
        
        for idx, obj in enumerate(deck, 1):
            if obj == "Sandbox Freeplay Night": 
                print("   👉 Sandbox Freeplay Night completed.", flush=True)
                continue
                
            total_attempted_cards += 1
            while True:
                print(f"\n   👉 Clear Obj {idx}? (y/n):", flush=True)
                display_wrapped_objective("   [", f"{obj}]")
                check = input("   >> ").strip().lower()
                if check in ['y', 'n']:
                    break
                print("      ⚠️  Enter 'y' or 'n'.", flush=True)
                
            if check == 'y':
                total_cleared_cards += 1
                session_cleared_cards.append(obj)
                card_value = 25 if is_sudden_death else 10
                session_points_earned += card_value
                print(f"      ✨ Clear! +{card_value}G Added.", flush=True)
            else:
                if is_sudden_death:
                    session_points_earned -= 15
                    print("      💀 FAILED! -15G Escalation Penalty Applied.", flush=True)
                else:
                    print("      💤 Logged. No points assigned.", flush=True)

    # --- PHASE 3: ESCALATION ENGINE GATE ---
    print("\n================================", flush=True)
    
    success_rate = (total_cleared_cards / total_attempted_cards) if total_attempted_cards > 0 else 0
    
    while True:
        # 🎮 SHARPER INTERFACE VERBIAGE
        overtime = input("\n[Enter] Save & Quit / [+] Encore: ").strip()
        if overtime in ["", "+"]:
            break
        print("⚠️  Command unrecognized.", flush=True)
        
    if overtime == "+":
        encore_mode_active = True
        encore_count += 1
        
        if success_rate == 1.0:
            is_sudden_death = True
            bonus_diff = "Hard"
            title = f"💀 ACT {encore_count + 1}: SUDDEN DEATH"
            
            # 🧠 SAFELY WRAPPED ALERTS TO PREVENT MOBILE CLIPPING
            print("\n🔥 PERFECT RUN DETECTED!", flush=True)
            display_wrapped_objective("🚨 ", "WARNING: High-reward (+25G) / Failure penalty (-15G) active.")
        else:
            is_sudden_death = False
            bonus_diff = "Hard" if success_rate >= 0.5 else "Easy"
            title = f"✨ ACT {encore_count + 1}: THE ENCORE"
            
            print(f"\n📈 Performance: {success_rate*100:.0f}%", flush=True)
            display_wrapped_objective("🗂️  ", f"Card deck calibrated to {bonus_diff} parameters.")
            
        rolls_queue.append((bonus_diff, title))
        time.sleep(1.2)
        continue  
    else:
        break  

# =========================================================
# FINAL ACCOUNT DATA PERSISTENCE LAYER SAVE
# =========================================================
print("\n🏆 SESSION TERMINATED: FINAL ACCOUNTS 🏆", flush=True)
print("================================", flush=True)

if session_points_earned != 0:
    gamer_score += session_points_earned
    if not TESTING_MODE:
        with open(ACHIEVEMENT_FILE, "w", encoding="utf-8") as f:
            f.write(f"TOTAL_GAMER_SCORE: {gamer_score}\n")
            f.write(f"LAST_UPDATED: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
        with open(COMPLETED_FILE, "a", encoding="utf-8") as f:
            for accomplished_card in session_cleared_cards:
                f.write(f"{accomplished_card}\n")
                
        print(f"🎉 PROFILE UPDATED! Net Change: {session_points_earned:+}G.", flush=True)
        print(f"👑 Total Gamer Score: {gamer_score}G", flush=True)
    else:
        print(f"🧪 SIMULATION: Net Session Change: {session_points_earned:+}G.", flush=True)
        print(f"🧪 Simulated Total Score: {gamer_score}G (Files safe)", flush=True)
        print(f"🧪 Cards Slate to Retire: {len(session_cleared_cards)} cards.", flush=True)
else:
    print(f"🎮 Session over. Total Gamer Score: {gamer_score}G", flush=True)
print("================================", flush=True)

if not TESTING_MODE and selected_session_games:
    all_history.extend(selected_session_games)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        for game in all_history: f.write(f"{game}\n")
