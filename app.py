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



if __name__=="__main__":
    app.run(debug=True)