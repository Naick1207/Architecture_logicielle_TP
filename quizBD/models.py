from .app import db

class Question(db.Model):
    __tablename__ = "Question"

    numero = db.Column(db.Integer, primary_key=True)
    enonce = db.Column(db.String(50), nullable=False)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('Questionnaire.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    questionnaire = db.relationship("Questionnaire", backref=db.backref("questions", lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, numero, enonce, questionnaire_id):
        self.numero = numero
        self.enonce = enonce
        self.questionnaire_id = questionnaire_id

    def to_json(self):
        return {"numero" : self.numero, "enonce" : self.enonce}


class Questionnaire(db.Model):
    __tablename__ = "Questionnaire"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)

    def __init__(self, nom:str):
        self.nom = nom
    
    def ajouter_question(self, enonce:str):
        question = Question(len(list(self.questions)) + 1, enonce, self.id)
        db.session.add(question)
        db.session.commit()
        return question
    
    def retirer_question(self, numero:int):
        question = Question.query.filter(Question.numero == numero, Question.questionnaire_id == self.id)
        if question is not None:
            db.session.delete(question)
            db.session.commit()
        return question

    def get_question(self, numero:int):
        question = Question.query.filter(Question.numero == numero, Question.questionnaire_id == self.id)
        return question
    
    def get_questions(self):
        return self.questions
    
    def __str__(self):
        return f"id : {self.id}, nom : {self.nom}"

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return {"nom" : self.nom, "questions" : [q.to_json() for q in self.questions]}

def recuperer_questionnaires() -> list[Question]:
    return Questionnaire.query.all()

def recuperer_questionnaire(id):
    return Questionnaire.query.get(id)
    
def creer_questionnaire(nom):
    questionnaire = Questionnaire(nom)
    db.session.add(questionnaire)
    db.session.commit()
    return questionnaire

def supprimer_questionnaire(id):
    questionnaire = Questionnaire.query.get(id)
    if questionnaire is not None:
        db.session.delete(questionnaire)
        db.session.commit()
    return questionnaire

def modifier_questionnaire(id, nom):
    questionnaire = Questionnaire.query.get(id)
    if questionnaire is not None:
        questionnaire.nom = nom
        db.session.commit()
    return questionnaire

