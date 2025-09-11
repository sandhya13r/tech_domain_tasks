from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "quiz_secret"  # needed for session handling

# Our quiz questions
questions = [
    {
        "question": "What is the capital of India?",
        "options": ["Mumbai", "Delhi", "Chennai", "Kolkata"],
        "answer": "Delhi"
    },
    {
        "question": "Which language is used for web apps?",
        "options": ["Python", "Java", "C++", "All of the above"],
        "answer": "All of the above"
    },
    {
        "question": "Which company developed Python?",
        "options": ["Google", "Microsoft", "Python Software Foundation", "Apple"],
        "answer": "Python Software Foundation"
    },
    {
        "question": "What does HTML stand for?",
        "options": ["Hyper Trainer Marking Language", "Hyper Text Markup Language", "High Text Machine Language", "None"],
        "answer": "Hyper Text Markup Language"
    },
    {
        "question": "Which is not a programming language?",
        "options": ["Python", "Ruby", "HTML", "Java"],
        "answer": "HTML"
    }
]

@app.route("/")
def index():
    # reset everything at start
    session["score"] = 0
    session["qno"] = 0
    session["answers"] = []
    return render_template("index.html")

@app.route("/question", methods=["GET", "POST"])
def question():
    qno = session.get("qno", 0)

    if request.method == "POST":
        selected = request.form.get("option")
        correct = questions[qno - 1]["answer"]

        # check answer
        if selected == correct:
            session["score"] += 1

        # store answer only once
        answers = session.get("answers", [])
        answers.append((questions[qno - 1]["question"], selected, correct))
        session["answers"] = answers

    if qno >= len(questions):
        return redirect(url_for("result"))

    question_data = questions[qno]
    session["qno"] = qno + 1
    return render_template("question.html", qno=qno+1, total=len(questions), question=question_data)

@app.route("/result")
def result():
    score = session.get("score", 0)
    answers = session.get("answers", [])
    return render_template("result.html", score=score, total=len(questions), answers=answers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
