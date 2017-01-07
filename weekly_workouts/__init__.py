from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api

app = Flask(__name__)
api = Api(app)
app.config.from_object('config')
db = SQLAlchemy(app)

from weekly_workouts import views, model

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')
