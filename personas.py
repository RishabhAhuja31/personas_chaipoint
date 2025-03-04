from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

file_path = "personas.xlsx"  
df = pd.read_excel(file_path, dtype=str) 

@app.route("/", methods=["GET", "POST"])
def home():
    details = None  

    if request.method == "POST":
        phone_number = request.form["phone_number"].strip()  
        result = df[df["phone_no"] == phone_number]  

        if not result.empty:
            details = result.iloc[0].to_dict() 
        else:
            details = {"error": "Phone number not found in database."}

    return render_template("index.html", details=details)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get port from environment
    app.run(host="0.0.0.0", port=port)  # Bind to all interfaces