import json

class Questionnaire:
    id = 0
    @classmethod
    def nouvel_id(cls) -> int:
        cls.id+=1
        return cls.id

    def __init__(self, nom:str):
        self.id = Questionnaire.nouvel_id()
        self.nom = nom
    
    def __str__(self):
        return f"id : {self.id}, nom : {self.nom}"

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

def recuperer_questionnaires():
    return questionnaires

def recuperer_questionnaire(id):
    question = None
    for q in questionnaires:
        if q.id == id:
            question = q
            break
    return question
    
def creer_questionnaire(nom):
    questionnaires.append(Questionnaire(nom))

def supprimer_questionnaire(id):
    question = None
    for q in questionnaires:
        if q.id == id:
            question = q
            break
    if question is not None:
        questionnaires.remove(question)



questionnaires:list[Questionnaire] = []
creer_questionnaire("Test1")
creer_questionnaire("Test2")
print(recuperer_questionnaires())
print(recuperer_questionnaire(1))
supprimer_questionnaire(1)
print(recuperer_questionnaires())
print(recuperer_questionnaire(2))
print(questionnaires[0].to_json())
