
from flask import Flask, render_template

app = Flask(__name__)

tasks = [
    {"name": "Code Pushed to GitHub", "status": "done"},
    {"name": "GitHub Actions Triggered", "status": "done"},
    {"name": "Build Docker Image", "status": "done"},
    {"name": "Push Image to Docker Registry", "status": "done"},
    {"name": "Deploy using Docker Compose", "status": "done"}
]

@app.route("/")
def home():
    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
