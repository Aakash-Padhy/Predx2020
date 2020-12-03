from flask import Flask, request, jsonify, make_response ,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from functools import wraps
import jwt
import json
import datetime
import os
import uuid
import base64
import re


app = Flask(__name__)

app.config['SECRET_KEY'] = 'fuckyouall'
CORS(app)
# database name 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object 
db = SQLAlchemy(app) 
ma = Marshmallow(app)
bcrypt = Bcrypt(app)



def token_required(func):
    def wrapper(*args,**kwargs):

        token = request.headers['x-auth-token']

        if not token:
            return jsonify({'message':'Token is missing'})
        
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            request.data = data
        except:
            return jsonify({'message':'invalid token'})
        return func(*args,**kwargs)
    wrapper.__name__ = func.__name__
    return wrapper



from models import User,Post

#auth decorator to act as middleware

@app.route("/",methods=["GET"])
def getpost():
    return jsonify({'message':"something"})

"""@app.route("/allUsers",methods=["GET"])
def printAllUsers():
    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify({"users": result})"""



@app.route("/register",methods=["POST"])    
def register():
    req = request.json
    if(req.get('username') and req.get('email') and req.get('password')):
        # print(req['email'])
        
        user = User.query.filter_by(email= req['email']).first()

        if(user):
            return jsonify({'message':'seems like the email id is already registered'})

        password = bcrypt.generate_password_hash(req['password']).decode('utf-8')
        user1 = User(username=req['username'],email=req['email'],password=password,)
        db.session.add(user1)
        db.session.commit()
        token = jwt.encode({'id':user1.id,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=180)},app.config['SECRET_KEY'])         
        # print("token:"+token.decode('UTF-8'))
        if token:
            resp = {
                'token': token.decode('UTF-8'),
                'user' : {
                'username':user1.username,
                    'email': user1.email,
                    'id' : user1.id
                }
            } 
            return jsonify(resp)
        else:
            return jsonify({'message':'Problem in creating a token'})
    else:
        return jsonify({'message': 'please enter all the values required for the creation of a new user'})
    

@app.route("/login",methods=["POST"])
def login():
    req = request.json

    if(req.get('email') and req.get('password')):

        user = User.query.filter_by(email= req['email']).first()

        if(user):
            if(user and bcrypt.check_password_hash(user.password,req['password'])):
                #things to do after checking the email and password
                token = jwt.encode({'id':user.id,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=180)},app.config['SECRET_KEY'])         
                # print("token:"+token.decode('UTF-8'))
                if token:
                    resp = {
                        'token': token.decode('UTF-8'),
                        'user' : {
                            'username':user.username,
                            'email': user.email,
                            'id' : user.id
                        }
                    } 
                    return jsonify(resp)
                else:
                    return jsonify({'message':'Problem in creating a token'})
            else:
                return jsonify({'message':'it seems that this email is not registered'})
        else:
            return jsonify({'message':'Login Unsuccesful.Please check email and password'})


@app.route('/login/user',methods=['GET'])
@token_required
def protected():
    data = request.data

    user = User.query.get(data['id'])
    if user:
        resp ={
            'username':user.username,
            'email':user.email,
            "id":user.id
        }
        return jsonify(resp)
    else:
        return jsonify({'message':'This is a protected'})

def getApp():
    return app


if __name__ == "__main__":
    app.run(debug=True)