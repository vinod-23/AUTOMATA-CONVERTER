from visualizer import state_to_str

def minimize_dfa(transitions, start_state, final_states):
    """
    DFA minimization using Myhill–Nerode theorem.
    Indistinguishable states are merged.
    Missing transitions (dead states) are ignored.
    """

    # Step 1️⃣: Collect all states and input symbols
    states = list(transitions.keys())
    symbols = sorted({sym for edges in transitions.values() for sym in edges.keys()})

    # Step 2️⃣: Initialize partitions — final vs non-final states
    final_partition = set(final_states)
    non_final_partition = set(s for s in states if s not in final_partition)
    partitions = [final_partition, non_final_partition]

    changed = True
    while changed:
        changed = False
        new_partitions = []

        for group in partitions:
            refined = {}

            for state in group:
                # Determine which partition each transition leads to
                signature = []
                for sym in symbols:
                    next_state = transitions[state].get(sym, None)
                    # Find which partition the next_state belongs to
                    idx = None
                    for i, part in enumerate(partitions):
                        if next_state in part:
                            idx = i
                            break
                    signature.append(idx)

                signature = tuple(signature)

                # Group states with same transition pattern
                if signature not in refined:
                    refined[signature] = set()
                refined[signature].add(state)

            # If group splits, flag change
            if len(refined) > 1:
                changed = True

            new_partitions.extend(refined.values())

        partitions = new_partitions

    # Step 3️⃣: Build minimized DFA
    new_states = [frozenset(group) for group in partitions]
    new_trans = {}
    new_start = None
    new_finals = []

    for group in new_states:
        representative = next(iter(group))
        new_state_name = state_to_str(group)
        new_trans[new_state_name] = {}

        for sym in symbols:
            next_state = transitions[representative].get(sym, None)
            if next_state is None:
                continue  # Skip missing transitions
            for g in new_states:
                if next_state in g:
                    new_trans[new_state_name][sym] = state_to_str(g)
                    break

        if representative == start_state:
            new_start = new_state_name
        if representative in final_states:
            new_finals.append(new_state_name)

    return new_trans, new_start, new_finals
