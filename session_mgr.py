# session_mgr.py

class SessionManager:
    def __init__(self):
        self.active_mission = None
        self.session_history = []
        self.session_achievements = []
        self.session_points = 0

    def stake_mission(self, card_data: dict):
        """Locks the active objective parameters into runtime memory before user execution."""
        self.active_mission = card_data

    def complete_mission(self, success: bool = True):
        """Processes mission rewards, formatting clean history strings for Yemma's ledger."""
        if not self.active_mission: 
            print("⚠️ SESSION MGR: No active mission staked. Aborting state capture.")
            return
            
        if success:
            payout = self.active_mission.get("base_payout", 10)
            game_name = self.active_mission.get("game", "Unknown")
            objective = self.active_mission.get("objective", "Unknown")
            difficulty = self.active_mission.get("difficulty", "UNKNOWN")

            # Capture points
            self.session_points += payout
            
            # Format history entry cleanly for long-term tracking
            history_entry = f"[{difficulty}] Cleared objective in {game_name}: {objective}"
            self.session_history.append(history_entry)
            
            # Append objective to the running global achievements tracker
            self.session_achievements.append(objective)
            
            print(f"✨ SESSION MGR: Logged +{payout} XP to current run state.")
            
        # Clear the chamber for the next cycle
        self.active_mission = None
