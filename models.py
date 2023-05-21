from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime
db = SQLAlchemy()
#comandos para usar mysql 
# mysql -u root -p
# jetgrande2022A!
# create database flask;
# use flask

# https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
# tutorial

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50), unique=True)
    admin=db.Column(db.Boolean(),default=False)
    email=db.Column(db.String(40))
    password=db.Column(db.String(200))
    comments = db.relationship('Comment')
    create_date=db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self,username, password,email):
        self.username = username
        self.password = self.__create_password(password)
        self.email = email
        
    def __create_password(self, password):
        return generate_password_hash(password, salt_length=8)
    
    def verify_password(self, password):
        return check_password_hash(self.password,password)
    
class Comment(db.Model):
    __tablename__='comments'

    id = db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Text())
    imageURL = db.Column(db.Text())
    create_date=db.Column(db.DateTime, default=datetime.datetime.now)

class Products(db.Model):
    __tablename__='products'
    
    id = db.Column(db.Integer,primary_key=True)
    product_name=db.Column(db.Text())
    regular_price=db.Column(db.Float())
    offer_price=db.Column(db.Float())
    on_offer=db.Column(db.Boolean(),default=False)
    imageURL = db.Column(db.Text())
    create_date=db.Column(db.DateTime, default=datetime.datetime.now)

class Orders(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    money=db.Column(db.Float())

