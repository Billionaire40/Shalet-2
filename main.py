from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Load tasks from file if it exists
if os.path.exists("tasks.json"):
    with open("tasks.json", "r") as file:
        tasks = json.load(file)
else:
    tasks = []

@app.route('/')
def index():
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t["done"]])
    open_tasks = total_tasks - completed_tasks
    return render_template("index.html", tasks=tasks, open_tasks=open_tasks, completed_tasks=completed_tasks)

@app.route('/add', methods=["POST"])
def add():
    task_name = request.form["task"]
    assigned_to = request.form["assigned_to"]
    priority = request.form["priority"]
    due_date = request.form["due_date"]

    new_task = {
        "task": task_name,
        "assigned_to": assigned_to,
        "priority": priority,
        "due_date": due_date,
        "done": False
    }

    tasks.append(new_task)
    save_tasks()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    tasks[task_id]["done"] = True
    save_tasks()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks()
    return redirect(url_for('index'))

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

app.run(host='0.0.0.0', port=81)