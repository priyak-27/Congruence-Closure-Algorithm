import re
from collections import OrderedDict


def sanitize(formula):
    try:
        trimmed = formula.replace(" ", "")
        clauses = trimmed.split("&")
        return clauses
    except Exception as e:
        print("Formula parsing error")
        raise e

def get_clauses_dict(clauses):
    clauses_dict = {i: [] for i in range(-1,len(clauses)-1)}
    for i in range(len(clauses)):
        c = clauses[i]
        if "!=" in c:
            left_ineq, right_ineq = c.split("!=")
            clauses_dict[-1] = [left_ineq, right_ineq]
        else:
            clauses_dict[i] = c.split("=")
    return clauses_dict

def get_terms(clauses_dict):
    terms = []
    for k,v in clauses_dict.items():
        terms += v

    return terms

def split_arguments(arg_string):
    # Split a string of arguments, ensuring nested arguments are handled correctly
    args = []
    depth = 0
    current_arg = []

    for char in arg_string:
        if char == ',' and depth == 0:
            args.append(''.join(current_arg).strip())
            current_arg = []
        else:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            current_arg.append(char)

    # Add the last argument
    if current_arg:
        args.append(''.join(current_arg).strip())

    return args

def function_chain(expression):
    # Extracting terms and subterms from a function expression
    # Handles both univariate (e.g., "f(a)") and multivariate (e.g., "f(a, b)") cases
    result = []
    stack = [expression]

    while stack:
        current = stack.pop()
        # Match the outermost function call
        match = re.fullmatch(r'(\w+)\((.+)\)', current)
        if match:
            result.append(current)
            arguments = split_arguments(match.group(2))
            stack.extend(arguments)
        else:
            result.append(current)
    
    return result

def get_eq_classes(clauses_dict):
    terms = get_terms(clauses_dict)

    eq_classes = []
    for t in terms:
        eq_classes += function_chain(t)
        
    eq_classes = (list(set(eq_classes)))
    eq_classes = [[k] for k in eq_classes]
    return eq_classes

class ResetException(BaseException):
    def __init__(self, *args):
        super().__init__(*args)
