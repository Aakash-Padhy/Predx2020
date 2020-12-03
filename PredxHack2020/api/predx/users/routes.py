from flask import render_template, url_for, flash, redirect, request, Blueprint,jsonify
import jwt
from flask_login import login_user, current_user, logout_user, login_required
from predx import db, bcrypt
from predx.models import User, Post
from predx.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,RequestResetForm, ResetPasswordForm)
from predx.users.utils import save_picture, send_reset_email
from predx import token_required

users = Blueprint('users', __name__)


@users.route("/register",methods=["POST"])    
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


@users.route("/login",methods=["POST"])
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


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/login/user',methods=['GET'])
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