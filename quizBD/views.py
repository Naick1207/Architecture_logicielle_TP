from flask import jsonify, abort, make_response, request, url_for
from .app import app, db
from .models import *

@app.route('/quiz/api/v1.0/questionnaires', methods=["GET"])
def get_questionnaires():
    return jsonify({'questionnaires': [q.to_json() for q in recuperer_questionnaires()]})

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods = ['GET'])
def get_questionnaire(questionnaire_id):
    questionnaire = recuperer_questionnaire(questionnaire_id)
    if questionnaire is not None:
        return jsonify({'questionnaire': questionnaire.to_json()})
    return abort(404)

@app.route('/quiz/api/v1.0/questionnaires', methods = ['POST'])
def create_questionnaire():
    if not request.json or not 'nom' in request.json:
        return abort(400)

    questionnaire = creer_questionnaire(request.json['nom'])
    return jsonify({'questionnaire': questionnaire.to_json()}), 201

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods = ['PUT'])
def update_questionnaire(questionnaire_id):
    if not request.json or ('nom' in request.json and not isinstance(request.json['nom'], str)):
        abort(400)
    questionnaire = modifier_questionnaire(questionnaire_id, request.json['nom'])
    if questionnaire is None:
        abort(404)
    return jsonify({'questionnaire': questionnaire.to_json()})

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods = ['DELETE'])
def delete_questionnaire(questionnaire_id):
    questionnaire = supprimer_questionnaire(questionnaire_id)
    if questionnaire is None:
        abort(404)
    return jsonify({'status': 'deleted'})

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/<int:question_num>', methods = ['GET'])
def afficher_question(questionnaire_id, question_num):
    questionnaire = recuperer_questionnaire(questionnaire_id)
    if questionnaire is None:
        abort(404)
    question = questionnaire.get_question(question_num)
    if question is None:
        abort(404)
    return jsonify({'question': question.to_json()})
    

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods = ['POST'])
def create_question(questionnaire_id):
    questionnaire:Questionnaire = recuperer_questionnaire(questionnaire_id)
    if questionnaire is None:
        return abort(404)
    if not request.json or not 'enonce' in request.json or not 'type' in request.json:
        return abort(400)
    if request.json['type'] == 'ouverte':
        if not 'reponse' in request.json:
            return abort(400)
        question = questionnaire.ajouter_question(request.json['enonce'], 'ouverte', request.json['reponse'])
    elif request.json['type'] == 'qcm':
        if not 'bonne_reponse' in request.json or not 'reponse1' in request.json or not 'reponse2' in request.json:
            return abort(400)
        question = questionnaire.ajouter_question(request.json['enonce'], 'qcm', request.json)
    else:
        return abort(400)
    return jsonify({'question' : question.to_json()}), 201

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/<int:question_num>', methods = ['DELETE'])
def delete_question(questionnaire_id, question_num):
    questionnaire = recuperer_questionnaire(questionnaire_id)
    if questionnaire is None:
        return abort(404)
    question = questionnaire.retirer_question(question_num)
    if question is None:
        return abort(404)
    else:
        return jsonify({'status' : "deleted"})