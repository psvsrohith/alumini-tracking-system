import pymongo

myclient=pymongo.MongoClient("mongodb://localhost:27017")
mydb=myclient["alumni"]
mycol=mydb["directorate"]
x=mycol.insert_one({'pass':'654','email':'abhinavmunagala2.o@gmail.com'})
# colleges=[{'account':'Abhi','pass':'654','id':'00','email':'abhinavmunagala4@gmail.com'},{'account':'Rohith','pass':'654','id':'01','email':'princerohith132000@gmail.com'}]
# x=mycol.insert_many(colleges)
# print(x.inserted_ids)
# for x in mycol.find():
# 	print(x)
# mycol.drop()





# from flask import Flask, session
# from flask_session import Session

# app = Flask(__name__)
# # Check Configuration section for more details
# SESSION_TYPE = 'filesystem'
# app.config.from_object(__name__)
# Session(app)

# @app.route('/')
# def reset():
#     session["counter"]=0

#     return "counter was reset"

# @app.route('/inc')
# def routeA():
#     if not "counter" in session:
#         session["counter"]=0

#     session["counter"]+=1

#     return "counter is {}".format(session["counter"])

# @app.route('/dec')
# def routeB():
#     if not "counter" in session:
#         session["counter"] = 0

#     session["counter"] -= 1

#     return "counter is {}".format(session["counter"])

# if __name__ == '__main__':
#     app.run()
















import pymongo
client=pymongo.MongoClient("mongodb://localhost:27017")
db=client['alumni']
posts=db['posts']
x=posts.find()
for y in x:
    print(x['id'])