from . import expression_parser as parser
from . import render

def plot(sympyfied_expression):
    f_numeric, num_variables = parser.analyze_and_compile(sympyfied_expression)

    if f_numeric is None or num_variables == 0:
        print("Failed to parse expression")
        return None

    if num_variables in (2, 3, 4):
        
        
        try:
            renderer = render.VisPyRenderer(f_numeric, num_variables)
            renderer.show()
        except Exception as e:
            print(f"Rendering error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"Unsupported number of variables: {num_variables}")
        return None