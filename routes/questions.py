from flask import Blueprint, jsonify, make_response, request, redirect, flash
from config.server_conf import db
from controller.Foro_questions import Questions
from datetime import datetime

questions = Blueprint("questions", __name__)

@questions.route("/new", methods=['POST'])
def new_question():
    Questions.create_question()

    flash("Pregunta creada")

    return redirect("/")

@questions.route("/list")
def questions_list():
    response = Questions.list_questions()

    return response

@questions.route("/edit/<id_question>", methods = ['GET','POST'])
def edit(id_question):
    quiestion = Questions.query.get(id_question)
    quiestion_to_be_edited = Questions.edit_question(id_question, quiestion)
    if quiestion_to_be_edited == None:
        flash("Pregunta editada")

        return redirect("/")
    else:

        return quiestion_to_be_edited

@questions.route("/delete/<id_question>")
def delete(id_question):
    quiestion = Questions.query.get(id_question)
    Questions.delete_question(id_question, quiestion)

    flash("Pregunta cancelada")

    return redirect("/")


