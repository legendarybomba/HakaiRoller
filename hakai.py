import sys
import random  # 🟢 Added random for the stash roll
from yemmas_tome_mgr import YemmasTomeManager
from oraclefish_goblet import OracleFish
from session_mgr import SessionManager
from chronoas_decree import ChronoasDecree
from korins_stash import KorinsStash  # 🟢 Import your stash
import dragon_radar

class TrinityController:
    def __init__(self):
        # 1. Initialize the Core Registry
        self.tome = YemmasTomeManager()
        
        # 2. Initialize the specialized modules
        self.oracle = OracleFish()
        self.state = SessionManager()
        self.decree = ChronoasDecree(self.tome)
        self.stash = KorinsStash(self.tome)  # 🟢 Pass shared tome to your stash

    def run_cycle(self):
        # 1. Access the local deck state from the Tome
        deck = self.tome.data.get("library", [])
        
        if not deck:
            print("❌ Library empty. Please initialize games in Yemma's Tome.")
            return

        # 2. Pull target profile configurations from settings
        settings = self.tome.data.get("settings", {})
        difficulty_preference = settings.get("difficulty_default", "Heated")

        # 3. Handle data flow explicitly to the Oracle Fish
        current_game_node = deck[0]
        game_title = current_game_node["game"]
        
        # Oracle interprets the timeline parameters and builds the dynamic card
        mission_card = self.oracle.generate_challenge(game_title, difficulty_preference)
        
        # Lock the mission parameters into runtime session memory
        self.state.stake_mission(mission_card)
        
        # 4. Present the interface cleanly to the user
        print("\n========================================")
        print(f"🎯 CURRENT TARGET : {mission_card['game']}")
        print(f"🔥 DIFFICULTY     : {mission_card['difficulty'].upper()}")
        print(f"⚔️ OBJECTIVE      : {mission_card['objective']}")
        print(f"💰 BASE PAYOUT    : {mission_card['base_payout']} XP")
        print("========================================")
        
        # 5. Process user input
        choice = input("\nClear? (y/n) [or 'veto'] >> ").lower().strip()
        
        if choice == 'y':
            # Signal complete to session state tracker
            self.state.complete_mission(success=True)
            
            # 📡 Radar Roll
            found = dragon_radar.calculate_dragon_ball_drop(mission_card['difficulty'], self.tome.data)
            if found: 
                print(f"\n✨ DRAGON RADAR: Signals locked! You secured the {found}!")
            
            # ⏳ Chronoa's Blessing Roll (5% passive chance)
            if self.decree.roll_for_decree():
                print("\n⏳ CHRONOA: The Supreme Kai of Time smiles upon your victory. A Decree has been bestowed!")
            
            # 🟢 KORIN'S PASSIVE BEAN DROP (10% random chance)
            if random.random() < 0.10:
                print("\n🍃 KORIN: A fresh harvest has matured at the top of the tower!")
                self.stash.add_senzu(1)
            
            # Execute the Fatigue mechanic
            self.tome.reorder_deck(game_title, 3) 
            print(f"✨ {game_title} shifted back in the timeline queue.")
            
        elif choice == 'veto':
            # Invoke the Divine Decree, passing the current game to banish it
            success = self.decree.invoke_decree(game_title)
            if not success:
                print("💤 Session cancelled due to lack of cosmic favor.")
                return
            
        else:
            print("💤 Session paused. No structural changes committed to the timeline.")
            return
            
        # 6. Commit the final structural data changes back to disk
        self.tome.commit_session(self.state.session_points, self.state.session_history, [])
        
        # 7. Evaluate the summon state condition
        if len(self.tome.data.get("dragon_balls", [])) >= 7:
            print("\n🐉 WARNING: 7 Dragon Balls gathered. The localized universe is open to modification.")

if __name__ == "__main__":
    print("--- HAKAI ENGINE CORE INITIALIZED ---")
    controller = TrinityController()
    controller.run_cycle()
