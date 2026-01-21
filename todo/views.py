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
    return abort(404)

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'],
                                        _external = True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    #vérification des données reçues
    if not request.json or not 'title' in request.json:
        return abort(400)
    #construction de la nouvelle tâche
    if tasks == []:
        new_id = 1
    else:
        new_id = tasks[-1]['id'] + 1
    task = {
        'id': new_id,
        'title': request.json['title'],
        'description': request.json['description'],
        'done': request.json.get('done', False)
    }
    #ajout de la nouvelle tâche aux tâches existantes
    tasks.append(task)
    #retour de la nouvelle tâche avec son uri 201 indique qu'une ressource a été créée
    return jsonify({'task': make_public_task(task)}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)