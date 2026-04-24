from flask import Flask
import mysql.connector
app = Flask(__name__)

import os

app.config['MYSQL_HOST'] = 'mysql.railway.internal'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'HwKpHgXmdRCIHwsjTqnPuzEcTmaVEEmt'
app.config['MYSQL_DB'] = 'railway'

app.config['SECRET_KEY']='65d38f6e381f7d4ebef212db'
app.config['UPLOAD_FOLDER']= 'static/uploads'


db = mysql.connector.connect(
    host=os.environ.get("MYSQLHOST", "mysql.railway.internal"),
    user=os.environ.get("MYSQLUSER", "root"),
    password=os.environ.get("MYSQLPASSWORD", "HwKpHgXmdRCIHwsjTqnPuzEcTmaVEEmt"),
    database=os.environ.get("MYSQLDATABASE", "railway"),
    port=int(os.environ.get("MYSQLPORT", 3306))
)

from election import routes
