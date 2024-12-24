# Regular Expression to NFA Converter

This project implements a Python program to convert a given regular expression into a Non-deterministic Finite Automaton (NFA). The tool supports various regex operators, including `|` (alternation), `*` (Kleene star), `+` (one or more repetitions), and `()` parentheses for grouping.

## Features
- Converts regular expressions into NFA transition diagrams.
- Supports the following regex operators:
  - `|`: Alternation (e.g., `a|b` matches `a` or `b`).
  - `*`: Kleene star (e.g., `a*` matches zero or more `a`'s).
  - `+`: One or more repetitions (e.g., `a+` matches one or more `a`'s).
  - Parentheses for grouping (e.g., `(a|b)c`).
- Generates a visual representation of the NFA as a transition diagram.

## Requirements
- Python 3.7 or later
- Libraries:
  - `graphviz` (for generating transition diagrams)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/saelthorn/regex-nfa.git
   cd regex-to-nfa
   ```
2. Install the required libraries:
   ```bash
   pip install graphviz
   ```

## Usage
1. Create or modify a Python script to define your regular expression:
   ```python

   regex = "(a|b)+c"
   nfa = RegexNFA(regex)
   _build_nfa()
   visualize(output_file="regex_nfa")
   ```
2. Run the script:
   ```
   python main.py
   ```
3. View the generated `regex_nfa.png` file to see the transition diagram of the NFA.


## Example
### Input
Regular expression: `(a|b)+c`

### Output
Transition Diagram:

![NFA Diagram](nfa_diagram.png)

### Explanation
1. Start with the initial state `q0`.
2. Handle alternation `(a|b)` using epsilon transitions.
3. Apply the `+` operator to create a loop for `a` and `b`.
4. Add a transition for `c` leading to the accept state.

## File Structure
- `regex_to_nfa.py`: Contains the main logic for converting regular expressions to NFAs.
- `README.md`: Documentation for the project.
- `requirements.txt`: Lists required Python libraries.

## Future Improvements
- Optimization of the NFA to minimize states.
- Conversion of NFA to DFA.



