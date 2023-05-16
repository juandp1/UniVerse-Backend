from flask import jsonify, make_response, request
from config.server_conf import db
from flask_sqlalchemy import SQLAlchemy as sq
from datetime import datetime

#Tablas provisionals miestras se tiene las tablas originales en otros controladores
class Community(db.model):
    id_community = db.Column(db.Integer, nullable = False, primary_key = True)
    name =db.Column(db.String(60), nullable = False)

class User(db.model):
    id_user = db.Column(db.Integer, nullable = False, primary_key = True)
    name =db.Column(db.String(60), nullable = False)

class Topic(db.model):
    id_topic = db.Column(db.Integer, nullable = False, primary_key = True)
    name =db.Column(db.String(60), nullable = False)

#Controlador Meeting
class Questions(db.model):
    id_question = db.Column(db.Integer, nullable = False, primary_key = True)
    title = db.Column(db.String(60), nullable = False)
    description = db.Column(db.String(120))
    score = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.datetime)
    updated_at = db.Column(db.datetime)
    id_topic = db.Column(db.Integer, sq.ForeignKey(Topic.id_topic), nullable = False)
    id_community = db.Column(db.Integer, sq.ForeignKey(Community.id_community), nullable = False)
    id_user = db.Column(db.Integer, sq.ForeignKey(User.id_user), nullable = False)
    
    def __init__(self,title,description,score,id_topic,id_community,id_user):
        self.title = title
        self.description = description
        self.score = score
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.id_topic = id_topic
        self.id_community = id_community
        self.id_user = id_user

    def create_question():
        title = request.form['title']
        description = request.form['description']
        score = request.form['score']
        id_topic = request.form['id_topic']
        id_community = request.form['id_community']
        id_user = request.form['id_user']
        
        new_question = Questions(title, description, score, id_topic, id_community, id_user)

        db.session.add(new_question)
        db.session.commit()

    def list_questions():
        questions_list = Questions.query.all()

        response = make_response(jsonify(questions_list),200)
        response.headers["Content-Type"] = "application/json"

        return response

    def edit_question(id_question, question):
        if request.method == "POST":
            question.title = request.form['title']
            question.description = request.form['description']
            question.score = request.form['score']
            question.updated_at = datetime.now()
            question.id_topic = request.form['id_topic']
            question.id_community = request.form['id_community']
            question.id_user = request.form['id_user']

            db.session.commit()
        else:
            response = make_response(jsonify(question),200)
            response.headers["Content-Type"] = "application/json"

            return response 
        
    def delete_question(id_question,question):
        
        db.session.delete(question)
        db.session.commit()