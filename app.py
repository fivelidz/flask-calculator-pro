from flask import Flask, render_template, request
import re

app = Flask(__name__)

def safe_eval(expr):
    """Safely evaluate basic math expressions with order of operations."""
    # Only allow numbers and math symbols
    if not re.match(r'^[\d\s\+\-\*/\(\)\.]+$', expr):
        raise ValueError("Invalid characters in expression")
    return eval(expr, {"__builtins__": None}, {})

def solve_for_x(equation):
    """Solve simple linear equations of the form: x + 5 = 9"""
    try:
        # Remove spaces
        equation = equation.replace(" ", "")
        left, right = equation.split("=")
        if "x" not in equation:
            raise ValueError("No variable to solve for.")

        # Move all terms to one side: ax + b = c → ax = c - b
        if "x" in left:
            left_expr = left.replace("x", "1*x")
            result = safe_eval(right) - safe_eval(re.sub(r"x", "0", left_expr))
            coeff = safe_eval(left_expr.replace("x", "1"))
        else:
            right_expr = right.replace("x", "1*x")
            result = safe_eval(left) - safe_eval(re.sub(r"x", "0", right_expr))
            coeff = -safe_eval(right_expr.replace("x", "1"))

        if coeff == 0:
            return "No solution (x cancels out)"
        return result / coeff
    except Exception as e:
        return f"Could not solve equation: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    expression = ""

    if request.method == "POST":
        expression = request.form["expression"]

        try:
            if "=" in expression:
                result = solve_for_x(expression)
            else:
                result = safe_eval(expression)
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result, expression=expression)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
