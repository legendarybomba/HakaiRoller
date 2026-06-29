# Project Hakai: Ginyu Scouter UI Dev Notes
**Last Updated:** June 2026
**Target Architecture:** Mobile Android Deployment (Standalone APK)
**Current Stable Layout Baseline:** Locked (`~/ginyu_scouter.py`)

---

## 📌 Current Status & Progress Core
We have successfully wireframed and compiled the full structural HUD UI for the Ginyu Scouter using a robust, container-focused design. Because the official Flet testing app introduced fatal client-compiler translation mismatches over version-specific styling parameters, we abandoned the app completely and pivoted to direct **Local Web Browser Rendering (`http://127.0.0.1:8550`)** via Termux. 

### Completed UI Layout Stack (Stacked Vertically):
1. **Identity Header:** Displays Player Gamertag (`LEGENDBOMBA#3129`) aligned next to a hardcoded text-glyph star (`★`) to bypass standard icon initialization faults.
2. **Mastery Rank Card (Block 2/1):** Displays progression metrics, custom string insignia dividers (`║█║`), and a nested double-container green horizontal XP bar.
3. **Character Portrait Card (Block 3/1 & 4/1):** Built a high-density panel framing structural character level texts and a tactical central bracket layout placeholder (`[ ❖ ]`).
4. **Consumables Deck (Section 5):** Establishes an explicit grid layout row mapping Senzu Beans, Vetos, and the core linked system branch.
5. **Dragon Ball Radar Dock:** Features a horizontal array tracking seven tracking spheres, setting up an active status layout baseline.
6. **Hakai Engine Trigger:** Implemented a full-width interactive container button completely stripped of standard material-button keyword requirements.
7. **Persistent Viewport Footer Nav:** Deployed a sticky Material 3 bottom menu mapped with universal string literals (`play_arrow`, `apps`, `book`) for future panel switching.

---

## ⚡ The Saiyan Blueprint (Rules for Exportable APKs)
To ensure this UI doesn't just work on a local Termux server, but cleanly compiles into a standalone, distributable **APK file** for other players using `flet build apk`, the code must strictly adhere to the following guardrails:

### 1. The Zero-Local-Asset Mandate
* **The Problem:** Referencing hardcoded local paths (e.g., `~/ProjectHakai/assets/...`) will cause instant compilation failure or application crashes on destination devices because those file directories only exist on our training machine.
* **The Solution:** Rely exclusively on native character text-glyphs or use remote, web-hosted image configurations (`src="https://raw.githubusercontent.com/.../image.png"`) pulled dynamically over the network.

### 2. Control Parameter Flattening
* Older backend environments (like `0.85.3`) and mobile compiler wrappers frequently mismatch on modern nested helper properties (e.g., `ft.border.all` or `ft.icons.STAR_PURPLE`). 
* Keep the code completely bulletproof by using layout rows/columns, explicit string variables for symbols, and standard flat layout arguments.

### 3. Decouple Layout from Engine Logic
* The main UI rendering loop must act entirely as a visual terminal shell. All randomization engines, game selection logic, and backend database queries should live inside a separate Python file, imported dynamically into the interface button click hooks (`on_click`).

---

## 📅 Next Development Phases
* **Phase 1: Dynamic Variable Binding:** Convert hardcoded UI display string values into flexible variables to accept real-time backend updates.
* **Phase 2: Panel State Interactivity:** Wire up the footer navigation bar to dynamically swap out the active central layout column when switching between the main engine, Capsule Corp inventory, and King Yemma's data logs.
* **Phase 3: Logic Engine Merge:** Inject the randomized game engine scripts into the primary layout trigger events.
