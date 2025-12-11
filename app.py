from flask import Flask , jsonify , request
import database as db

app = Flask(__name__)

db.create_table()

@app.route('/api/tasks' , methods = ['GET'])
def get_tasks():
    tasks = db.get_all_tasks()
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            "id": task[0],
            "title": task[1],
            "description": task[2],
            "priority": task[3],
            "due_date": task[4],
            "status": task[5],
            "created_at": task[6],
            "category_id": task[7]
        })
    return jsonify(tasks_list) , 200

@app.route('/api/tasks' , methods = ['POST'])
def create_task():
        data = request.get_json()
        title = data.get('title')
        description = data.get('description', '')
        priority = data.get('priority', 'Medium')
        due_date = data.get('due_date', '')
        category = data.get('category', 'General')
        db.add_task(title , description , priority ,due_date , category )
        return jsonify({"message": "Task created successfully"}), 201
        
@app.route('/api/tasks/<int:task_id>' , methods = ['DELETE'])
def delete_task(task_id):
    result = db.delete_task(task_id)
    if "not found" in result:
        return jsonify({"message": result}), 404
    
    return jsonify({"message": result}), 200

@app.route('/api/tasks/<int:task_id>' , methods = ['GET'])
def get_single_task(task_id):
    task = db.get_task_by_id(task_id)
    if  task is None:
        return jsonify({"error" : f"Cannot find the task by {task_id} id!"}) , 404
    task = {"id": task[0],
            "title": task[1],
            "description": task[2],
            "priority": task[3],
            "due_date": task[4],
            "status": task[5],
            "created_at": task[6],
            "category_id": task[7]}
    return jsonify(task) , 200


@app.route('/api/tasks/<int:task_id>' , methods = ['PUT'])
def update_task(task_id):
    update = request.get_json()   
    title = update.get('title')
    description = update.get('description')
    priority = update.get('priority')
    due_date = update.get('due_date')
    status = update.get('status')
    result = db.update_task(task_id ,title= title , description=description,priority=priority,due_date=due_date,status=status )
    if result:    
        return jsonify({"message":"Task updated successfully!"}) , 200
    return jsonify({"error":"Task cannot be updated"}) , 404



if __name__ == '__main__':
    app.run(debug=True)
    
    
