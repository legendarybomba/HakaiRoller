# 🎰 HakaiRoller

HakaiRoller is an automated gaming coach, a progress tracker, and a personalized achievement engine all rolled into one clean terminal screen.

Designed with a strict, hard target constraint (`MAX_WIDTH = 32`) for pristine readability on mobile viewports (like Termux on Android) or any standard desktop terminal.

---

## 🎯 The Primary Use Case

Think of this tool as an automated, arcade-style challenge manager for your gaming sessions. It eliminates "decision paralysis" by taking over your itinerary. It chooses the game, sets the stakes, tracks your accomplishments, and rolls everything into a unified progression system across your entire library.

---

## ⚙️ What it Does (The Functionality)

* **Session Tailoring:** Choose between solo, co-op, or double-feature session modes.
* **The Reel Spin:** A slot-machine style selector that chooses your target game based on smart, adaptive weights.
* **The Wild Card Deck:** Pull objective "cards" from the OracleFish API. Stack up to three challenges for higher difficulty and rewards.
* **The After-Action Report:** Log your completions to update your permanent profile.
* **The Escalation Engine:** Achieve a perfect run to trigger "Sudden Death Overtime"—a high-stakes finale with significant XP bonuses or penalties.
* **Dragon Radar:** Automatically tracks the collection of random, non-sequential Dragon Ball stars during mission completion. Once 7 are collected, access powerful passive buffs and level boosts via Shenron’s wish system.

---

## 🏎️ Under the Hood (In Plain English)

* **From Concept to Engine (DLM):** The evolution of Dynamic Library Management has arrived. By replacing fragmented, hardcoded text files with a unified persistence layer, the system now procedurally manages your gaming metadata, enabling a truly intelligent and reactive environment.
* **The Anti-Repetition Weight System:** Keeps a running memory of games played, dynamically adjusting spin odds to ensure your rotation never feels stale.
* **Calendar-Aware Multipliers:** Automatically boosts odds for specific games on their real-world weekly reset days.
* **Dragon Radar Logic:** A non-sequential collection engine that tracks rare drops across missions, allowing for thematic endgame progression without linear grinding.

---

## 📂 The Trinity Architecture

The heartbeat of the system. The **Trinity Architecture** is the convergence of three foundational pillars that define the `HakaiRoller` experience:

*   **Hakai (The Chaos):** The engine of volatility. It governs the random weights and the "Sudden Death" mechanics, ensuring the path forward is never stagnant and bad habits are routinely "destroyed."
*   **OracleFish (The Fate):** The herald of your path. It processes the library to forecast your challenges, providing the structure and objective destiny for each session.
*   **Yemma’s Tome (The Memory):** The persistence layer (`yemmas_tome.json`). This is the permanent record-keeper. It grounds the chaos of the engine and the prophecy of the Oracle into an immutable, verifiable reality, ensuring that your progress—and the stars you've collected—are never forgotten.

---

## 🤝 Credits & Inspiration

* **Dynamic Library Management (DLM) Concept:** Inspired by and developed in collaboration with [@theZoblin](https://github.com/theZoblin).
* **Development & Design:** DFC