class Questionnaire:
    id = 0
    @classmethod
    def nouvel_id(cls) -> int:
        cls.id+=1
        return cls.id

    def __init__(self, nom:str):
        self.id = Questionnaire.nouvel_id()
        self.nom = nom
    
    @staticmethod
    def recuperer_questionnaires():
        return questionnaires

    @staticmethod
    def recuperer_questionnaire(id):
        question = None
        for q in questionnaires:
            if q.id == id:
                question = q
                break
        return question
    
    @staticmethod
    def creer_questionnaire(nom):
        questionnaires.append(Questionnaire(nom))

    @staticmethod
    def supprimer_questionnaire(id):
        question = None
        for q in questionnaires:
            if q.id == id:
                question = q
                break
        if question is not None:
            questionnaires.remove(question)
    
    def __str__(self):
        return f"id : {self.id}, nom : {self.nom}"

    def __repr__(self):
        return self.__str__()


questionnaires:list[Questionnaire] = []
Questionnaire.creer_questionnaire("Test1")
Questionnaire.creer_questionnaire("Test2")
print(Questionnaire.recuperer_questionnaires())
print(Questionnaire.recuperer_questionnaire(1))
Questionnaire.supprimer_questionnaire(1)
print(Questionnaire.recuperer_questionnaires())
print(Questionnaire.recuperer_questionnaire(2))
