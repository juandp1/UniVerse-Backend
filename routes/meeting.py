from flask import Blueprint, jsonify, make_response, request, redirect, flash
from config.server_conf import db
from controller.Meeting import Meeting
from datetime import datetime

meetings = Blueprint("meetings", __name__)

@meetings.route("/new", methods=['POST'])
def new_meet():
    Meeting.create_meet()

    flash("Reunión creada")

    return redirect("/")

@meetings.route("/list")
def meetings_list():
    response = Meeting.list_meetings()

    return response

@meetings.route("/edit/<id_meeting>", methods = ['GET','POST'])
def edit(id_meeting):
    meet = Meeting.query.get(id_meeting)
    meet_to_be_edited = Meeting.edit_meet(id_meeting, meet)
    if meet_to_be_edited == None:
        flash("Reunión editada")

        return redirect("/")
    else:

        return meet_to_be_edited

@meetings.route("/delete/<id_meeting>")
def delete(id_meeting):
    meet = Meeting.query.get(id_meeting)
    Meeting.delete_meet(id_meeting, meet)

    flash("Reunión cancelada")

    return redirect("/")


