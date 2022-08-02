import requests
  

choice = input("1 - Wyślij notatkę tekstową \n 2 -Notatka Linkowa \n 3 - Wyslij notatkę podpunktową \n 4 - Zatwierdź punkt notatki \n 5-  znajdź notatkę")
if choice == "1":
    r = requests.post('http://127.0.0.1:5000/note', json={
"action": "CREATE_N",
"title" : "TES1232dsaddsa3sT",
"content" : "Blflald1asdasdasds231231lasdjasjduasidj",
"due_date" : ""})#1658756884
elif choice == "2":
    r = requests.post('http://127.0.0.1:5000/note', json={
"action": "CREATE_CON",
"title" : "TES12323sT",
"content" : "test.pl",
"due_date" : ""})
elif choice == "3":
    r = requests.post('http://127.0.0.1:5000/note', json={
"action": "CREATE_LI",
"title" : "TES12323sT",
"content" : "Bjdasnsadjsavnxidjsajjjkdosadsjad|fjsdjdiojsdjiasjidjasjd|jusdhjadjiasjdjasjdasdjasj|",
"due_date" : ""})
elif choice == "4":
      r = requests.post('http://127.0.0.1:5000/note', json={
"action": "LIST_STATUS",
"note_id": "3",
"note_order":"2"})
elif choice == "5":
    r = requests.post('http://127.0.0.1:5000/find', json={
"action": "TYPE",
"type":"CON_NOTE"
}) #ALL 
elif choice == "6":
    r = requests.post('http://127.0.0.1:5000/find', json={
"action": "DATE",
"date":"CON_NOTE"
}) #ALL 




print(f"Status Code: {r.status_code}, Response: {r.json()}")



# {
# "action": "CREATE",
# "title" : "TES12323sT",
# "content" : "Bjdasnsadjsavnxidjsajjjkdosadsjad|||fjsdjdiojsdjiasjidjasjd|||jusdhjadjiasjdjasjdasdjasj",
# "due date" : ""}