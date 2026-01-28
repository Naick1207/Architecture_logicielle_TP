from flask import jsonify, abort, make_response, request, url_for
from .app import app
from .models import questionnaires, Questionnaire

@app.route('/quiz/api/v1.0/questionnaires', methods=["GET"])
def get_questionnaires():
    return jsonify({'questionnaires': [q.to_json() for q in questionnaires]})

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods = ['GET'])
def get_questionnaire(questionnaire_id):
    for questionnaire in questionnaires:
        if questionnaire.id == questionnaire_id:
            return jsonify({'questionnaire': questionnaire.to_json()})
    return abort(404)

@app.route('/quiz/api/v1.0/questionnaires', methods = ['POST'])
def create_questionnaire():
    if not request.json or not 'nom' in request.json:
        return abort(400)

    questionnaire = Questionnaire(request.json['nom'])
    questionnaires.append(questionnaire)
    return jsonify({'questionnaire': questionnaire.to_json()}), 201

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods = ['PUT'])
def update_questionnaire(questionnaire_id):
    questionnaire = None
    for q in questionnaires:
        if q.id == questionnaire_id:
            questionnaire = q
            break
    if questionnaire is None:
        abort(404)
    if not request.json or ('nom' in request.json and not isinstance(request.json['nom'], str)):
        abort(400)
    questionnaire.nom = request.json.get('nom', questionnaire.nom)
    return jsonify({'questionnaire': questionnaire.to_json()})

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods = ['DELETE'])
def delete_questionnaire(questionnaire_id):
    questionnaire = None
    for q in questionnaires:
        if q.id == questionnaire_id:
            questionnaire = q
            break
    if questionnaire is None:
        abort(404)
    questionnaires.remove(questionnaire)
    return jsonify({'status': 'deleted'})

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/<int:question_num>', methods = ['GET'])
def afficher_question(questionnaire_id, question_num):
    questionnaire = None
    for q in questionnaires:
        if q.id == questionnaire_id:
            questionnaire = q
            break
    if questionnaire is None:
        abort(404)
    question = None
    for q in questionnaire.questions:
        if q.numero == question_num:
            question = q
            break
    if question is None:
        abort(404)
    return jsonify({'question': question.to_json()})
    

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods = ['POST'])
def create_question(questionnaire_id):
    questionnaire = None
    for q in questionnaires:
        if q.id == questionnaire_id:
            questionnaire = q
            break
    if questionnaire is None:
        return abort(404)
    if not request.json or not 'enonce' in request.json:
        return abort(400)
    question = questionnaire.ajouter_question(request.json['enonce'])
    return jsonify({'question' : question.to_json()}), 201

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/<int:question_num>', methods = ['DELETE'])
def delete_question(questionnaire_id, question_num):
    questionnaire = None
    for q in questionnaires:
        if q.id == questionnaire_id:
            questionnaire = q
            break
    if questionnaire is None:
        return abort(404)
    question = questionnaire.retirer_question(question_num)
    if question is None:
        return abort(404)
    else:
        return jsonify({'status' : "deleted"})