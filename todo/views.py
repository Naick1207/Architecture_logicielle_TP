from flask import jsonify, abort, make_response, request, url_for
from .app import app
from .models import tasks

@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
    public_tasks = []
    for task in tasks:
        public_tasks.append(make_public_task(task))
    return jsonify({'tasks': public_tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return jsonify({'task': make_public_task(task)})
    return {'error': 'Not found'}, 404

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'],
                                        _external = True)
        else:
            new_task[field] = task[field]
    return new_task