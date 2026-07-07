# chronoas_decree.py
import random

class ChronoasDecree:
    def __init__(self, tome):
        self.tome = tome

    def roll_for_decree(self, drop_chance=0.05):
        """Attempts to trigger a Decree roll. Defaults to 5%."""
        if not self.tome.data.get("has_decree"):
            if random.random() < drop_chance:
                self.tome.data["has_decree"] = True
                
                # Setup history cleanly if it doesn't exist
                if "history" not in self.tome.data:
                    self.tome.data["history"] = []
                    
                self.tome.data["history"].append("⏳ Chronoa has bestowed a Decree upon you.")
                # self.tome.save() # We remove explicit saves here; let Hakai's main cycle handle the write!
                return True
        return False

    def invoke_decree(self, game_title: str):
        """Consumes the Decree to nullify a mission and shuffles the timeline deck."""
        if self.tome.data.get("has_decree"):
            self.tome.data["has_decree"] = False
            
            if "history" not in self.tome.data:
                self.tome.data["history"] = []
            self.tome.data["history"].append(f"⏳ Exercised Chronoa's Decree: prophecy for {game_title} nullified.")
            
            # 🟢 THE TIMELINE BYPASS LOGIC:
            # Send the hated game straight to the back of the queue (fatigue max out)
            self.tome.reorder_deck(game_title, max_fatigue=True) 
            
            print(f"✨ CHRONOA: Prophecy shattered! {game_title} has been banished to the end of the timeline.")
            return True
            
        print("❌ CHRONOA: You do not possess a Divine Decree. Prophecy cannot be undone!")
        return False
