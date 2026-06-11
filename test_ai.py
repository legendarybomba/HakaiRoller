import os
from ai_client import OracleFish

if not os.getenv("GEMINI_API_KEY"):
    print("❌ ERROR: GEMINI_API_KEY is not set.")
    exit(1)

print("🔮 Consulting the Oracle Fish...")
client = OracleFish()

print("🎲 Rolling and parsing a test card...")
card_data = client.generate_challenge(game="Helldivers 2", difficulty="Hard")

print("\n=== PARSED DICTIONARY OUTPUT ===")
import pprint
pprint.pprint(card_data)
print("=================================")
