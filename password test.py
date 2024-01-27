import bcrypt
from pymongo import MongoClient
from pymodm import connect, MongoModel, fields
from bson import ObjectId

connect("mongodb://localhost:27017/auth_tutorial")

class User(MongoModel):
    user_name = fields.CharField(mongo_name="User Name")
    password = fields.CharField(mongo_name="Password")
    # likes = fields.ListField(mongo_name="Likes")

class Actions(MongoModel):
    UserID = fields.ReferenceField(User, mongo_name='User Details')
    ActionType = fields.CharField(mongo_name="Action Taken")




def signup(user,passw):
    passw_2_hash= passw.encode('utf-8')
    hashed_passw =  bcrypt.hashpw(passw_2_hash,bcrypt.gensalt())
    new_user = User(user_name=user,password=hashed_passw)
    new_user.save()
    print('signup successfull')


def login(user,passw):
    passw = passw.encode('utf-8')
    #function that takes login details and returns true of false
    logged_in,uID =auth(user_name=user,password=passw)
    if logged_in:
        print("logged in")
        return uID
        
    else:
        print(" Wrong password or username")
        # print(logged_in)


def auth(user_name, password):
    users = User.objects.all()
    for u in users:
        if user_name == u.user_name:
            checkP = u.password
            checkP = checkP[2:-1]
            checkP= bytes(checkP,'utf-8')
            # print(type(checkP))            
            logged_in = bcrypt.checkpw(password,checkP)
            if logged_in:
                user_id = u._id
                break
        elif user_name != u.user_name:
            
            # print("user name not found")
            logged_in,user_id= None,None
    return logged_in, user_id


def start():
    while True:
        print("\n\nWelcome to the Password Manager! \nPlease choose an option from below : ")
        me =  input("user name >> ")
        p = input("password >> ")
        UserId=login(user=me,passw=p)
        print(type(UserId))

        if UserId==None:
            print("failed to login")
            signups = input("Type yes to signup:  ")
            if "yes" in signups:
                me =  input("user name >> ")
                p = input("password >> ")
                signup(me,p)
        else:
            while True:
                step2 = input("type something to be saved: ")
                action = Actions(UserID=UserId, ActionType= step2)
                action.save()
                end = input("To end type yes: ")

                if 'yes' in end:
                    break

        end = input("To end type yes: ")

        if 'yes' in end:
            if UserId !=None:
                print("User id is not none",UserId)
                # UserId = str(UserId)
                for a in Actions.objects.all():
                    if a.UserID._id == UserId:
                        print(f'{a.UserID.user_name} said {a.ActionType}')
                    else:
                        pass
                        # print(a.UserID._objectid,UserId)
                        # for User in a.UserID:
                        #     print(a.UserID._id)
            break


start()


