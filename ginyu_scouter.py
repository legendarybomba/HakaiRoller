import flet as ft
import time
import random
import re
import os

# =========================================================================
# TRINITY ARCHITECTURE STATE BACKEND
# =========================================================================
class OracleFish:
    def __init__(self):
        self.active = False
        if "GOOGLE_API_KEY" in os.environ:
            try:
                from google import genai
                from google.genai import types
                self.genai = genai
                self.types = types
                self.client = genai.Client()
                self.active = True
            except Exception:
                self.active = False

    def generate_challenge(self, game: str, difficulty: str) -> dict:
        if not self.active:
            payouts = {"Heated": 250, "Hard": 500}
            objectives = {
                "The Division 2": [
                    {"title": "DZ Extraction", "desc": "Extract outstanding high-value targets in dark zone safely."},
                    {"title": "Armor Preservation", "desc": "Clear localized sector landmarks without losing your armor pool."},
                    {"title": "Heroic Infiltration", "desc": "Infiltrate a stronghold on Heroic difficulty with an active directive."}
                ],
                "Fallout 76": [
                    {"title": "Horde Eradication", "desc": "Clear a Super Mutant horde using heavy ballistic weaponry."},
                    {"title": "Scorchbeast Intercept", "desc": "Exterminate a Scorchbeast before the mutation window closes completely."},
                    {"title": "Fluid Collection", "desc": "Secure localized sector landmarks and collect radioactive fluid."}
                ]
            }
            game_objs = objectives.get(game, [{"title": "Tactical Op", "desc": "Execute standard tactical field operation."}])
            chosen = random.choice(game_objs)
            return {
                "status": "success",
                "game": game,
                "difficulty": difficulty,
                "title": chosen["title"],
                "objective": chosen["desc"],
                "base_payout": payouts.get(difficulty, 100)
            }

        system_instruction = (
            "You are the Hakai Gaming Engine AI Director. Generate high-stakes challenge cards.\n"
            "DIFFICULTY SCALE:\n"
            " - Easy: Straightforward, light requirements.\n"
            " - Heated: Tactical focus, slight friction.\n"
            " - Hard: Brutal, maximum friction, survival requirements.\n\n"
            "OUTPUT FORMAT (Raw text only, no markdown):\n"
            "GAME:[Name]\n"
            "DIFFICULTY:[Level]\n"
            "TITLE:[Short 2-3 word punchy objective title]\n"
            "OBJECTIVE:[Concise, high-stakes tactical description]\n"
            "BASE_PAYOUT:[Integer value]"
        )
        user_prompt = f"Generate a {difficulty} challenge card for: {game}."
        try:
            config = self.types.GenerateContentConfig(
                systemInstruction=system_instruction,
                temperature=0.7
            )
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
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
            "title": "Tactical Operation",
            "objective": "Unknown Details",
            "base_payout": 10
        }
        for line in raw_text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key, value = key.strip().upper(), value.strip()
                if key == "GAME": parsed_data["game"] = value
                elif key == "DIFFICULTY": parsed_data["difficulty"] = value
                elif key == "TITLE": parsed_data["title"] = value
                elif key == "OBJECTIVE": parsed_data["objective"] = value
                elif key == "BASE_PAYOUT":
                    digits = re.findall(r'\d+', value)
                    parsed_data["base_payout"] = int(digits[0]) if digits else 10
        return parsed_data

class SessionManager:
    def __init__(self):
        self.active_missions = []
        self.senzu_beans = 1
        self.wager_active = False
        self.session_history = []
        self.session_achievements = []
        self.session_points = 0

    def stake_missions(self, card_list):
        self.active_missions = card_list
        self.wager_active = False
        for card in card_list:
            print(f"🎯 Target Locked: {card['objective']}")

    def use_senzu_bean(self):
        if self.senzu_beans > 0:
            self.senzu_beans -= 1
            return True
        return False

class YemmasTomeManager:
    def __init__(self, filename="yemmas_tome.json"):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        return {
            "character_level": 40,
            "wallet_balance": 1450,
            "total_xp": 133157,
            "completed_missions": 22,
            "history": [],
            "completed_achievements": [],
            "dragon_balls": ["1-Star", "2-Star", "7-Star"]
        }

