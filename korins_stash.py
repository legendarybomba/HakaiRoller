# korins_stash.py

class KorinsStash:
    def __init__(self, tome):
        # 🟢 Accept the shared tome instance from the core engine
        self.tome = tome

    def consume_senzu(self):
        """Reduces Senzu bean count if available."""
        if self.tome.data.get("senzu_beans", 0) > 0:
            # Safely adjust the resource count
            self.tome.data["senzu_beans"] -= 1
            
            if "history" not in self.tome.data:
                self.tome.data["history"] = []
            self.tome.data["history"].append("🟢 Ate a Senzu Bean! Fatal timeline fatigue completely restored.")
            
            print("\n⚠️ Senzu Bean consumed! Session fatigue fully cleared.")
            return True
        else:
            print("\n❌ KORIN: Your pouch is completely empty! Scale the tower to get more.")
            return False

    def add_senzu(self, amount=1):
        """Adds Senzu beans to the stash."""
        if "senzu_beans" not in self.tome.data:
            self.tome.data["senzu_beans"] = 0
            
        self.tome.data["senzu_beans"] += amount
        
        if "history" not in self.tome.data:
            self.tome.data["history"] = []
        self.tome.data["history"].append(f"🟢 Added {amount} Senzu Bean(s) to the stash.")
        
        print(f"✨ Senzu Beans added. Total: {self.tome.data['senzu_beans']}")
