from flask import Flask, render_template, jsonify
import json
import time

app = Flask(__name__)

# Load JSON data from file
def load_data():
    with open("kzg.json", "r") as file:
        data = json.load(file)
    return data["videos"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_data")
def get_data():
    return jsonify(load_data())

if __name__ == "__main__":
    app.run(debug=True)
