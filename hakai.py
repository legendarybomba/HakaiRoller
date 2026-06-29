import collections
import random
import textwrap

# Internal Imports
from oraclefish_goblet import OracleFish
from yemmas_tome_mgr import YemmasTomeManager

# CONFIGURATION
GAME_POOL = [
    "Fallout 76", "The Division 2", "The First Descendant", "Helldivers 2",
    "Titanfall 2", "Doom Eternal", "Soulcalibur 6", "DB Xenoverse 2",
    "Gears 5", "Rainbow Six Vegas 2"
]
COOP_GAMES = ["Fallout 76", "The Division 2", "The First Descendant", "Helldivers 2", "Gears 5", "Rainbow Six Vegas 2"]
SHORT_TERM_COOL_DOWN = 3

# INITIALIZATION
state = YemmasTomeManager(filename="yemmas_tome.json")
oracle = OracleFish()

def roll_game(session_type="1"):
    """Core logic to roll a game, used by both CLI and Web API."""
    all_history = [g for g in state.profile.get("history", []) if g in GAME_POOL]
    recent_blocks = all_history[-SHORT_TERM_COOL_DOWN:] if all_history else []
    
    available = [g for g in GAME_POOL if g not in recent_blocks] or GAME_POOL
    
    if session_type == "2": # Co-Op
        available = [g for g in available if g in COOP_GAMES] or COOP_GAMES
        
    return random.choice(available)

# CLI EXECUTION BLOCK
if __name__ == "__main__":
    print("--- Hakai Engine CLI ---")
    print("[1] Solo | [2] Co-Op")
    choice = input("Select mode: ").strip()
    
    game = roll_game(choice)
    print(f"\n🎯 TARGET LOCKED: {game.upper()}")
    
    card = oracle.generate_challenge(game=game, difficulty="Heated")
    print(f"💎 Obj: {card['objective']}")
    
    if input("\nClear mission? (y/n) >> ").lower() == 'y':
        state.stake_mission(card)
        state.complete_mission()
        print("✅ Mission Synced.")
