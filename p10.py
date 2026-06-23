# FIRST and FOLLOW Calculation

grammar = {
    'E': ['TA'],
    'A': ['+TA', 'e'],
    'T': ['FB'],
    'B': ['*FB', 'e'],
    'F': ['(E)', 'i']
}

FIRST = {}
FOLLOW = {}

non_terminals = list(grammar.keys())

for nt in non_terminals:
    FIRST[nt] = set()
    FOLLOW[nt] = set()

FOLLOW['E'].add('$')  # Start symbol


def first(symbol):
    if symbol not in grammar:
        return {symbol}

    if FIRST[symbol]:
        return FIRST[symbol]

    result = set()

    for production in grammar[symbol]:
        if production == 'e':
            result.add('e')
        else:
            first_char = production[0]
            result.update(first(first_char))

    FIRST[symbol] = result
    return result


# Calculate FIRST
for nt in non_terminals:
    first(nt)

# Calculate FOLLOW
changed = True
while changed:
    changed = False

    for lhs in grammar:
        for production in grammar[lhs]:

            for i in range(len(production)):
                symbol = production[i]

                if symbol in grammar:

                    if i + 1 < len(production):
                        next_symbol = production[i + 1]

                        if next_symbol in grammar:
                            old = len(FOLLOW[symbol])

                            FOLLOW[symbol].update(
                                first(next_symbol) - {'e'}
                            )

                            if len(FOLLOW[symbol]) > old:
                                changed = True
                        else:
                            old = len(FOLLOW[symbol])

                            FOLLOW[symbol].add(next_symbol)

                            if len(FOLLOW[symbol]) > old:
                                changed = True

                    else:
                        old = len(FOLLOW[symbol])

                        FOLLOW[symbol].update(FOLLOW[lhs])

                        if len(FOLLOW[symbol]) > old:
                            changed = True

print("FIRST Sets")
for nt in non_terminals:
    print(f"FIRST({nt}) = {{ {', '.join(sorted(FIRST[nt]))} }}")

print("\nFOLLOW Sets")
for nt in non_terminals:
    print(f"FOLLOW({nt}) = {{ {', '.join(sorted(FOLLOW[nt]))} }}")