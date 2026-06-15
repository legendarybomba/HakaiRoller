import os
import re
from google import genai
from google.genai import types

class OracleFish:
    def __init__(self):
        # SDK automatically looks for GOOGLE_API_KEY environment variable
        self.client = genai.Client()

    def generate_challenge(self, game: str, difficulty: str) -> dict:
        system_instruction = (
            "You are the Hakai Gaming Engine AI Director. Generate high-stakes challenge cards.\n"
            "DIFFICULTY SCALE:\n"
            " - Easy: Straightforward, light requirements.\n"
            " - Heated: Tactical focus, slight friction.\n"
            " - Hard: Brutal, maximum friction, survival requirements.\n\n"
            "OUTPUT FORMAT (Raw text only, no markdown):\n"
            "GAME:[Name]\n"
            "DIFFICULTY:[Level]\n"
            "OBJECTIVE:[Concise, high-stakes objective]\n"
            "BASE_PAYOUT:[Integer value]"
        )
        
        user_prompt = f"Generate a {difficulty} challenge card for: {game}."

        try:
            config = types.GenerateContentConfig(
                systemInstruction=system_instruction,
                temperature=0.7
            )
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash", # Ensure you're using a current stable model
                contents=user_prompt,
                config=config
            )
            
            return self._parse_raw_output(response.text.strip())

        except Exception as e:
            return {"status": "error", "message": f"Pipeline failure: {str(e)}"}

    def _parse_raw_output(self, raw_text: str) -> dict:
        parsed_data = {
            "status": "success",
            "game": "Unknown",
            "difficulty": "Unknown",
            "objective": "Unknown",
            "base_payout": 10
        }
        
        for line in raw_text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key, value = key.strip().upper(), value.strip()
                
                if key == "GAME": parsed_data["game"] = value
                elif key == "DIFFICULTY": parsed_data["difficulty"] = value
                elif key == "OBJECTIVE": parsed_data["objective"] = value
                elif key == "BASE_PAYOUT":
                    # Robust extraction: finds the first number in the string
                    digits = re.findall(r'\d+', value)
                    parsed_data["base_payout"] = int(digits[0]) if digits else 10
                        
        return parsed_data