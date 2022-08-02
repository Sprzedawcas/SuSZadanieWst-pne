from asyncio.windows_events import NULL
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
import time
from flask_sqlalchemy import SQLAlchemy
import json


from datetime import datetime

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
    title = db.Column(db.String()) 
    content = db.Column(db.String(500))
    cration_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    
    def __init__(self, title, content):
        self.cration_date=datetime.now()
        self.title = title 
        self.content = content 

class linotes(db.Model):
    id_ = db.Column("id",db.Integer,primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    cration_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)

    def __init__(self, title, content):
        self.cration_date=datetime.now()
        self.title = title 
        self.content = content 


class connotes(db.Model):
    id_ = db.Column("id",db.Integer,primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String(5))
    cration_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)

    def __init__(self, title, content):
        self.cration_date=datetime.now()
        self.title = title 
        self.content = content 



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
        return jsonify({"status":"linote update"}) 

def linote_string_to_list(x):
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
    if len(json['due_date']) == 10:
        linote.due_date = datetime.fromtimestamp(int(json['due_date']))
        print("Bad due_date")
    db.session.add(linote)
    db.session.commit()    
    return linote.id_

def change_subitem_status(json):
    linote = linotes.query.filter_by(id_ = json['note_id']).first()
    linote_subitem = linote_string_to_list(linote.content)
    linote_subitem[int(json['note_order'])][1] = "1"
    linote_subitem_todb = ""
    for linoteitem in linote_subitem:
        linote_subitem_todb += linoteitem[0] + "{|" + linoteitem[1] + "|}"
    linote.content = linote_subitem_todb
    db.session.add(linote)
    db.session.commit()
    return

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
    if len(json['due_date']) == 10:
        note.due_date = datetime.fromtimestamp(int(json['due_date']))
        print("Bad due_date")
    db.session.add(note)
    db.session.commit()
    return note.id_


#con_note


@app.route('/connote', methods=["POST"])
def con_note():
    input_json = request.get_json(force=True) 
    action = input_json['action']
    if action == "CREATE":
        for characters in input_json['content']:
            if characters == " ":
                 return jsonify({"status":"note content is no link"})
            
        con_noteid = create_con_note(input_json)
        return jsonify({"status":"note add", "noteid":con_noteid})

            


def create_con_note(json):
    con_note = connotes(json['title'], json['content'])
    if len(json['due_date']) == 10:
        con_note.due_date = datetime.fromtimestamp(int(json['due_date']))
        print("Bad due_date")
    db.session.add(con_note)
    db.session.commit()
    return con_note.id_

#finding


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
        x = {"note_id":note.id_,"title":note.title, "content":note.content, "cration_date":str(note.cration_date),"due_date":str(note.due_date)} #trzeba by ło zamienić na tringa bo w json nie ma czegoś takiego jak data
        noutput.append(x)
    #linote
    linotess = linotes.query.all()
    lioutput = []
    
    for linote in linotess:
        x = {"note_id":linote.id_,"title":linote.title, "content":linote_string_to_list(linote.content), "cration_date":str(linote.cration_date)}
        lioutput.append(x)

    #connote 
    connotess = connotes.query.all()
    conoutput = []

    for connote in connotess:
        x = {"note_id":connote.id_,"title":connote.title, "content":connote.content, "cration_date":str(connote.cration_date)}
        conoutput.append(x)

    return json.dumps({"notes":noutput,"linotes":lioutput,"connotes":conoutput})



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True) 