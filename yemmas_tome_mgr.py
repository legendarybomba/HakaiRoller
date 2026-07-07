import json
import os

class YemmasTomeManager:
    def __init__(self, filename="yemmas_tome.json"):
        self.filename = filename
        self.data = self._load()

    def _load(self) -> dict:
        """Loads the registry from disk, fallback to a clean Ginyu-approved default state."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Fresh initialization schema
        return {
            "user_profile": {
                "gamertag": "Player1", 
                "platform": "Steam"
            },
            "settings": {
                "rotation_limit": 10,
                "difficulty_default": "Heated"
            },
            # Expanded structure: ready for direct SteamDB appid lookups
            "library": [],  # List of dicts: {"game": "Name", "appid": None, "weight": 0}
            "wallet": 0,
            "total_xp": 0,
            "history": [],
            "achievements": [],
            "dragon_balls": []
        }

    def reorder_deck(self, game_name, requested_index=3):
        """
        Shuffles a game deeper into the rotation stack.
        Ensures the fatigue drop scales naturally based on the total number of games currently in the deck.
        """
        library = self.data.get("library", [])
        game_data = next((item for item in library if item["game"] == game_name), None)
        
        if game_data:
            library.remove(game_data)
            
            # Dynamic Fatigue Check: Calculate the max possible safe position in the current deck
            deck_size = len(library) # Size after removal
            
            # If the deck size is small, default to pushing it to the very back.
            # Otherwise, use the requested depth or cap it at the deck's bound boundary.
            actual_new_index = min(requested_index, deck_size) if deck_size > requested_index else deck_size
            
            library.insert(actual_new_index, game_data)
            self.save()

    def commit_session(self, xp, history, achievements):
        """Appends active gaming timeline data and updates overall progress tracking."""
        self.data["total_xp"] += xp
        self.data["history"].extend(history)
        self.data["achievements"].extend(achievements)
        self.save()
        print("📜 Yemma's Tome ledger committed safely to the timeline database.")
    
    def save(self):
        """Serializes current memory state straight to persistent JSON storage."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)
