import collections
import datetime
import os
import random
import sys
import time
import textwrap

from oraclefish_goblet import OracleFish
from state_manager import HakaiStateManager
import dragon_radar

# CONFIGURATION & SOURCE OF TRUTH GATES
GAME_POOL = [
    "Fallout 76", "The Division 2", "The First Descendant", "Helldivers 2",
    "Titanfall 2", "Doom Eternal", "Soulcalibur 6", "DB Xenoverse 2",
    "Gears 5", "Rainbow Six Vegas 2"
]
COOP_GAMES = ["Fallout 76", "The Division 2", "The First Descendant", "Helldivers 2", "Gears 5", "Rainbow Six Vegas 2"]
SHORT_TERM_COOL_DOWN = 3
DIFF_LEVELS = ["Easy", "Heated", "Hard"]
MAX_WIDTH = 32

def display_wrapped_objective(prefix, text):
    wrapped = textwrap.fill(text, width=MAX_WIDTH, initial_indent=prefix, subsequent_indent=" " * len(prefix))
    print(wrapped, flush=True)

# SUBSYSTEM INITIALIZATION
state = HakaiStateManager(filename="profile.json")
oracle = OracleFish()

# INITIAL MODE ROUTER
print("--- Select Execution Mode ---", flush=True)
print("[1] Simulation (Test Run)", flush=True)
print("[2] Production (Live Records)", flush=True)

while True:
    mode_choice = input("\nSelect mode (1 or 2): ").strip()
    if mode_choice in ["1", "2"]:
        break
    print("⚠️  Invalid entry. Use 1 or 2.", flush=True)

TESTING_MODE = (mode_choice == "1")

if TESTING_MODE:
    print("\n🧪 --- TESTING MODE ACTIVE --- 🧪", flush=True)
    all_history = ["The Division 2", "Helldivers 2", "Titanfall 2"]
    state.filename = "gamer_profile_sim.txt"
else:
    print("\n⚡ --- LIVE RUNTIME ENGAGED --- ⚡", flush=True)
    all_history = [g for g in state.profile.get("history", []) if g in GAME_POOL]

recent_blocks = all_history[-SHORT_TERM_COOL_DOWN:] if all_history else []

# MENU ROUTER
print("--- Session Parameters ---", flush=True)
print("[1] Solo Night (Full Library)", flush=True)
print("[2] Co-Op Night (Squad Only)", flush=True)
print("[3] Double Feature (Warmup+Main)", flush=True)

while True:
    session_choice = input("\nSelect choice (1, 2, 3): ").strip()
    if session_choice in ["1", "2", "3"]:
        break
    print("⚠️  Invalid entry. Use 1, 2, or 3.", flush=True)

available_games = [g for g in GAME_POOL if g in COOP_GAMES] if session_choice == "2" else GAME_POOL[:]
available_games = [g for g in available_games if g not in recent_blocks] or GAME_POOL[:]

is_double_feature = (session_choice == "3")
rolls_queue = []

if is_double_feature:
    rolls_queue.extend([("Easy", "🟢 ACT I: WARMUP"), ("Hard", "🔴 ACT II: MAIN EVENT")])
else:
    print("\n--- Intensity Matrix ---", flush=True)
    print("[1] Chill (Easy)\n[2] Heated\n[3] Sweat (Hard)", flush=True)
    while True:
        intensity_choice = input("\nSelect difficulty (1-3): ").strip()
        if intensity_choice in ["1", "2", "3"]: break
    single_diff = ["Easy", "Heated", "Hard"][int(intensity_choice)-1]
    rolls_queue.append((single_diff, "🎮 SINGLE FEATURE"))

counts = collections.Counter(all_history)
max_plays = max(counts.values()) if counts else 0
selected_session_games = []
game_session_cards = {}
session_points_earned = 0
session_cleared_cards = []
encore_mode_active = False
encore_count = 0
is_sudden_death = False

# THE ENGINE EXECUTION LOOP
while True:
    while rolls_queue:
        target_difficulty, act_title = rolls_queue.pop(0)
        weights = [(max_plays - counts[game] + 1) * (1.0) for game in available_games]
        winner = random.choices(available_games, weights=weights, k=1)[0]
        selected_session_games.append(winner)
        
        print(f"\n{act_title}\n--------------------------------", flush=True)
        print(f"🎯 TARGET LOCKED: {winner.upper()}\n", flush=True)
        
        card_data = oracle.generate_challenge(game=winner, difficulty=target_difficulty)
        if card_data["status"] == "error":
            card_data = {"status": "success", "game": winner, "difficulty": target_difficulty, "objective": "Sandbox Freeplay Night", "base_payout": 10}
        if is_sudden_death: card_data["base_payout"] = 25
            
        active_deck = [card_data]
        display_wrapped_objective("💎 Obj 1: ", card_data["objective"])
        print(f"💰 Payout: {card_data['base_payout']} XP/G", flush=True)
        game_session_cards[winner] = active_deck
        print("--------------------------------", flush=True)

    print("\n🎮 ITINERARY LOCKED. GO STREAM SESSIONS! 🎮\n================================", flush=True)
    input("Type [c] + Enter to open After-Action Report: ")

    for game in (selected_session_games[-1:] if encore_mode_active else selected_session_games):
        print(f"\n⚔ Review: {game.upper()}", flush=True)
        for idx, card in enumerate(game_session_cards[game], 1):
            check = input(f"\n   👉 Clear {card['objective']}? (y/n) >> ").strip().lower()
            if check == 'y':
                session_cleared_cards.append(card['objective'])
                state.stake_mission(card)
                state.complete_mission()
                session_points_earned += card['base_payout']
                
                # DRAGON RADAR TRIGGER
                found_star = dragon_radar.calculate_dragon_ball_drop(card['difficulty'], state.profile)
                if found_star:
                    print(f"✨ You found the {found_star} Dragon Ball!")
                    state.save_profile()
            elif is_sudden_death:
                state.profile["wallet_balance"] = max(0, state.profile["wallet_balance"] - 15)
                state.save_profile()

    if input("\n[Enter] Save & Quit / [+] Encore: ") == "+":
        encore_mode_active = True
        encore_count += 1
        success_rate = (len(session_cleared_cards) / len(selected_session_games))
        is_sudden_death = (success_rate == 1.0)
        rolls_queue.append(("Hard" if success_rate >= 0.75 else "Heated", "✨ THE ENCORE"))
        continue
    break

print("\n🏆 SESSION TERMINATED 🏆\n", state.get_status_overview(), flush=True)
if not TESTING_MODE:
    state.sync_tome(history_entries=selected_session_games, achievement_entries=session_cleared_cards)