from flask import Flask, render_template, request
from controller.database import db
from controller.confige import Confige
from controller.model import *

app = Flask(__name__)
app.config.from_object(Confige)
db.init_app(app)

with app.app_context():
    db.create_all()

    if Role.query.count() == 0:
        student = Role(name='student')
        admin = Role(name='Admin')
        staff = Role(name='Staff')
        
        db.session.add_all([student, admin, staff]) 
        db.session.commit()
        

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)