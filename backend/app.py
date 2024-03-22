import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler

# ROOT_PATH for linking with all your files. 
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
LOCAL_MYSQL_USER = "root"
LOCAL_MYSQL_USER_PASSWORD = "new_password"
LOCAL_MYSQL_PORT = 3306
LOCAL_MYSQL_DATABASE = "fashion_db"

mysql_engine = MySQLDatabaseHandler(LOCAL_MYSQL_USER,LOCAL_MYSQL_USER_PASSWORD,LOCAL_MYSQL_PORT,LOCAL_MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

app = Flask(__name__)
CORS(app)

# Sample search, the LIKE operator in this case is hard-coded, 
# but if you decide to use SQLAlchemy ORM framework, 
# there's a much better and cleaner way to do this
def sql_search(names):
    query_sql = f"""SELECT Tagline, Description, Name FROM aritzia_tshirts_and_tops WHERE LOWER( Description ) LIKE '%%{input.lower()}%%' limit 10"""
    query_sql = f"""SELECT * FROM fashion_db"""
    keys = ["Name","Price","Tagline","Description"]
    data = mysql_engine.query_selector(query_sql)
    return json.dumps([dict(zip(keys,i)) for i in data])

@app.route("/")
def home():
    return render_template('base.html',title="sample html")

@app.route("/artizia_tshirts_and_tops")
def taglines_search():
    text = request.args.get("Tagline")
    return sql_search(text)

def descriptions_search():
    text = request.args.get("Description")
    return sql_search(text)

def names_search():
    text = request.args.get("Name")
    return sql_search(text)

if 'DB_NAME' not in os.environ:
    app.run(debug=True,host="0.0.0.0",port=5000)
