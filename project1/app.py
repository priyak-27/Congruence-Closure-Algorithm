from flask import Flask, request, render_template, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def form_page():
    result = None  # Default: no result to show
    input_enabled = True  # Default: input is enabled

    if request.method == "POST":
        if "continue" in request.form:
            # User clicked Yes or No for continuing
            if request.form["continue"] == "no":
                return "<h1>Thank you! I hope it was helpful!</h1>", 200
            elif request.form["continue"] == "yes":
                # Enable the input field
                input_enabled = True
                return render_template("form.html", result=None, input_enabled=input_enabled)

        # Process the formula submitted
        formula = request.form.get("formula")
        if not formula:
            return "Error: No formula provided.", 400

        try:
            # Run your Python script with the formula
            result = subprocess.run(
                ["python3", "scripts/graph.py", formula],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()
            input_enabled = False  # Disable the input field after submission
        except subprocess.CalledProcessError as e:
            result = f"Error: {e.stderr}"
            input_enabled = True  # Keep input enabled in case of an error

    # Render the form with the current state
    return render_template("form.html", result=result, input_enabled=input_enabled)

if __name__ == "__main__":
    app.run(debug=True)