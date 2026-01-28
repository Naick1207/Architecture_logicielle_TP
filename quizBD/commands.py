from .app import app, db
from .models import create_questionnaire

@app.cli.command()
def syncdb():

    db.create_all()
    qz1 = create_questionnaire("Maths")