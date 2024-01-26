import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId

def objId(findme):
    for find in collection.find({f'{findme}' :{'$exists': 'true'}}):
        return find['_id']
        break



    


if "client" not in st.session_state:
    st.session_state.client = MongoClient("mongodb+srv://nathaniel:fjUEye3fjmCb78eV@cluster0.uoteo13.mongodb.net/?retryWrites=true&w=majority")

if "user_disabled" not in st.session_state:
    st.session_state.user_disabled = False

if "matric_disabled" not in st.session_state:
    st.session_state.matric_disabled = False

if "name" not in st.session_state:
    st.session_state.name = None

if "matric" not in st.session_state:
    st.session_state.matric = None

if "count" not in st.session_state:
    st.session_state.count= 0

db = st.session_state.client["test"]
collection  = db.stds

for find in collection.find({'_id':ObjectId(objId('Group Leaders'))},{'_id':0}):
    testinglist = find

if "group_choices" not in st.session_state:
    st.session_state.group_choices= testinglist["Group Leaders"]

if "group_choice" not in st.session_state:
    st.session_state.group_choice= None

if "oldchoices" not in st.session_state:
    st.session_state.oldchoices= None



def groupChoosen():
    import random as rd
    if st.session_state.group_choices == []:
        st.write("No free group")
        st.session_state.group_choice ="No free group"

    else:
        for find in collection.find({'_id':ObjectId(objId('Group Leaders'))},{'_id':0}):
            testinglist = find
        group_choices = testinglist["Group Leaders"]

        choosen = rd.choice(st.session_state.group_choices)
        st.session_state.oldchoices= st.session_state.group_choices
        
        st.session_state.group_choices.remove(choosen)
        collection.update_one({"Group Leaders":group_choices},{"$set":{"Group Leaders":st.session_state.group_choices}})
        # print(st.session_state.oldchoices)
        
        
        

        st.write(choosen)
        st.session_state.group_choice = choosen
    

st.set_page_config(page_title="mongos tutorial")
if st.session_state.matric!= None and (st.session_state.matric) not in range(-5000000000000000000000,2000) and st.session_state.matric != 4188 and st.session_state.matric != 4035:
    st.write(f"enter the last 4 digits as your matric")
    st.session_state.matric_disabled = True

if st.session_state.name!= None and (st.session_state.name) != '' and len(st.session_state.name)>6  :
    st.session_state.user_disabled = True

def Submit():
    st.session_state.count+=1
    
    st.write(st.session_state.count)

st.info(icon="💀", body="FIll in with your Full Name and with Your last 4 digits of your Matric no.")
st.info(icon="🤖",body="Then Click shuffle and submit to join a group")
st.button("Submit name or matric you can only submit once")
st.session_state.name = st.text_input("Enter your name", disabled=st.session_state.user_disabled, key="student_name", value=st.session_state.name)

st.session_state.matric = st.number_input("Enter your matric",disabled=st.session_state.matric_disabled, key= "student_matric",format="%i",value=0, help="enter the last 4 digits as your matric")

if st.session_state.name is not None and len(st.session_state.name) > 6 and st.session_state.matric not in range(-5000000000000000000000,2000) and st.session_state.matric != 4188 and st.session_state.matric != 4035:

    if st.button("Shuffle,join group and submit", type="primary"):
        match_found = False

        for find in collection.find({}):
            if find['_id'] == ObjectId(objId('Group Leaders')):
                pass
            else:
                
                if find["name"] == st.session_state.name or find["matric no"] == st.session_state.matric:
                    match_found = True
                    st.error(f"You are already in team | {find['Group Leader']} |", icon="🚨")
                    st.warning(f"You registered with Name: |{find['name']}| and Matric: |{find['matric no']}|",icon="⚠️")
                    break  

        if not match_found:
            groupChoosen()
        
            st.write(f"{st.session_state.name}, {st.session_state.matric}, {st.session_state.group_choice}")
            collection.insert_one({"name": st.session_state.name, "matric no": st.session_state.matric, "Group Leader": st.session_state.group_choice})
            st.toast(f"Successfully joined Team {st.session_state.group_choice}", icon="✅")
            st.balloons()
            st.session_state.client.close()
            st.toast("Connection closed",icon="✅")





