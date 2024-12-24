import graphviz

class RegexNFA:
    def __init__(self, pattern):
        self.pattern = pattern
        self.states = set()
        self.transitions = {}
        self.start_state = 'q0'
        self.accept_states = set()
        self._build_nfa()

    def _build_nfa(self):
        # Initialize
        self.states = {self.start_state}
        self.transitions = {self.start_state: {}}
        self.accept_states.clear()

        def create_state():
            new_state = f'q{len(self.states)}'
            self.states.add(new_state)
            self.transitions[new_state] = {}
            return new_state

        def process_alternative(alt, start_state):
            current_state = start_state
            alt_states = []  # To handle alternation branches
            i = 0
            while i < len(alt):
                char = alt[i]

                if char == '(':
                    # Find matching parenthesis
                    depth = 1
                    j = i + 1
                    while j < len(alt) and depth > 0:
                        if alt[j] == '(':
                            depth += 1
                        elif alt[j] == ')':
                            depth -= 1
                        j += 1

                    # Process subpattern
                    subpattern = alt[i+1:j-1]
                    new_state = create_state()

                    # Add epsilon transition
                    if 'ε' not in self.transitions[current_state]:
                        self.transitions[current_state]['ε'] = set()
                    self.transitions[current_state]['ε'].add(new_state)

                    current_state = process_alternative(subpattern, new_state)

                    # Check for Kleene star or '+' operator
                    if j < len(alt) and (alt[j] == '*' or alt[j] == '+'):
                        repeat_state = create_state()

                        if alt[j] == '*':
                            # Add epsilon transitions for Kleene star
                            if 'ε' not in self.transitions[current_state]:
                                self.transitions[current_state]['ε'] = set()
                            self.transitions[current_state]['ε'].add(repeat_state)  # Move to repeat state
                            self.transitions[current_state]['ε'].add(new_state)   # Can repeat the subpattern

                        elif alt[j] == '+':
                            # Add epsilon transitions for '+' (at least one occurrence)
                            if 'ε' not in self.transitions[current_state]:
                                self.transitions[current_state]['ε'] = set()
                            self.transitions[current_state]['ε'].add(repeat_state)  # Move to repeat state

                        # Add a loop back to the subpattern
                        if 'ε' not in self.transitions[repeat_state]:
                            self.transitions[repeat_state]['ε'] = set()
                        self.transitions[repeat_state]['ε'].add(new_state)

                        current_state = repeat_state
                        j += 1

                    i = j

                elif char == '|':
                    # Split for alternation
                    branch_state = create_state()
                    if 'ε' not in self.transitions[start_state]:
                        self.transitions[start_state]['ε'] = set()
                    self.transitions[start_state]['ε'].add(branch_state)

                    # Process the rest of the alternative in a new branch
                    alt_states.append(process_alternative(alt[i+1:], branch_state))
                    break  # Exit loop to complete processing of other branches
                
                elif char == '*':
                    # Kleene star for the previous character
                    prev_char = alt[i-1]
                    star_state = create_state()

                    # Add self-loop for the character
                    if prev_char not in self.transitions[current_state]:
                        self.transitions[current_state][prev_char] = set()
                    self.transitions[current_state][prev_char].add(current_state)

                    # Add epsilon transition to new state
                    if 'ε' not in self.transitions[current_state]:
                        self.transitions[current_state]['ε'] = set()
                    self.transitions[current_state]['ε'].add(star_state)

                    current_state = star_state
                    i += 1

                elif char == '+':
                    # '+' operator for the previous character
                    prev_char = alt[i-1]
                    plus_state = create_state()

                    # Add a transition for the character
                    if prev_char not in self.transitions[current_state]:
                        self.transitions[current_state][prev_char] = set()
                    self.transitions[current_state][prev_char].add(plus_state)

                    # Add a loop back to allow repetition
                    if 'ε' not in self.transitions[plus_state]:
                        self.transitions[plus_state]['ε'] = set()
                    self.transitions[plus_state]['ε'].add(current_state)

                    current_state = plus_state
                    i += 1

                else:
                    # Regular character
                    new_state = create_state()
                    if char not in self.transitions[current_state]:
                        self.transitions[current_state][char] = set()
                    self.transitions[current_state][char].add(new_state)
                    current_state = new_state
                    i += 1

            # If there are alternation branches, connect them
            for alt_state in alt_states:
                if 'ε' not in self.transitions[alt_state]:
                    self.transitions[alt_state]['ε'] = set()
                self.transitions[alt_state]['ε'].add(current_state)

            # Mark final state as accept state
            self.accept_states.add(current_state)
            return current_state


        # Build NFA
        process_alternative(self.pattern, self.start_state)

    def visualize(self):
        dot = graphviz.Digraph(comment='Regex NFA')
        dot.attr(rankdir='LR')

        # Nodes
        for state in self.states:
            if state == self.start_state:
                dot.node(state, state, shape='circle', style='filled', color='green')
            elif state in self.accept_states:
                dot.node(state, state, shape='doublecircle', style='filled', color='red')
            else:
                dot.node(state, state, shape='circle')

        # Edges
        for from_state, transitions in self.transitions.items():
            for symbol, to_states in transitions.items():
                for to_state in to_states:
                    dot.edge(from_state, to_state, label=symbol)

        # Render
        dot.render('regex_nfa', format='png', cleanup=True)
        print("NFA visualization saved as regex_nfa.png")

def main():
    pattern = input("Enter pattern (use * for Kleene star, () for grouping, | for alternation: ") 
    
    nfa = RegexNFA(pattern)
    nfa.visualize()
    
if __name__ == "__main__":
    main()