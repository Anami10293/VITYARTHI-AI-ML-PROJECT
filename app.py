from flask import Flask, render_template, request, redirect
import json
from datetime import datetime

app = Flask(__name__)

def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)

@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()

    if request.method == "POST":
        subject = request.form["subject"]
        date = request.form["date"]

        data.append({"subject": subject, "date": date})
        save_data(data)
        return redirect("/")

    # Priority logic
    today = datetime.today()
    for item in data:
        d = datetime.strptime(item["date"], "%Y-%m-%d")
        item["days_left"] = (d - today).days

    data.sort(key=lambda x: x["days_left"])

    return render_template("index.html", data=data)

app.run(debug=True)
