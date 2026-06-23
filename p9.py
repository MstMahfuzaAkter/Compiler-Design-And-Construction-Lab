import copy
from collections import defaultdict

EPSILON = 'ε'

class AmbiguityHandler:
    def __init__(self, grammar: dict, start_symbol: str):
        self.grammar = copy.deepcopy(grammar)
        self.start = start_symbol
        self.non_terminals = set(grammar.keys())

    def has_direct_left_recursion(self):
        for nt, prods in self.grammar.items():
            for prod in prods:
                if prod and prod[0] == nt:
                    return True
        return False

    def has_indirect_left_recursion(self):
        def can_start_with(nt, target, visited=None):
            if visited is None:
                visited = set()
            if nt in visited:
                return False
            visited.add(nt)
            for prod in self.grammar.get(nt, []):
                if not prod or prod == [EPSILON]:
                    continue
                first_sym = prod[0]
                if first_sym == target:
                    return True
                if first_sym in self.non_terminals:
                    if can_start_with(first_sym, target, visited.copy()):
                        return True
            return False

        for nt in self.non_terminals:
            if can_start_with(nt, nt):
                return True
        return False

    def has_common_prefix(self):
        for nt, prods in self.grammar.items():
            prefixes = [prod[0] for prod in prods if prod and prod != [EPSILON]]
            if len(prefixes) != len(set(prefixes)):
                return True
        return False

    def is_ambiguous(self):
        reasons = []
        if self.has_direct_left_recursion():
            reasons.append("direct left recursion")
        if self.has_indirect_left_recursion():
            reasons.append("indirect left recursion")
        if self.has_common_prefix():
            reasons.append("common prefixes (not left-factored)")
        return bool(reasons), reasons

    def remove_left_recursion(self):
        g = copy.deepcopy(self.grammar)
        nts = list(g.keys())
        counter = {}

        def new_nt(base):
            prime = base + "'"
            count = counter.get(base, 0) + 1
            counter[base] = count
            return prime if count == 1 else prime + str(count)

        for i, Ai in enumerate(nts):
            for j in range(i):
                Aj = nts[j]
                new_prods = []
                for prod in g[Ai]:
                    if prod and prod[0] == Aj:
                        for aj_prod in g[Aj]:
                            if aj_prod == [EPSILON]:
                                new_prods.append(prod[1:] if len(prod) > 1 else [EPSILON])
                            else:
                                new_prods.append(aj_prod + prod[1:])
                    else:
                        new_prods.append(prod)
                g[Ai] = new_prods

            alpha_list = []
            beta_list = []
            for prod in g[Ai]:
                if prod and prod[0] == Ai:
                    alpha_list.append(prod[1:] if len(prod) > 1 else [EPSILON])
                else:
                    beta_list.append(prod)

            if alpha_list:
                Ai_prime = new_nt(Ai)
                g[Ai] = [b + [Ai_prime] for b in beta_list] if beta_list else [[Ai_prime]]
                g[Ai_prime] = [a + [Ai_prime] for a in alpha_list] + [[EPSILON]]
                nts.append(Ai_prime)
                self.non_terminals.add(Ai_prime)
        return g

    def left_factor(self, grammar=None):
        if grammar is None:
            grammar = copy.deepcopy(self.grammar)
        changed = True
        counter = {}

        def new_nt(base):
            prime = base + "'"
            count = counter.get(base, 0) + 1
            counter[base] = count
            return prime if count == 1 else prime + str(count)

        while changed:
            changed = False
            new_grammar = {}
            for nt, prods in list(grammar.items()):
                groups = defaultdict(list)
                no_prefix = []
                for prod in prods:
                    if prod and prod != [EPSILON]:
                        groups[prod[0]].append(prod)
                    else:
                        no_prefix.append(prod)
                
                new_prods = list(no_prefix)
                for prefix, group in groups.items():
                    if len(group) == 1:
                        new_prods.append(group[0])
                    else:
                        lcp = group[0]
                        for g_prod in group[1:]:
                            i = 0
                            while i < len(lcp) and i < len(g_prod) and lcp[i] == g_prod[i]:
                                i += 1
                            lcp = lcp[:i]
                        
                        if len(lcp) == 0:
                            new_prods.extend(group)
                        else:
                            nt_prime = new_nt(nt)
                            new_prods.append(lcp + [nt_prime])
                            remainders = [p[len(lcp):] or [EPSILON] for p in group]
                            new_grammar[nt_prime] = remainders
                            changed = True
                new_grammar[nt] = new_prods
            
            for k, v in grammar.items():
                if k not in new_grammar:
                    new_grammar[k] = v
            grammar = new_grammar
        return grammar

    def process(self):
        ambiguous, reasons = self.is_ambiguous()
        print("=" * 55)
        print(" CFG Ambiguity Analysis")
        print("=" * 55)
        print("\n Original Grammar:")
        self._print_grammar(self.grammar)
        
        if not ambiguous:
            print("\n Grammar is UNAMBIGUOUS. No transformation needed.")
            return self.grammar
            
        print(f"\n Grammar is AMBIGUOUS!")
        print(" Reasons detected:")
        for r in reasons:
            print(f" • {r}")
            
        print("\n Step 1 → Removing Left Recursion...")
        no_lr = self.remove_left_recursion()
        self._print_grammar(no_lr)
        
        print("\n Step 2 → Applying Left Factoring...")
        factored = self.left_factor(no_lr)
        print(" Final Unambiguous Grammar:")
        self._print_grammar(factored)
        print("=" * 55)
        return factored

    def _print_grammar(self, grammar):
        for nt in sorted(grammar.keys()):
            prods = grammar[nt]
            prod_strs = [" ".join(p) if p != [EPSILON] else EPSILON for p in prods]
            print(f" {nt} → {' | '.join(prod_strs)}")

if __name__ == "__main__":
    ambiguous_grammar = {
        'E': [['E', '+', 'E'], ['E', '*', 'E'], ['(', 'E', ')'], ['id']],
    }
    handler = AmbiguityHandler(ambiguous_grammar, start_symbol='E')
    handler.process()