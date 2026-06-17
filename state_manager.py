import json
import os

class HakaiStateManager:
    def __init__(self, filename="profile.json"):
        self.filename = filename
        self.profile = self._load_profile()
        self.active_mission = None

    def sync_tome(self, history_entries=None, achievement_entries=None):
        """Updates the ledger with new session data."""
        if "history" not in self.profile:
            self.profile["history"] = []
        if "completed_achievements" not in self.profile:
            self.profile["completed_achievements"] = []
            
        if history_entries:
            self.profile["history"].extend(history_entries)
        
        if achievement_entries:
            self.profile["completed_achievements"].extend(achievement_entries)
            
        self.save_profile()
        print("📜 Yemma's Tome updated with session data.")
  
    def _load_profile(self) -> dict:
        """Loads JSON, converts legacy plain text scores, or generates a fresh profile."""
        default_profile = {
            "character_level": 1,
            "wallet_balance": 0,
            "total_xp": 0,
            "completed_missions": 0
        }

        if os.path.exists(self.filename):
            try:
                # 1. Try reading as our new structured JSON system
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                # 2. JSON failed, meaning it's likely your legacy plain-text file format!
                print("🛠️ Legacy profile file format detected. Migrating stats...")
                legacy_score = 0
                try:
                    with open(self.filename, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.startswith("TOTAL_GAMER_SCORE:"):
                                legacy_score = int(line.split(":")[1].strip())
                    
                    # Convert your legacy score directly into your new wallet/XP bank!
                    default_profile["wallet_balance"] = legacy_score
                    default_profile["total_xp"] = legacy_score
                    
                    # Simple automated catch-up calculation for character level mapping
                    default_profile["character_level"] = (legacy_score // 2500) + 1
                    
                    print(f"✨ Migration Complete! Transferred {legacy_score}G to the new wallet.")
                    return default_profile
                except Exception as migration_error:
                    print(f"⚠️ Profile read failure: {str(migration_error)}. Using default profile.")
                    return default_profile
        
        return default_profile

    def save_profile(self):
        """Saves current state to local JSON storage."""
        with open(self.filename, 'w') as f:
            json.dump(self.profile, f, indent=4)

    def stake_mission(self, card_data: dict):
        """Locks in the active mission payload from the Oracle Fish."""
        if card_data.get("status") == "success":
            self.active_mission = card_data
            print(f"🎯 Target Locked: Mission staked for {card_data['base_payout']} points.")
        else:
            print("❌ Cannot stake an invalid mission card.")

    def complete_mission(self):
        """Awards points and progress updates from the active stake."""
        if not self.active_mission:
            print("❌ No active mission to complete.")
            return

        payout = self.active_mission.get("base_payout", 0)
        self.profile["wallet_balance"] += payout
        self.profile["completed_missions"] += 1
        
        # Simple RPG calculation: Payout equals matching XP gains
        self.profile["total_xp"] += payout
        
        print(f"🏆 Mission Accomplished! +{payout} points added to wallet.")
        
        # Check for level up milestone thresholds
        self._check_level_up()
        
        # Clear the active slot and sync to files
        self.active_mission = None
        self.save_profile()

    def _check_level_up(self):
        """Basic milestone tracking to calculate character level increases."""
        xp_per_level = 2500
        calculated_level = (self.profile["total_xp"] // xp_per_level) + 1
        if calculated_level > self.profile["character_level"]:
            self.profile["character_level"] = calculated_level
            print(f"⚡ LEVEL UP! Engine profile advanced to Level {calculated_level}! ⚡")

    def get_status_overview(self) -> str:
        """Returns a scannable text panel of your profile stats."""
        return (
            f"=== HAKAI ENGINE PROFILE ===\n"
            f"🏅 Level: {self.profile['character_level']}\n"
            f"💰 Wallet: {self.profile['wallet_balance']} pts\n"
            f"✨ Total XP: {self.profile['total_xp']}\n"
            f"📊 Cleared Contracts: {self.profile['completed_missions']}\n"
            f"============================"
        )
