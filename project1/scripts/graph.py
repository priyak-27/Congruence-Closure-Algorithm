import networkx as nx
from pyvis.network import Network
import webbrowser
import os
import time
import sys
from cc import *


class ResetException(Exception):
    pass

class CongruenceGraphVisualizer:
    def __init__(self, l_ineq, r_ineq, wait):
        self.l_ineq, self.r_ineq = l_ineq, r_ineq
        self.graph = nx.Graph()
        self.html_file = "congruence_graph.html"
        self.browser_opened = False
        self.auto_refresh = True
        self.message = ""
        self.wait = wait
        self.fixed_positions = {}  # Store fixed positions for nodes so it does not change.

    def add_constraint(self, t1, t2, color = "black"):
        self.graph.add_edge(t1, t2, color=color)
        self.show_graph()

    def calculate_fixed_positions(self):
        """
        Calculate positions for the nodes in the graph and fix them.
        """
        pos = nx.spring_layout(self.graph, seed=42, scale=300)  # Reduce scale to bring nodes closer
        self.fixed_positions = {node: (pos[node][0], pos[node][1]) for node in pos}

    def show_graph(self):
        net = Network(height="750px", width="100%", notebook=False)

        # Add nodes and edges
        net.from_nx(self.graph)

        # Apply fixed positions
        for node in net.nodes:
            if node["id"] in self.fixed_positions:
                x, y = self.fixed_positions[node["id"]]
                node["x"] = x
                node["y"] = y
                node["fixed"] = {"x": True, "y": True}
                node["font"] = {"size": 20}  # Increase font size
                node["size"] = 20  # Increase node size for better visibility

        # Disable physics to keep positions static
        net.set_options("""
            var options = {
                "physics": {
                    "enabled": false
                }
            }
        """)

        net.write_html(self.html_file)

        with open(self.html_file, "r") as f:
            content = f.read()

        message_div = f'<div id="message" style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%); background-color: rgba(255,255,255,0.8); padding: 10px; border-radius: 5px; z-index: 1000;">{self.message}</div>'
        content = content.replace('<body>', f'<body>{message_div}')

        if self.auto_refresh:
            refresh_script = '''
            <script>
                setTimeout(() => {
                    window.location.reload();
                }, ''' + str(self.wait/2 * 1000) + ''');
            </script>
            '''
            content = content.replace('</body>', f'{refresh_script}</body>')

        with open(self.html_file, "w") as f:
            f.write(content)

        if not self.browser_opened:
            webbrowser.open(f"file://{os.path.abspath(self.html_file)}")
            self.browser_opened = True

    def visualize_equivalence_classes(self, eq_list):
        for eq_class in eq_list:
            for term in eq_class:
                self.graph.add_node(term, title=f"Class: {eq_class[0]}")
            for term1, term2 in zip(eq_class, eq_class[1:]):
                self.graph.add_edge(term1, term2)
        self.auto_refresh = False
        self.show_graph()

    def update_message(self, message):
        self.message = message
        self.show_graph()

def congruence_closure(eq_classes, clauses_dict, v=False, wait=2):
    left_ineq, right_ineq = clauses_dict[-1]
    clauses_dict.pop(-1)

    if v: print("1", eq_classes)

    eq_list = [list(dict.fromkeys(eq_class)) for eq_class in eq_classes]
    terms = [t[0] for t in eq_list]

    visualizer = CongruenceGraphVisualizer(left_ineq, right_ineq, wait)
    for t in terms:
        visualizer.graph.add_node(t, color=("red" if t in (left_ineq, right_ineq) else "blue"))

    # Calculate and fix positions
    visualizer.calculate_fixed_positions()
    visualizer.show_graph()

    def find_class(term):
        return next((c for c in eq_list if term in c), None)

    def merge_classes(class1, class2):
        new_class = list(dict.fromkeys(class1 + class2))
        eq_list.remove(class1)
        eq_list.remove(class2)
        eq_list.append(new_class)

    changed = True
    while changed:
        changed = False
        for clauses in sorted(clauses_dict.values()):
            term1, term2 = sorted(clauses)
            class1 = find_class(term1)
            class2 = find_class(term2)
            if class1 != class2:
                if v: print("clause:", clauses, term1, term2)
                if v: print("merging...", eq_list)
                merge_classes(class1, class2)
                if v: print("merged:", eq_list)
                changed = True
                visualizer.add_constraint(term1, term2, "orange") 
                visualizer.update_message(f"Merging classes containing {term1} and {term2}")
                time.sleep(wait)
                
        left_class = find_class(left_ineq)
        right_class = find_class(right_ineq)

        if left_class is not None and right_class is not None and left_class == right_class:
            visualizer.update_message("Result: UNSAT")
            return "UNSAT" 

        try:
            for eq_class in eq_list:
                for term in eq_class.copy():
                    for term2 in terms:
                        if term2 != term and term2 in term:
                            class2 = find_class(term2)
                            if class2 != eq_class:
                                for term3 in class2:
                                    if term3 != term2:
                                        new_term = term.replace(term2, term3)
                                        visualizer.update_message(f"Considering merging {term} and {new_term} by replacing {term2} with {term3}")    
                                        time.sleep(wait)
                                        if new_term in terms:
                                            time.sleep(wait)
                                            if new_term not in eq_class:
                                                class3 = find_class(new_term)
                                                merge_classes(eq_class, class3)
                                                visualizer.add_constraint(term, new_term)
                                                visualizer.update_message(f"Merging {term} and {new_term}") 
                                                time.sleep(wait)
                                                raise ResetException()
                                        else:
                                            visualizer.update_message(f"{new_term} not in terms list") 
                                            time.sleep(wait)
        except ResetException:
            pass

        left_class = find_class(left_ineq)
        right_class = find_class(right_ineq)

        #visualizer.auto_refresh = False
        visualizer.show_graph()

        if left_class is not None and right_class is not None and left_class == right_class:
            visualizer.update_message("Result: UNSAT")
            return "UNSAT" 

    visualizer.update_message("Result: SAT")
    return "SAT"

if __name__ == "__main__":
    # Example usage
    #formula = "f(g(x)) = g(f(x)) & f(g(f(y))) = x & f(y) = x & g(f(x)) != x"
    if len(sys.argv) < 2:
        print("Usage: python project1/scripts/graph.py '<formula>'")
        sys.exit(1)

    formula = sys.argv[1]
    print(f"Received formula: {formula}\n") 
    clauses_dict = get_clauses_dict(sanitize(formula))
    #print(formula)
    eq_classes = get_eq_classes(clauses_dict)

    result = congruence_closure(eq_classes, clauses_dict, v=False)
    print(f"\nResult: {result}\n")