import graphviz
import os

def state_to_str(state):
    """Convert frozenset or set to readable string."""
    if isinstance(state, (set, frozenset)):
        return "{" + ",".join(sorted(map(str, state))) + "}"
    return str(state)

def visualize_dfa(transitions, start_state, final_states, filename="DFA"):
    """Generate and save DFA visualization."""
    dot = graphviz.Digraph(comment="Deterministic Finite Automaton")

    for state in transitions:
        shape = "doublecircle" if state in final_states else "circle"
        dot.node(state_to_str(state), shape=shape)

    for src, edges in transitions.items():
        for symbol, dst in edges.items():
            dot.edge(state_to_str(src), state_to_str(dst), label=symbol)

    dot.node("", shape="none")
    dot.edge("", state_to_str(start_state))

    output_path = dot.render(filename, format="png", cleanup=True)
    final_name = filename + ".png"
    if os.path.exists(output_path):
        os.rename(output_path, final_name)
    return final_name
