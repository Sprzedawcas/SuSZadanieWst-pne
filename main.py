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
    content = db.Column(db.String())
    cration_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    type_ = db.Column(db.String())

    def __init__(self, title, content,type_):
        self.cration_date=datetime.now()
        self.title = title 
        self.content = content 
        self.type_ = type_



#note 
@app.route('/note', methods=["POST"])
def note():
    input_json = request.get_json(force=True) 
    action = input_json['action']
    
    
    if action == "CREATE_N":
        if len(input_json['content']) < 500:
            noteid = create_note(input_json)
            return jsonify({"status":"note add", "noteid":noteid})
        else:
            return jsonify({"status":"note too long max 500 character"})
    
    
    elif action == "CREATE_LI":
        sub_items = input_json['content'].split("|")
        for item in sub_items:
            if len(item) > 100:
                return jsonify({"status":"Some of items was too long"})
        
        linoteid = create_linote(input_json)
        return jsonify({"status":"note add", "linoteid":linoteid})

        
    elif action == "LIST_STATUS":
        change_subitem_status(input_json)
        return jsonify({"status":"linote update"}) 


    elif action == "CREATE_CON":
        for characters in input_json['content']:
            if characters == " ":
                 return jsonify({"status":"note content is no link"})
            
        con_noteid = create_con_note(input_json)
        return jsonify({"status":"note add", "noteid":con_noteid})


#note

def create_note(json):
    note = notes(json['title'], json['content'], "NOTE")
    if len(json['due_date']) == 10:
        note.due_date = datetime.fromtimestamp(int(json['due_date']))
        print("Bad due_date")
    db.session.add(note)
    db.session.commit()
    return note.id_


#li_note

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
    linote = notes(json['title'], sub_items,"LI_NOTE")
    if len(json['due_date']) == 10:
        linote.due_date = datetime.fromtimestamp(int(json['due_date']))
        print("Bad due_date")
    db.session.add(linote)
    db.session.commit()    
    return linote.id_

def change_subitem_status(json):
    linote = notes.query.filter_by(id_ = json['note_id']).first()
    linote_subitem = linote_string_to_list(linote.content)
    linote_subitem[int(json['note_order'])][1] = "1"
    linote_subitem_todb = ""
    for linoteitem in linote_subitem:
        linote_subitem_todb += linoteitem[0] + "{|" + linoteitem[1] + "|}"
    linote.content = linote_subitem_todb
    db.session.add(linote)
    db.session.commit()
    return



#con_note
   
def create_con_note(json):
    con_note = notes(json['title'], json['content'],"CON_NOTE")
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
    if action == "TYPE":
        return jsonify(find_type(input_json['type']))
    if action == "DATE":
        pass
def find_type(typee):
    notess = notes.query.filter(notes.type_== typee)
    noutput = []
    for note in notess:
        if typee == "LI_NOTE":
            x = {"noteType": note.type_,"note_id":note.id_,"title":note.title, "content":linote_string_to_list(note.content), "cration_date":str(note.cration_date)}
        else:
            x = {"noteType": note.type_,"note_id":note.id_,"title":note.title, "content":note.content, "cration_date":str(note.cration_date),"due_date":str(note.due_date)} #trzeba by ło zamienić na tringa bo w json nie ma czegoś takiego jak data
        noutput.append(x)
    return json.dumps({"notes":noutput})

def find_all():
    notess = notes.query.all() 
    noutput = []
    for note in notess:
        if note.type_ == "LI_NOTE":
            x = {"noteType": note.type_,"note_id":note.id_,"title":note.title, "content":linote_string_to_list(note.content), "cration_date":str(note.cration_date)}
        else:
            x = {"noteType": note.type_,"note_id":note.id_,"title":note.title, "content":note.content, "cration_date":str(note.cration_date),"due_date":str(note.due_date)} #trzeba by ło zamienić na tringa bo w json nie ma czegoś takiego jak data
        noutput.append(x)
    return json.dumps({"notes":noutput})



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True) 