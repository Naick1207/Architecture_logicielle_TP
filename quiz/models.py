class Question:
    def __init__(self, numero, enonce):
        self.numero = numero
        self.enonce = enonce

    def to_json(self):
        return {"numero" : self.numero, "enonce" : self.enonce}


class Questionnaire:
    id = -1
    @classmethod
    def nouvel_id(cls) -> int:
        cls.id+=1
        return cls.id

    def __init__(self, nom:str):
        self.id = Questionnaire.nouvel_id()
        self.nom = nom
        self.questions:list[Question] = []
    
    def ajouter_question(self, enonce:str):
        question = Question(len(self.questions), enonce)
        self.questions.append(question)
        return question
    
    def retirer_question(self, numero:int):
        question = None
        for q in self.questions:
            if q.numero == numero:
                question = q
                break
        if question is not None:
            self.questions.remove(question)
        return question

    def get_question(self, numero:int):
        for question in self.questions:
            if question.numero == numero:
                return question
    
    def get_questions(self):
        return self.questions
    
    def __str__(self):
        return f"id : {self.id}, nom : {self.nom}"

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return {"nom" : self.nom, "questions" : [q.to_json() for q in self.questions]}

def recuperer_questionnaires():
    return questionnaires

def recuperer_questionnaire(id):
    questionnaire = None
    for q in questionnaires:
        if q.id == id:
            questionnaire = q
            break
    return questionnaire
    
def creer_questionnaire(nom):
    questionnaires.append(Questionnaire(nom))

def supprimer_questionnaire(id):
    questionnaire = None
    for q in questionnaires:
        if q.id == id:
            questionnaire = q
            break
    if questionnaire is not None:
        questionnaires.remove(questionnaire)



questionnaires:list[Questionnaire] = []
creer_questionnaire("Test1")
creer_questionnaire("Test2")
