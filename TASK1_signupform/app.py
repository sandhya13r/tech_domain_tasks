from flask import Flask, render_template, request, redirect
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)

DATA_FILE = "users.txt"

def load_users():
    users = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    users.append({"username": parts[0], "email": parts[1], "password": parts[2]})
    return users

def save_users(users):
    with open(DATA_FILE, "w") as f:
        for u in users:
            f.write(f"{u['username']},{u['email']},{u['password']}\n")

@app.route("/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        users = load_users()
        users.append({"username": username, "email": email, "password": password_hash})
        save_users(users)

        return redirect("/dashboard")

    return render_template("signup.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    users = load_users()

    if request.method == "POST":  # delete user
        index = int(request.form["index"])
        users.pop(index)
        save_users(users)
        return redirect("/dashboard")

    return render_template("dashboard.html", users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
