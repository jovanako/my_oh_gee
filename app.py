import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

database_path = os.getenv('DATABASE_URL', 'DATABASE_URL_WAS_NOT_SET?!')
database_path = database_path.replace('postgres://', 'postgresql://')
app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

if __name__ == '__main__':
  port = int(os.environ.get("PORT",5000))
  app.run(host='127.0.0.1',port=port,debug=True)