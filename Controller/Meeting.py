from flask import jsonify, make_response, request
from config.server_conf import db
from flask_sqlalchemy import SQLAlchemy as sq
from datetime import datetime

class Community(db.model):
    id_community = db.Column(db.Integer, nullable = False, primary_key = True)
    name =db.Column(db.String(60), nullable = False)

class User(db.model):
    id_user = db.Column(db.Integer, nullable = False, primary_key = True)
    name =db.Column(db.String(60), nullable = False)

class Meeting(db.model):
    id_meeting = db.Column(db.Integer, nullable = False, primary_key = True)
    name = db.Column(db.String(60), nullable = False)
    description = db.Column(db.String(120))
    place = db.Column(db.String(100), nullable = False)
    date = db.Column(db.date, nullable = False)
    created_at = db.Column(db.datetime)
    updated_at = db.Column(db.datetime)
    id_community = db.Column(db.Integer, sq.ForeignKey(Community.id_community), nullable = False)
    id_user = db.Column(db.Integer, sq.ForeignKey(User.id_user), nullable = False)
    
    def __init__(self,name,description,place,date,id_community,id_user):
        self.name = name
        self.description = description
        self.place = place
        self.date = date
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.id_community = id_community
        self.id_user = id_user

    def create_meet():
        name = request.form['name']
        description = request.form['description']
        place = request.form['place']
        date = request.form['date']
        name_community = request.form['name_community']
        name_user = request.form['name_user']
        
        new_meet = Meeting(name, description, place, date, name_community, name_user)

        db.session.add(new_meet)
        db.session.commit()

    def list_meetings():
        meetings_list = Meeting.query.all()

        response = make_response(jsonify(meetings_list),200)
        response.headers["Content-Type"] = "application/json"

        return response

    def edit_meet(id_meeting, meet):
        if request.method == "POST":
            meet.name = request.form['name']
            meet.description = request.form['description']
            meet.place = request.form['place']
            meet.date = request.form['date']
            meet.updated_at = datetime.now()
            meet.id_community = request.form['id_community']
            meet.id_user = request.form['id_user']

            db.session.commit()
        else:
            response = make_response(jsonify(meet),200)
            response.headers["Content-Type"] = "application/json"

            return response 
        
    def delete_meet(id_meeting,meet):
        
        db.session.delete(meet)
        db.session.commit()