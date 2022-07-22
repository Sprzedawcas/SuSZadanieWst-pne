from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import json
import datetime



app = Flask(__name__)

app.secret_key = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///notes.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

#note - note
#li_note - list note
#con_note - link note

class notes(db.Model):
    id_ = db.Column("id",db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(500))
    cration_date = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, title, content):
        self.title = title 
        self.content = content 


#w bazie danych przechowywac listę z zadaniami i każda posiadała 2 opcje True i False w postaci tego w zależności czy zrobiona czy nie 

class linotes(db.Model):
    id_ = db.Column("id",db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String())
    cration_date = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, title, content):
        self.title = title 
        self.content = content 


@app.route('/')
def hello_world():
    return 'This is my first API call!'




@app.route('/linote', methods=["POST"])
def linote():
    input_json = request.get_json(force=True) 
    action = input_json['action']
    if action == "CREATE":
        
        sub_items = input_json['content'].split("|")
        for item in sub_items:
            if len(item) > 100:

                return jsonify({"status":"Some of items was too long"})
        
        linoteid = create_linote(input_json)
        return jsonify({"status":"note add", "linoteid":linoteid})
    
    if action == "LIST_STATUS":
        change_subitem_status(input_json)

def linote_string_to_list(x):
    print(x)
    x = x.split("|}")
    y = []
    for itemx in x:
        y.append(itemx.split("{|"))
    y= y[:-1]
    return y


def create_linote(json):
    sub_items = json['content'].replace("|","{|0|}")
    print(sub_items)
    linote = linotes(json['title'], sub_items)
    db.session.add(linote)
    db.session.commit()
    
    return linote.id_

def change_subitem_status(json):



@app.route('/nnote', methods=["POST"])
def note():
    input_json = request.get_json(force=True) 
    action = input_json['action']
    if action == "CREATE":
        if len(input_json['content']) < 500:
            noteid = create_note(input_json)
            return jsonify({"status":"note add", "noteid":noteid})
        else:
            return jsonify({"status":"note too long max 500 character"})


def create_note(json):
    note = notes(json['title'], json['content'])
    db.session.add(note)
    db.session.commit()
    return note.id_




@app.route('/find',methods=["POST"])
def find_note():
    input_json = request.get_json(force=True) 
    action = input_json['action']
    if action == "ALL": 
        return jsonify(find_all())


def find_all():
    #note
    notess = notes.query.all() #Zmienić tutaj nazwę prze pushem 
    noutput = []
    for note in notess:
        x = {"note_id":note.id_,"title":note.title, "content":note.content, "cration_date":str(note.cration_date)} #trzeba by ło zamienić na tringa bo w json nie ma czegoś takiego jak data
        noutput.append(x)
    #linote
    linotess = linotes.query.all()
    lioutput = []
    
    for linote in linotess:
        x = {"note_id":linote.id_,"title":linote.title, "content":linote_string_to_list(linote.content), "cration_date":str(linote.cration_date)}
        lioutput.append(x)
    return json.dumps({"notes":noutput,"linotes":lioutput})



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True) 