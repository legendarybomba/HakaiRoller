import json
import random
import urllib.parse
import urllib.request

class OracleFish:
    def __init__(self):
        # Clean foundation—no API keys or external authentication states required.
        pass

    def generate_challenge(self, game: str, difficulty: str) -> dict:
        """
        Dynamically processes local game achievement arrays based on difficulty matrix.
        Yields the exact dictionary footprint that Hakai expects to consume.
        """
        local_achievement_pool = {
            "HEATED": [
                "Achieve a flawless victory / mission rank clear without items.",
                "Slay an elite boss or clear a sector with maximum modifiers active.",
                "Complete an encounter using only baseline/starting gear configurations.",
                "Speedrun an operational phase breaking your current personal best time."
            ],
            "RELAXED": [
                "Explore an unmapped sub-sector or locate 3 hidden collectibles.",
                "Spend a cycle optimizing character gear, loadouts, or inventory layouts.",
                "Complete a minor secondary side-quest or clear out world map nodes.",
                "Farm necessary raw crafting components for a tier-upgrade project."
            ]
        }
        
        # Standardize matching casing
        diff_upper = difficulty.upper() if difficulty else "HEATED"
        if diff_upper not in local_achievement_pool:
            diff_upper = "HEATED"
            
        # Select objective from the appropriate pool
        pool = local_achievement_pool[diff_upper]
        selected_objective = random.choice(pool)
        
        # Balance payouts locally based on challenge difficulty weight
        base_payout = 35 if diff_upper == "HEATED" else 15

        return {
            "game": game,
            "difficulty": diff_upper,
            "objective": selected_objective,
            "base_payout": base_payout
        }

    def fetch_appid_by_name(self, game_name: str) -> int:
        """
        Queries Steam's public storefront API to automatically resolve an AppID 
        by text search. Eliminates manual lookups for the user.
        """
        try:
            # Encode the game title cleanly for a URL query string
            encoded_name = urllib.parse.quote(game_name)
            url = f"https://store.steampowered.com/api/storesearch/?term={encoded_name}&l=english&cc=US"
            
            # Make a lightweight, login-free web request
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Hakai Gaming Engine Architecture Auditing System)'}
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                
                # If Steam found a match, grab the AppID of the very first result
                if res_data.get("total", 0) > 0:
                    resolved_id = res_data["items"][0]["id"]
                    print(f"📡 ORACLE FISH: Auto-resolved '{game_name}' to Steam AppID {resolved_id}")
                    return resolved_id
                    
        except Exception as e:
            print(f"⚠️ ORACLE FISH: Could not auto-resolve AppID for '{game_name}': {e}")
            
        return None # Graceful fallback if offline, timed out, or game isn't on Steam

    def generate_steamdb_url(self, appid: int) -> str:
        """
        Utility method to quickly output the exact, login-free SteamDB target 
        for tracking public milestone performance metrics.
        """
        if not appid:
            return "No AppID linked to this game in the registry."
        return f"https://steamdb.info/app/{appid}/achievements/"
