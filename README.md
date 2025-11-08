# Automata Converter & Minimizer (NFA -> DFA -> Minimize) with Streamlit GUI

## What is included
- `main.py` : Streamlit application (GUI)
- `nfa_to_dfa.py` : NFA and DFA classes and conversion logic
- `dfa_minimizer.py` : DFA minimization (Hopcroft-like partition refinement) and simulator
- `visualizer.py` : Graphviz-based PNG generation for automata diagrams
- `dfa_animator.py` : Generates frame-by-frame PNGs and stitches them into a GIF using imageio
- `requirements.txt` : Python dependencies

## Quick Setup (step-by-step)
1. Install Python 3.8+ (recommended).
2. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Graphviz system package from https://graphviz.org/download/
   - Add Graphviz `bin` folder to your PATH so graphviz executables are available.
4. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```
5. Open `http://localhost:8501` in your browser.

## How to use the app
1. Define states, alphabet, start state, final states and transitions.
2. Click **Convert to DFA** — the app shows the DFA and a download button for PNG.
3. Click **Minimize DFA** — the app shows minimized DFA and download button.
4. Use **Simulate Input String** to enter a string, simulate it, view trace and an animation GIF, and download the GIF.

## Notes & Tips
- Transitions format: `SOURCE,SYMBOL=DEST1,DEST2` one per line. Example: `q0,a=q0,q1`
- DFA states are displayed as `{q0,q1}` (sets) when necessary.
- If Graphviz is not in PATH, visualization will fail — ensure system installation.
- Frames for GIF are saved to a `frames/` folder when animations are generated.
