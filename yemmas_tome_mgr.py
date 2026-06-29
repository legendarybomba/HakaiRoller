import json
import os

class YemmasTomeManager:
    def __init__(self, filename="yemmas_tome.json"):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "character_level": 1,
            "wallet_balance": 0,
            "total_xp": 0,
            "completed_missions": 0,
            "history": [],
            "completed_achievements": []
        }

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)

    def commit_session(self, wallet_gain, xp_gain, history_list, achievements):
        self.data["wallet_balance"] += wallet_gain
        self.data["total_xp"] += xp_gain
        self.data["completed_missions"] += len(history_list)
        self.data["history"].extend(history_list)
        self.data["completed_achievements"].extend(achievements)
        
        # Simple level check
        self.data["character_level"] = (self.data["total_xp"] // 2500) + 1
        self.save()
        print("📜 Yemma's Tome ledger committed.")
