import numpy as np
import sympy as sp


def analyze_and_compile(expr):
    try:
        syms = expr.free_symbols
        order_map = {'x': 0, 'y': 1, 'z': 2, 't': 3}
        
        variables = tuple(sorted(syms, key=lambda s: order_map.get(str(s), 99)))
        num_vars = len(variables)

        if num_vars < 2 or num_vars > 4:
            print(f"Error: Equation must have between 2 and 4 variables. Found {num_vars}.")
            return None, 0

    except Exception as e:
        print(f"Parser Error: Failed to analyze expression variables. {e}")
        return None, 0

    try:
        f_numeric = sp.lambdify(variables, expr, modules='numpy', dummify=False)
        
    except Exception as e:
        print(f"Parser/Compilation Error: Failed to convert expression to NumPy function. {e}")
        return None, 0

    return f_numeric, num_vars
    