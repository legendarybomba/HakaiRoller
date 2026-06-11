# 🎰 HakaiRoller

HakaiRoller is an automated gaming coach, a progress tracker, and a personalized achievement engine all rolled into one clean terminal screen.

Designed with a strict, hard target constraint (`MAX_WIDTH = 32`) for pristine readability on mobile viewports (like Termux on Android) or any standard desktop terminal.

---

## 🎯 The Primary Use Case

Think of this tool as an automated, arcade-style challenge manager for your gaming sessions. If you have ever opened up your game library, stared at the screen, and had no idea what to play or what to do, this tool fixes that. It eliminates "decision paralysis" by completely taking over your itinerary. It chooses the game, sets the stakes, tracks your accomplishments, and rolls everything into a unified progression system across your entire library.

---

## ⚙️ What it Does (The Functionality)

When you boot it up, you aren't just getting a basic random picker. You are stepping into an interactive game loop:

* **Session Tailoring:** You tell it the vibe. Are you playing solo or with a co-op squad? Is it a chill night, a sweaty challenge night, or a massive double feature?
* **The Reel Spin:** The tool simulates a slot-machine style reel spin, locking onto a target game from your library using custom, smart logic.
* **The Wild Card Deck:** Once a game is locked, it deals you an objective "card" (e.g., an Easy daily bounty or a Hard endgame boss clear). You can choose to accept it or "double down" by stacking up to three challenge cards at once for massive rewards.
* **The After-Action Report:** After you finish streaming or playing, you open the debrief log. You manually mark whether you cleared or skipped your objectives, and the tool dynamically tallies up your session score.
* **The Escalation Engine:** If you pull off a perfect run, the tool detects it and throws you into "Sudden Death Overtime." It forces a high-stakes finale card where clears are worth massive bonus points, but a failure actually docks points from your permanent record.

---

## 🏎️ Under the Hood (In Plain English)

While it looks like a retro terminal game, there is a lot of hidden math making sure your experience stays fresh:

* **The Anti-Repetition Weight System:** The tool keeps a running memory of what you’ve played. Games you play frequently naturally lose "weight" on the wheel, while games you haven't touched in a while get a massive statistical boost. It guarantees your rotation never feels stale.
* **Calendar-Aware Multipliers:** It knows what day of the week it is. If a specific game has real-world weekly resets or community events on a Tuesday or Thursday, the internal math automatically triples its chances of winning the reel spin on those days.
* **Self-Healing Diagnostics:** Every single time it starts up, it silently scans your phone's storage. If a critical save file or objective deck is missing or accidentally deleted, it instantly rebuilds it from scratch behind the scenes before you even see the main menu, preventing crashes.

---

## 📂 The Ecosystem (Local Storage)

HakaiRoller manages everything locally using four simple text files:

* `game_history.txt` — Chronological log of games played to feed the weight system.
* `achievements.txt` — The master deck holding your game-specific objectives.
* `completed_achievements.txt` — Tracks retired challenges to prevent repeats.
* `gamer_profile.txt` — Keeps a permanent record of your Total Gamer Score.

---

## 🔮 On The Horizon: Dynamic Library Management (DLM)

We are currently architecturalizing an AI-driven evolution to replace hardcoded text decks with **Dynamic Library Management**. Leveraging the Gemini API, HakaiRoller will soon procedurally generate lore-accurate, difficulty-calibrated objectives on the fly whenever games are dynamically injected into or removed from the matrix.

---

## 🤝 Credits & Inspiration

* **Dynamic Library Management (DLM) Concept:** Inspired by and developed in collaboration with [@theZoblin](https://github.com/theZoblin).
* **Development & Design:** DFC
