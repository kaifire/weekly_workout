from weekly_workouts import app, db, api
from flask import render_template, request, redirect, url_for, flash
from model import Workout, Exercises
from flask_restplus import Resource, fields
import json

wo = api.namespace('workouts', description='Workouts!')
ex = api.namespace('exercises', description='Exercises!')

@wo.route('/')
class WorkoutList(Resource):
  def get(self):
    all_workouts = {}
    all_db_workouts = Workout.query.all()
    for workouts in all_db_workouts:
      all_workouts[workouts.wrkout_title] = format_workout(workouts)
    return all_workouts

@wo.route('/<int:workout_id>')
class Workouts(Resource):
  model = api.model('Workout',{
    "workout_title": fields.String(required=False, description="Workout title"),
    "description": fields.String(required=False, description="Workout description")
  })
  post_parser = api.parser()
  post_parser.add_argument('workout_title', type=str, help=model['workout_title'].description, required=False, location='form')
  post_parser.add_argument('description', type=str, help=model['description'].description, required=False, location='form')
  def get(self, workout_id):
    work_return = {}
    got_workout = Workout.query.get(workout_id)
    work_return[got_workout.wrkout_title] = format_workout(got_workout)
    return work_return
  @api.doc(parser=post_parser)
  @api.marshal_with(model, code=200, description="Workout update")
  def post(self, workout_id):
    args = self.post_parser.parse_args()
    workout_title = args.get('workout_title')
    description = args.get('description')
    new_workout = Workout(workout_id, workout_title, description)
    try:
      db.session.add(new_workout)
      db.session.flush()
      db.session.commit()
    except Exception as e:
      db.session.rollback()
    return {'id': workout_id, 'workout_title': workout_title, 'description': description}

@ex.route('/')
class ExerciseList(Resource):
  def get(self):
    all_exercises = {}
    all_db_exercies = Exercises.query.all()
    for exercises in all_db_exercies:
      all_exercises[exercises.exercise_name] = format_workout(exercises)
    return all_exercises

def format_workout(workout_object):
  return {'id': workout_object.id, 'description': workout_object.description}

# @app.route('/workouts')
# def workouts():
#     all_workouts = Workout.query.all()
#     return render_template('workout_list.html', all_workouts=all_workouts)

# @app.route('/workouts/<int:workout_id>')
# def workout_exercises(workout_id):
#   workout_id = workout_id
#   return render_template('workout_exercises.html', workout_id=workout_id)

# @app.route('/add_items')
# def add_items():
#   return render_template('add_items.html')

# @app.route('/add_workout', methods=['GET', 'POST'])
# def add_workout():
#   if request.method == 'GET':
#     all_workouts = Workout.query.all()
#     print all_workouts
#     return render_template('add_workout.html', all_workouts=all_workouts)
#   elif request.method == 'POST':
#     try:
#       new_workout = Workout(wrkout_title=request.form['workout_title'], description=request.form['workout_description'])
#       db.session.add(new_workout)
#       db.session.commit()
#       all_workouts = Workout.query.all()
#     except e:
#       db.session.rollback()
#       print "there was an exception that happened"
#     return render_template('add_workout.html', all_workouts=all_workouts)

# @app.route('/add_exercise', methods=['GET', 'POST'])
# def add_exercise():
#   if request.method == 'GET':
#     return render_template('add_exercise.html')
#   elif request.method == 'POST':
#     try:
#       new_exercise = Exercises(exercise_name=request.form['exercise_name'], description=request.form['exercise_description'])
#       db.session.add(new_exercise)
#       db.session.commit()
#     except e:
#       db.session.rollback()
#       print "there was an exception that happened"
#   return render_template('add_exercise.html')

# @app.route('/add_program', methods=['GET', 'POST'])
# def add_program():
#   workout_list = Workout.query.all()
#   exercise_list = Exercises.query.all()
#   if request.method == 'GET':
#     return render_template('add_program.html', workout_list=workout_list, exercise_list=exercise_list)
#   elif request.method == 'POST':
#     selected = request.form.get('workout_list')
#     print str(selected)
#   return render_template('add_program.html', workout_list=workout_list, exercise_list=exercise_list)
