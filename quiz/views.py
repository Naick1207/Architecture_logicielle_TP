from flask import jsonify, abort, make_response, request, url_for
from .app import app
from .models import questionnaires, Questionnaire

@app.route('/quiz/api/v1.0/questionnaires', methods=["GET"])
def get_questionnaires():
    return jsonify({'questionnaires': questionnaires})