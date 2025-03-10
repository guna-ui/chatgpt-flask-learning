from flask import Flask,jsonify,request

app=Flask(__name__)

tasks=[
        {"id": 1, "title": "Buy groceries", "status": "pending","due_date":2025},
        {"id": 2, "title": "Finish Flask project", "status": "in-progress","due_date":2028},
    ]

#define a API route

@app.route('/')
def home():
    return jsonify({"message":"Welcome to Task Management"})



## day1 Task
@app.route('/about')
def about():
    return jsonify({"author":"guna","version":"1.0.0"})

@app.route('/tasks/<int:taskid>')
def get_task(taskid):
  for task in tasks:
      if task["id"]==taskid:
          return jsonify(task)
  return jsonify({"error":"Task not found"}),404

@app.route('/tasks')
def get_tasks():
    status=request.args.get("status")
    get_date=request.args.get("due_date")
    if status:
        filtered_status=[task for task in tasks if task["status"]==status]
        return jsonify(filtered_status)
    elif get_date :
        filtered_date=[task for task in tasks if task["due_date"]==int(get_date)]
        return jsonify(filtered_date)
    return jsonify(tasks)

@app.route('/tasks/title/<string:title>')
def get_task_title(title):
    for task in tasks:
        if task["title"]==title:
            return jsonify(task)
    return jsonify({"error":"Task not found"}),404

@app.route('/tasks',methods=["POST"])
def add_task():
    data=request.get_json()
    if not data or "title" not in data:
        return jsonify({"error":"Title is required"}),404
    if any(task["title"].lower()==data["title"].lower() for task in tasks):
        return jsonify({"error": "Task with this title already exists"}), 400
    new_task={
        "id":len(tasks)+1,
        "name":data["title"],
        "status":data.get("status","pending"),
        "due_date":data.get("due_date",2025)
    }
    tasks.append(new_task)
    return jsonify(new_task),201

@app.route("/tasks/bulk", methods=["POST"])
def multiple_tasks():
    data = request.get_json()  # Get JSON data from request

    if not isinstance(data, list):  # Ensure input is a list
        return jsonify({"message": "Expected a list of tasks"}), 400

    existing_titles = {task["title"].lower() for task in tasks}  # Track existing task titles
    new_tasks = []  # Store new tasks

    for d in data:
        if "title" not in d:
            return jsonify({"message": "Each task must have a title"}), 400

        if d["title"].lower() in existing_titles:  # Skip duplicates
            continue  

        new_task = {
            "id": len(tasks) + len(new_tasks) + 1,
            "title": d["title"],
            "status": d.get("status", "pending"),
            "due_date": d.get("due_date", 2023),
        }
        new_tasks.append(new_task)
        existing_titles.add(d["title"].lower())  # Track new titles

    if not new_tasks:
        return jsonify({"message": "No new tasks added"}), 400

    tasks.extend(new_tasks)  # Add new tasks to global list
    return jsonify({"message": "Tasks added successfully", "tasks": new_tasks}), 201

       
if __name__=="__main__":
    app.run(debug=True)