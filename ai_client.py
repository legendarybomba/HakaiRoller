import os
from google import genai
from google.genai import types

class OracleFish:
    def __init__(self):
        self.client = genai.Client()

    def generate_challenge(self, game: str, difficulty: str) -> dict:
        system_instruction = (
            "You are the Hakai Gaming Engine AI Director. Generate high-stakes challenge cards.\n"
            "CRITICAL: Output ONLY raw, unformatted text variables using the exact keys below.\n"
            "Do NOT use markdown code blocks (```), and do NOT include conversational pleasantries.\n"
            "Provide exactly four lines of text formatted like this:\n"
            "GAME:[Game Name]\n"
            "DIFFICULTY:[Difficulty]\n"
            "OBJECTIVE:[One concise, high-stakes objective]\n"
            "BASE_PAYOUT:[Point value]"
        )
        
        user_prompt = f"Generate a {difficulty} challenge card for the game: {game}."

        try:
            config = types.GenerateContentConfig(
                systemInstruction=system_instruction,
                temperature=0.7
            )
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=config
            )
            
            raw_text = response.text.strip()
            return self._parse_raw_output(raw_text)

        except Exception as e:
            return {
                "status": "error",
                "message": f"Network pipeline failure: {str(e)}"
            }

    def _parse_raw_output(self, raw_text: str) -> dict:
        # Initialize default schema structure
        parsed_data = {
            "status": "success",
            "game": "Unknown",
            "difficulty": "Unknown",
            "objective": "Unknown",
            "base_payout": 0
        }
        
        # Split text by lines and parse key-value pairs
        lines = raw_text.split("\n")
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().upper()
                value = value.strip()
                
                if key == "GAME":
                    parsed_data["game"] = value
                elif key == "DIFFICULTY":
                    parsed_data["difficulty"] = value
                elif key == "OBJECTIVE":
                    parsed_data["objective"] = value
                elif key == "BASE_PAYOUT":
                    # Safeguard against non-integer responses
                    try:
                        parsed_data["base_payout"] = int(value)
                    except ValueError:
                        parsed_data["base_payout"] = value
                        
        return parsed_data
