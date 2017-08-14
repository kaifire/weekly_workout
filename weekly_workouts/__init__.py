from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
import os

app = Flask(__name__)
api = Api(app)
#app.config.from_object('config')
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from weekly_workouts import views, model

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')
