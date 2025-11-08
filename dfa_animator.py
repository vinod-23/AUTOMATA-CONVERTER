import graphviz
from visualizer import state_to_str

def generate_dfa_frame(transitions, start_state, final_states, current_state=None, filename="frame"):
    dot = graphviz.Digraph()

    for state in transitions:
        shape = "doublecircle" if state in final_states else "circle"
        color = "lightblue" if state == current_state else "white"
        dot.node(state_to_str(state), shape=shape, style="filled", fillcolor=color)

    for src, edges in transitions.items():
        for sym, dst in edges.items():
            dot.edge(state_to_str(src), state_to_str(dst), label=sym)

    dot.node("", shape="none")
    dot.edge("", state_to_str(start_state))

    dot.render(filename, format="png", cleanup=True)
