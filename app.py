from flask import Flask, render_template, request

# Auto-install sympy if needed
try:
    from sympy import symbols, Eq, solve, sympify
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "sympy"])
    from sympy import symbols, Eq, solve, sympify

app = Flask(__name__)

def process_input(expression):
    try:
        # Check for equation solving (contains "=")
        if "=" in expression:
            x = symbols("x")
            left, right = expression.split("=")
            left_expr = sympify(left.strip())
            right_expr = sympify(right.strip())
            equation = Eq(left_expr, right_expr)
            solution = solve(equation, x)
            return f"x = {solution[0]}" if solution else "No solution found."
        else:
            # Evaluate normal math expression
            result = sympify(expression)
            return result
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    expression = ""

    if request.method == "POST":
        expression = request.form["expression"]
        result = process_input(expression)

    return render_template("index.html", result=result, expression=expression)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
