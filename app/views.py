from app import app
from flask import render_template, request, redirect, url_for, flash
from model import Workout, Exercises

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/workouts')
def workouts():
    all_workouts = Workout.query.all()
    return render_template('workout_list.html', all_workouts=all_workouts)

@app.route('/workouts/<int:workout_id>')
def workout_exercises(workout_id):
  workout_id = workout_id
  return render_template('workout_exercises.html', workout_id=workout_id)