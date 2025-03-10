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

@app.route('/tasks',methods=['Get'])
def get_tasks():
    sort_by=request.args.get("sort_by","id")
    order  =request.args.get("order","asc")
    valid_fields = ["id", "title", "status", "due_date"]
    if sort_by not in valid_fields:
        return jsonify({"message":f"invalid sortby field.choose from {valid_fields}"}),404
    reverse=order.lower()=="desc"
    sorted_tasks=sorted(tasks,key=lambda x:x[sort_by],reverse=reverse)
    # return jsonify(sorted_tasks)

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))
    start = (page - 1) * limit
    end = start + limit
    paginated_tasks = sorted_tasks[start:end]
    return jsonify({
        "total_tasks": len(tasks),
        "page": page,
        "limit": limit,
        "tasks": paginated_tasks
    })
    

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

@app.route("/tasks/<int:taskid>",methods=["PUT"])
def update_task(taskid):
    data=request.get_json()
    task=next((task for task in tasks if task["id"]==taskid),None)
    if not  task:
        return jsonify({"message":"taskid is not  available"})
    if not any(key in data for key in ["title", "status", "due_date"]):
        return jsonify({"message": "At least one field (title, status, due_date) required"}), 400
    task["title"]=data.get("title",task["title"])
    task["status"]=data.get("status",task["status"])
    task["due_date"]=data.get("due_date",task["due_date"])
    return jsonify({"message": "Task updated successfully", "task": task})

@app.route('/tasks/<int:task_id>',methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task=next((task for task in tasks if task["id"]==task_id),None)
    if not  task:
        return jsonify({"message":"taskid is not  available"})
    tasks=[task for task in tasks if task["id"] != task_id]
    return jsonify({"message": f"Task {task_id} deleted successfully"})
       
if __name__=="__main__":
    app.run(debug=True)