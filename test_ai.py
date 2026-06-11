import os
from ai_client import OracleFish
from state_manager import HakaiStateManager

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
# Initialize systems
state = HakaiStateManager()
client = OracleFish()

# Display starting wallet values
print("📊 Pulling current local save data...")
print(state.get_status_overview())

print("\n🔮 Consulting the Oracle Fish for a contract...")
card_data = client.generate_challenge(game="Helldivers 2", difficulty="Hard")

if card_data["status"] == "success":
    # Stake the challenge card
    state.stake_mission(card_data)
    
    # Simulate completing it right away for verification testing
    print("\n⚔️ Simulating successful combat run...")
    state.complete_mission()
    
    # Print the updated profile overview showing the point addition
    print("\n📊 Final Updated Status Sync:")
    print(state.get_status_overview())