# DRAGON BALL RADAR CORE LOGIC
DRAGON_BALL_MAX = 7
ALL_STARS = ["1-Star", "2-Star", "3-Star", "4-Star", "5-Star", "6-Star", "7-Star"]

def calculate_dragon_ball_drop(difficulty: str, profile_data: dict) -> str or None:
    if "dragon_balls" not in profile_data:
        profile_data["dragon_balls"] = []
    current_balls = profile_data["dragon_balls"]
    if len(current_balls) >= DRAGON_BALL_MAX:
        return None
    drop_chances = {"easy": 0.08, "heated": 0.25, "hard": 0.55}
    roll = random.random()
    if roll < drop_chances.get(difficulty.lower(), 0.05):
        remaining_stars = [s for s in ALL_STARS if s not in current_balls]
        if not remaining_stars:
            return None
        new_star = random.choice(remaining_stars)
        profile_data["dragon_balls"].append(new_star)
        return new_star
    return None


# =========================================================================
# SCOUTER FRONTEND LAYOUT ENGINE
# =========================================================================
def main(page: ft.Page):
    session = SessionManager()
    tome = YemmasTomeManager()
    oracle = OracleFish()
    pending_cards = {"payloads": []}

    page.title = "Project Hakai: Scouter UI"
    page.background_color = "#0B1116"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 0
    page.spacing = 0

    # COMPONENT 1: IDENTITY HEADER 
    identity_header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(value="LEGENDBOMBA#3129", size=16, weight=ft.FontWeight.BOLD, color="#D6F5FF"),
                ft.Text(value="★", size=16, color="#59C3E6", weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER, spacing=15
        ),
        width=360, height=55, padding=10, bgcolor="#0F1B22", border_radius=6,
        border=ft.Border(top=ft.BorderSide(1.5, "#25475A"), bottom=ft.BorderSide(1.5, "#25475A"), left=ft.BorderSide(1.5, "#25475A"), right=ft.BorderSide(1.5, "#25475A"))
    )

    # COMPONENT 2: ARTISTIC MASTERY RANK CARD
    mastery_card = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Stack([
                        ft.Text(value="▼", size=32, color="#B58A4C", weight=ft.FontWeight.BOLD),
                        ft.Text(value="▲", size=32, color="#E3BA6D", weight=ft.FontWeight.BOLD, top=8)
                    ]),
                    width=45, alignment=ft.Alignment(0, 0)
                ),
                ft.Column(
                    controls=[
                        ft.Text(value=f"Mastery Rank {tome.data['completed_missions']}", size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        ft.Text(value=f"XP {tome.data['total_xp']:,} / 229,600", size=12, color="#7A8B99"),
                        ft.Container(
                            width=240, height=5, bgcolor="#13231F", border_radius=3,
                            content=ft.Row([ft.Container(width=140, height=5, bgcolor="#00E676", border_radius=3)], alignment=ft.MainAxisAlignment.START)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER, spacing=6
                )
            ],
            alignment=ft.MainAxisAlignment.START, spacing=15
        ),
        width=360, height=90, padding=ft.Padding(20, 10, 15, 10), bgcolor="#111C24", border_radius=6,
        border=ft.Border(bottom=ft.BorderSide(1.5, "#1F3542"))
    )

    # COMPONENT 3: CHARACTER PORTRAIT CARD
    character_level_text = ft.Text(value=f"Lv {tome.data['character_level']}", size=14, color="#59C3E6", weight=ft.FontWeight.W_500)
    character_name_text = ft.Text(value="INES", size=24, weight=ft.FontWeight.BOLD, color="#FFFFFF")
    character_subtitle_text = ft.Text(value=f"Hakai Level {tome.data['character_level']}", size=12, color="#7A8B99")

    character_card = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(controls=[character_level_text, character_name_text, character_subtitle_text], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    width=190, padding=ft.Padding(5, 0, 0, 0)
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(value="[ IMAGE ]", size=11, color="#3A5E75", weight=ft.FontWeight.BOLD),
                        ft.Text(value="ANCHOR", size=10, color="#253D4C")
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    width=110, height=140, bgcolor="#0B1216", border_radius=4, alignment=ft.Alignment(0, 0),
                    border=ft.Border(top=ft.BorderSide(1.2, "#1F3542"), bottom=ft.BorderSide(1.2, "#1F3542"), left=ft.BorderSide(1.2, "#1F3542"), right=ft.BorderSide(1.2, "#1F3542"))
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        width=360, height=180, padding=15, bgcolor="#121F28", border_radius=4
    )

    # COMPONENT 4: CONSUMABLES DECK
    senzu_status_text = ft.Text(value=f"{session.senzu_beans} / 3", size=14, weight=ft.FontWeight.BOLD, color="#FFFFFF")
    mode_status_text = ft.Text(value="Solo", size=14, weight=ft.FontWeight.BOLD, color="#FFB300")
    
    def use_bean_trigger(e):
        if session.use_senzu_bean():
            senzu_status_text.value = f"{session.senzu_beans} / 3"
            page.update()

    consumables_card = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.Column([ft.Text(value="𫳮 Senzu", size=12, color="#7A8B99"), senzu_status_text], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), on_click=use_bean_trigger),
                ft.Column([ft.Text(value="⚙️ Mode", size=12, color="#7A8B99"), mode_status_text], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column([ft.Text(value="⚔️ Core", size=12, color="#7A8B99"), ft.Text(value="Linked", size=14, weight=ft.FontWeight.BOLD, color="#59C3E6")], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        ),
        width=360, height=65, padding=5, bgcolor="#111C24", border_radius=4
    )

    # COMPONENT 5: DRAGON BALLS RADAR DOCK WITH DYNAMIC RENDERING
    def generate_radar_row():
        count = len(tome.data.get("dragon_balls", []))
        dots = []
        for i in range(DRAGON_BALL_MAX):
            if i < count:
                dots.append(ft.Text(value="●", size=20, color="#FF9100"))
            else:
                dots.append(ft.Text(value="○", size=20, color="#2A4354"))
        return ft.Row(controls=dots, alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    dragon_ball_dock = ft.Container(content=generate_radar_row(), width=360, height=50, padding=10, bgcolor="#0E171E", border_radius=4)

    # COMPONENT 6: DYNAMIC CONTAINER FOR INCOMING STACKED OBJECTIVES
    objective_stack_layout = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def build_objective_card(title: str, payout: int, desc: str):
        return ft.Container(
            content=ft.ExpansionTile(
                title=ft.Row(
                    controls=[
                        ft.Text(value=title, size=13, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        ft.Text(value=f"+{payout} pts", size=12, weight=ft.FontWeight.BOLD, color="#59C3E6")
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                controls=[
                    ft.Container(
                        content=ft.Text(value=desc, size=12, color="#A2B4C2"),
                        padding=ft.Padding(15, 5, 15, 15), alignment=ft.Alignment(-1, 0)
                    )
                ],
                collapsed_bgcolor="#16252F", bgcolor="#1A2D3A", icon_color="#59C3E6",
                shape=ft.RoundedRectangleBorder(radius=4), collapsed_shape=ft.RoundedRectangleBorder(radius=4)
            ),
            width=360, border_radius=4
        )

    # Confirmation Sub-Panel
    confirmation_panel = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.Text("CONFIRM SYNC", size=12, weight=ft.FontWeight.BOLD, color="#0B1116"), bgcolor="#00E676", width=165, height=40, border_radius=4, alignment=ft.Alignment(0, 0), on_click=lambda e: finish_stake(True)),
                ft.Container(content=ft.Text("ABORT SCAN", size=12, weight=ft.FontWeight.BOLD, color="#FFFFFF"), bgcolor="#D32F2F", width=165, height=40, border_radius=4, alignment=ft.Alignment(0, 0), on_click=lambda e: finish_stake(False))
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        width=360, visible=False
    )

    # COMPONENT 7: SYSTEM ACTION BUTTON & LIVE GENERATION LOGIC
    button_label = ft.Text(value="INITIALIZE HAKAI ENGINE", size=14, weight=ft.FontWeight.BOLD, color="#0B1116")
    
    def handle_hakai_click(e):
        button_label.value = "CONSULTING ORACLE FISH..."
        run_button.bgcolor = "#FFB300"
        page.update()
        
        # Capsule Corp Core Strategy: Randomly select batch target count (1 to 3 items)
        roll_count = random.choice([1, 2, 3])
        pending_cards["payloads"] = []
        objective_stack_layout.controls.clear()

        selected_game = random.choice(["The Division 2", "Fallout 76"])
        character_name_text.value = selected_game.upper()
        character_subtitle_text.value = f"Scan Result // Syncing {roll_count} Cards"

        for idx in range(roll_count):
            target_diff = random.choice(["Heated", "Hard"])
            card = oracle.generate_challenge(game=selected_game, difficulty=target_diff)
            
            if card and card.get("status") == "success":
                # Offset payouts appropriately if multi-rolled to keep macro stakes interesting
                if roll_count > 1:
                    card["base_payout"] = int(card["base_payout"] * 0.75)
                
                pending_cards["payloads"].append(card)
                
                # Append constructed component piece to the dynamic list
                card_title = f"Task {idx + 1}: {card['title']}"
                card_comp = build_objective_card(title=card_title, payout=card['base_payout'], desc=card['objective'])
                objective_stack_layout.controls.append(card_comp)
            else:
                character_name_text.value = "ERROR"
                character_subtitle_text.value = "Pipeline Blocked"
                err_comp = build_objective_card(title="Pipeline Interrupted", payout=0, desc="Check container environmental settings or active networking profiles.")
                objective_stack_layout.controls.append(err_comp)
                break

        run_button.visible = False
        confirmation_panel.visible = True
        page.update()

    def finish_stake(confirmed):
        run_button.visible = True
        confirmation_panel.visible = False
        cards = pending_cards["payloads"]
        
        if confirmed and cards:
            session.stake_missions(cards)
            max_diff = "Heated"
            if any(c["difficulty"] == "Hard" for c in cards):
                max_diff = "Hard"
                
            character_subtitle_text.value = f"Target Locked // System Active"
            dropped_star = calculate_dragon_ball_drop(max_diff, tome.data)
            
            if dropped_star:
                dragon_ball_dock.content = generate_radar_row()
                button_label.value = f"CORE ACTIVE // FOUND {dropped_star.upper()}!"
                run_button.bgcolor = "#FF9100"
            else:
                button_label.value = "HAKAI CORE ENGINE ACTIVE"
                run_button.bgcolor = "#00E676"
        else:
            character_name_text.value = "INES"
            character_subtitle_text.value = f"Hakai Level {tome.data['character_level']}"
            objective_stack_layout.controls.clear()
            button_label.value = "INITIALIZE HAKAI ENGINE"
            run_button.bgcolor = "#59C3E6"
        page.update()

    run_button = ft.Container(content=ft.Row(controls=[button_label], alignment=ft.MainAxisAlignment.CENTER), width=360, height=50, bgcolor="#59C3E6", border_radius=4, on_click=handle_hakai_click)

    page.navigation_bar = ft.NavigationBar(
        bgcolor="#0B1116", selected_index=0,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.PLAY_ARROW, label="Hakai"),
            ft.NavigationBarDestination(icon=ft.Icons.APPS, label="Capsule Corp"),
            ft.NavigationBarDestination(icon=ft.Icons.BOOK, label="Yemma's Tome")
        ]
    )

    scrollable_content = ft.Column(
        controls=[
            ft.Container(height=10), identity_header, mastery_card, character_card, consumables_card, dragon_ball_dock,
            ft.Container(height=5), run_button, confirmation_panel, objective_stack_layout, ft.Container(height=15)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, scroll=ft.ScrollMode.HIDDEN, expand=True
    )

    page.add(scrollable_content)
    page.update()

if __name__ == "__main__":
    ft.run(main, port=8550, view=ft.AppView.WEB_BROWSER)
