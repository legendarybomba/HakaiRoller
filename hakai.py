import collections
import datetime
import os
import random
import sys
import time
import textwrap

# EXPERIMENTAL BRANCH IMPORTS
from ai_client import OracleFish
from state_manager import HakaiStateManager

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
COMPLETED_FILE = "completed_achievements.txt"  
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
    print("🛠  Running system diagnostic...", flush=True)
    
    if not os.path.exists(HISTORY_FILE):
        open(HISTORY_FILE, "w", encoding="utf-8").close()
        healed_any = True

    if not os.path.exists(COMPLETED_FILE):
        open(COMPLETED_FILE, "w", encoding="utf-8").close()
        healed_any = True

    if healed_any:
        print("✨ Diagnostic: Assets restored. [OK]\n", flush=True)
    else:
        print("✨ Diagnostic: Verified. [OK]\n", flush=True)

# Run diagnostics at boot
heal_environment()

# =========================================================
# EXPERIMENTAL SUBSYSTEM INITIALIZATION
# =========================================================
# We pass "gamer_profile.txt" directly to your State Manager to preserve your production save location!
state = HakaiStateManager(filename="gamer_profile.txt")
oracle = OracleFish()

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

# Override state manager saving if in test mode to protect live logs
if TESTING_MODE:
    print("\n🧪 --- TESTING MODE ACTIVE --- 🧪", flush=True)
    print("Using Simulated History Data...\n", flush=True)
    all_history = ["The Division 2", "Helldivers 2", "Titanfall 2"]
    # Hot-swap the save coordinator to a sandbox file for testing safety
    state.filename = "gamer_profile_sim.txt"
else:
    print("\n⚡ --- LIVE RUNTIME ENGAGED --- ⚡", flush=True)
    print("Accessing Production Ecosystem...\n", flush=True)
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            all_history = [line.strip() for line in f if line.strip() in GAME_POOL]
    else:
        all_history = []

recent_blocks = all_history[-SHORT_TERM_COOL_DOWN:] if all_history else []

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
counts = collections.Counter(all_history)
max_plays = max(counts.values()) if counts else 0

selected_session_games = []
game_session_cards = {}  # Tracks the full dict payloads returned by OracleFish

# ESCALATION ENGINE DATA LAYER
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
        current_day = datetime.datetime.now().weekday()
        
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
        
        # UI Spin Routine
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
        
        # CONNECT TO THE ORACLE FISH PIPELINE
        print("🔮 Consulting the Oracle Fish...", flush=True)
        card_data = oracle.generate_challenge(game=winner, difficulty=target_difficulty)
        
        if card_data["status"] == "error":
            print(f"❌ Oracle Error: {card_data['message']}", flush=True)
            # Fallback to local default string if API fails entirely
            card_data = {
                "status": "success",
                "game": winner,
                "difficulty": target_difficulty,
                "objective": "Sandbox Freeplay Night (API Pipeline Timeout)",
                "base_payout": 10
            }
            
        # Adjust payout for sudden death multipliers
        if is_sudden_death:
            card_data["base_payout"] = 25
            
        game_session_cards[winner] = card_data
        display_wrapped_objective("💎 Objective: ", card_data["objective"])
        print(f"💰 Potential Yield: {card_data['base_payout']} XP/G", flush=True)
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
        print(f"\n⚔ Review: {game.upper()}", flush=True)
        card = game_session_cards[game]
        total_attempted_cards += 1
        
        while True:
            print(f"\n   👉 Clear Challenge?", flush=True)
            display_wrapped_objective("   [", f"{card['objective']}]")
            check = input("   (y/n) >> ").strip().lower()
            if check in ['y', 'n']:
                break
            print("      ⚠️  Enter 'y' or 'n'.", flush=True)
            
        if check == 'y':
            total_cleared_cards += 1
            session_cleared_cards.append(card['objective'])
            
            # Map into our State Manager engine profile
            state.stake_mission(card)
            state.complete_mission()
            session_points_earned += card['base_payout']
        else:
            if is_sudden_death:
                state.profile["wallet_balance"] -= 15
                session_points_earned -= 15
                print("      💀 FAILED! -15G Escalation Penalty Applied.", flush=True)
                state.save_profile()
            else:
                print("      💤 Logged. No points assigned.", flush=True)

    # --- PHASE 3: ESCALATION ENGINE GATE ---
    print("\n================================", flush=True)
    success_rate = (total_cleared_cards / total_attempted_cards) if total_attempted_cards > 0 else 0
    
    while True:
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

print(state.get_status_overview(), flush=True)

if not TESTING_MODE and session_cleared_cards:
    with open(COMPLETED_FILE, "a", encoding="utf-8") as f:
        for accomplished_card in session_cleared_cards:
            f.write(f"{accomplished_card}\n")

if not TESTING_MODE and selected_session_games:
    all_history.extend(selected_session_games)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        for game in all_history: 
            f.write(f"{game}\n")

print("================================", flush=True)
