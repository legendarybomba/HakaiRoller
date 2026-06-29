import random

class SessionManager:
    def __init__(self):
        self.active_mission = None
        self.senzu_beans = 0
        self.wager_active = False
        self.session_history = []
        self.session_achievements = []
        self.session_points = 0

    def stake_mission(self, card_data):
        self.active_mission = card_data
        self.wager_active = False # Reset wager each new stake
        print(f"🎯 Target Locked: {card_data['objective']}")

    def use_senzu_bean(self):
        if self.senzu_beans > 0:
            self.senzu_beans -= 1
            return True
        return False

    def roll_for_senzu_bean(self):
        if self.senzu_beans < 3 and random.random() < 0.07:
            self.senzu_beans += 1
            return True
        return False

    def complete_mission(self, success=True):
        if not self.active_mission: return
        
        payout = self.active_mission.get("base_payout", 0)
        if success:
            self.session_points += payout
            self.session_history.append(self.active_mission["game"])
            self.session_achievements.append(self.active_mission["objective"])
        
        self.active_mission = None
