from flask import Flask
import mysql.connector
app = Flask(__name__)

import os

db = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST', 'localhost'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE')
)

app.config['SECRET_KEY']='65d38f6e381f7d4ebef212db'
app.config['UPLOAD_FOLDER']= 'static/uploads'



from election import routes
