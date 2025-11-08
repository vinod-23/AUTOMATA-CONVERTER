from collections import defaultdict
from visualizer import state_to_str

def epsilon_closure(nfa, states):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        for nxt in nfa.get(state, {}).get("", []):
            if nxt not in closure:
                closure.add(nxt)
                stack.append(nxt)
    return frozenset(closure)

def move(nfa, states, symbol):
    result = set()
    for state in states:
        result.update(nfa.get(state, {}).get(symbol, []))
    return frozenset(result)

def nfa_to_dfa(nfa, start, finals, symbols):
    start_closure = epsilon_closure(nfa, [start])
    dfa_trans = {}
    unmarked = [start_closure]
    dfa_finals = set()
    visited = set()

    while unmarked:
        current = unmarked.pop()
        if current in visited:
            continue
        visited.add(current)

        dfa_trans[current] = {}
        for sym in symbols:
            if sym == "": 
                continue
            target = epsilon_closure(nfa, move(nfa, current, sym))
            if target:
                dfa_trans[current][sym] = target
                if target not in visited:
                    unmarked.append(target)

        if any(s in finals for s in current):
            dfa_finals.add(current)

    # Convert all sets to stringified labels for visualization
    clean_trans = {}
    for s, edges in dfa_trans.items():
        clean_trans[state_to_str(s)] = {}
        for sym, dst in edges.items():
            clean_trans[state_to_str(s)][sym] = state_to_str(dst)

    return clean_trans, state_to_str(start_closure), [state_to_str(s) for s in dfa_finals]
