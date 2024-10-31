from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
with app.app_context():
    db = SQLAlchemy(app)

class Firstapp_Aitsam(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.sno} - {self.fname}"

# Route for main page
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        if fname and lname and email:
            new_person = Firstapp_Aitsam(fname=fname, lname=lname, email=email)
            db.session.add(new_person)
            db.session.commit()

    allpeople = Firstapp_Aitsam.query.all()
    return render_template('index.html', allpeople=allpeople)

# Route for deleting an entry
@app.route('/delete/<int:sno>')
def delete(sno):
    person_to_delete = Firstapp_Aitsam.query.filter_by(sno=sno).first()
    if person_to_delete:
        db.session.delete(person_to_delete)
        db.session.commit()
    return redirect('/')

# Route for updating an entry
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    person_to_update = Firstapp_Aitsam.query.filter_by(sno=sno).first()
    
    if request.method == 'POST':
        person_to_update.fname = request.form.get('fname')
        person_to_update.lname = request.form.get('lname')
        person_to_update.email = request.form.get('email')

        db.session.commit()
        return redirect('/')
    
    return render_template('update.html', person=person_to_update)

# Home page route
@app.route('/home')
def home():
    return "Welcome to the Home Page"

if __name__ == "__main__":
    app.run(debug=True)
