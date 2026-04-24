from flask import Flask
from flask_mysqldb import MySQL
import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'mysql.railway.internal'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'HwKpHgXmdRCIHwsjTqnPuzEcTmaVEEmt'
app.config['MYSQL_DB'] = 'railway'

app.config['SECRET_KEY']='65d38f6e381f7d4ebef212db'
app.config['UPLOAD_FOLDER']= 'static/uploads'

mysql = MySQL(app)

from election import routes
