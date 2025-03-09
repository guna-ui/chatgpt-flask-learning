from flask import Flask,jsonify

app=Flask(__name__)

#define a API route

@app.route('/')
def home():
    return jsonify({"message":"Welcome to Task Management"})

@app.route('/tasks')
def get_tasks():
    tasks=[
        {"id": 1, "title": "Buy groceries", "status": "pending","due_date":2025},
        {"id": 2, "title": "Finish Flask project", "status": "in-progress","due_date":2028},
    ]
    return jsonify(tasks)

## day1 Task
@app.route('/about')
def about():
    return jsonify({"author":"guna","version":"1.0.0"})

if __name__=="__main__":
    app.run(debug=True)