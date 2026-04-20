from flask import Flask, render_template,request
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
#from zipfile import SizeFileHeader

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mushi01695'
app.config['MYSQL_DB'] = 'student_election'

app.config['SECRET_KEY']='65d38f6e381f7d4ebef212db'
app.config['UPLOAD_FOLDER']= 'static/uploads'

mysql = MySQL(app)

from election import routes
