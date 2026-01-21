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

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=["PUT"])
def update_task(task_id):
    #Recherche de la ta tâche à modifier avec son id
    task = None
    for taski in tasks:
        if taski['id'] == task_id:
            task = taski
            break
    #La tâche avec cette id n'existe pas
    if task is None:
        abort(404)
    #La requête n'est pas au format json
    if not request.json:
        abort(400)
    #Vérification des types
    if 'title' in request.json and not isinstance(request.json['title'], str):
        abort(400)
    if 'description' in request.json and not isinstance(request.json['description'], str):
        abort(400)
    if 'done' in request.json and not isinstance(request.json['done'], bool):
        abort(400)
    #Modification des champs de la tâche
    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    task['done'] = request.json.get('done', task['done'])
    #Retour de la tâche modifiée
    return jsonify({'task': make_public_task(task)})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=["DELETE"])
def delete_task(task_id):
    task = None
    for taski in tasks:
        if taski['id'] == task_id:
            task = taski
            break
    if task is None:
        abort(404)
    tasks.remove(task)
    return jsonify({'status': 'deleted'})