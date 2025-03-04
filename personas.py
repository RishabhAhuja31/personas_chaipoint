from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load Excel sheet
file_path = "personas.xlsx"  # Update this with your actual file path
df = pd.read_excel(file_path, dtype=str)  # Read as string to avoid conversion issues

@app.route("/", methods=["GET", "POST"])
def home():
    details = None  # Default value

    if request.method == "POST":
        phone_number = request.form["phone_number"].strip()  # Get input and remove spaces
        result = df[df["phone_no"] == phone_number]  # Filter based on phone number

        if not result.empty:
            details = result.iloc[0].to_dict()  # Convert row to dictionary
        else:
            details = {"error": "Phone number not found in database."}

    return render_template("index.html", details=details)

if __name__ == "__main__":
    app.run(debug=True)
