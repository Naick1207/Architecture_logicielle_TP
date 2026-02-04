from .app import app, db
from .models import creer_questionnaire

@app.cli.command()
def syncdb():
    db.drop_all()
    db.create_all()
    qz1 = creer_questionnaire("Maths")
    qz2 = creer_questionnaire("Français")
    qz3 = creer_questionnaire("Histoire")
    qz1.ajouter_question("2+2")
    qz1.ajouter_question("1*5")
    qz2.ajouter_question("Le COD ?")