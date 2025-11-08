import streamlit as st
from nfa_to_dfa import nfa_to_dfa
from dfa_minimizer import minimize_dfa
from visualizer import visualize_dfa

st.set_page_config(page_title="Automata Converter & Minimizer", page_icon="🤖")

st.title("Automata Converter and Minimizer")
st.caption("Enter your NFA or DFA transition table below to visualize and minimize automata.")

# -------------------------------------------------------------------------
# 🔹 INPUT SECTION
# -------------------------------------------------------------------------
st.subheader("1️⃣ Enter Automaton Transitions")

automaton_input = st.text_area(
    "Enter NFA or DFA transitions (Python dictionary format):",
    value="{ 'q0': {'0': ['q0','q1'], '1': ['q0']}, 'q1': {'0': ['q2']}, 'q2': {'0': ['q2'], '1': ['q2']} }"
)

start_state = st.text_input("Start State", value="q0")
final_states = st.text_input("Final States (comma separated)", value="q2").replace(" ", "").split(",")
symbols = st.text_input("Input Symbols (comma separated)", value="0,1").replace(" ", "").split(",")

st.divider()

# -------------------------------------------------------------------------
# 🔹 DETECT AUTOMATON TYPE (NFA or DFA)
# -------------------------------------------------------------------------
def is_dfa(automaton):
    """Checks if automaton is deterministic (DFA)."""
    for state, transitions in automaton.items():
        for sym, nexts in transitions.items():
            # If transition has multiple next states, it’s NFA
            if isinstance(nexts, list) and len(nexts) > 1:
                return False
    return True

# -------------------------------------------------------------------------
# 🔹 USER INPUT PARSING
# -------------------------------------------------------------------------
try:
    automaton = eval(automaton_input)  # Convert string → Python dict
    if not isinstance(automaton, dict):
        st.error("❌ Input must be a dictionary structure.")
    else:
        # Detect automaton type
        automaton_type = "DFA" if is_dfa(automaton) else "NFA"
        st.info(f"✅ Detected automaton type: **{automaton_type}**")

        # -----------------------------------------------------------------
        # CASE 1️⃣: DFA entered → Show Minimize Button immediately
        # -----------------------------------------------------------------
        if automaton_type == "DFA":
            if st.button("🧩 Minimize DFA (Direct)"):
                try:
                    min_dfa, min_start, min_finals = minimize_dfa(automaton, start_state, final_states)
                    st.success("✅ DFA minimized successfully!")
                    st.json(min_dfa)

                    img_path = visualize_dfa(min_dfa, min_start, min_finals, filename="Minimized_DFA")
                    st.image(img_path, caption="Minimized DFA", use_container_width=True)

                except Exception as e:
                    st.error(f"❌ Error minimizing DFA: {e}")

        # -----------------------------------------------------------------
        # CASE 2️⃣: NFA entered → Show Convert Button first
        # -----------------------------------------------------------------
        else:
            if st.button("🔁 Convert NFA → DFA"):
                try:
                    dfa, dfa_start, dfa_finals = nfa_to_dfa(automaton, start_state, final_states, symbols)
                    st.session_state['dfa_data'] = (dfa, dfa_start, dfa_finals)

                    st.success("✅ NFA successfully converted to DFA!")
                    st.json(dfa)

                    img_path = visualize_dfa(dfa, dfa_start, dfa_finals, filename="DFA")
                    st.image(img_path, caption="Converted DFA", use_container_width=True)

                except Exception as e:
                    st.error(f"❌ Error converting NFA: {e}")


            # -----------------------------------------------------------------
            # Minimize only after DFA is generated
            # -----------------------------------------------------------------
            if 'dfa_data' in st.session_state:
                if st.button("🧩 Minimize Converted DFA"):
                    try:
                        dfa, dfa_start, dfa_finals = st.session_state['dfa_data']
                        min_dfa, min_start, min_finals = minimize_dfa(dfa, dfa_start, dfa_finals)
                        st.success("✅ DFA minimized successfully!")
                        st.json(min_dfa)

                        img_path = visualize_dfa(min_dfa, min_start, min_finals, filename="Minimized_DFA")
                        st.image(img_path, caption="Minimized DFA", use_container_width=True)

                    except Exception as e:
                        st.error(f"❌ Error minimizing DFA: {e}")

except Exception as e:
    st.error(f"⚠️ Invalid automaton input: {e}")
