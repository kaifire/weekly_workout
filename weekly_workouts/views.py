from weekly_workouts import app, db, api
from flask import render_template, request, redirect, url_for, flash
from model import Workout, Exercises, Workout_Exercises
from flask_restplus import Resource, fields
import json

wo = api.namespace('workouts', description='Workouts!')
ex = api.namespace('exercises', description='Exercises!')
we = api.namespace('workout_exercises', description='Workout Exercises!')

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
  @api.marshal_with(model, code=200, description="Add New Workout")
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

  @api.doc(parser=post_parser)
  @api.marshal_with(model, code=200, description="Workout update")
  def put(self, workout_id):
    args = self.post_parser.parse_args()
    workout_title = args.get('workout_title')
    description = args.get('description')
    try:
      updated_workout = Workout.query.get(workout_id)
      if workout_title is not None:
        updated_workout.wrkout_title = workout_title
      if description is not None:
        updated_workout.description = description
      db.session.merge(updated_workout)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      print "there was an exception!!  Rolling back"
      print "Exception: {0}".format(e)
      return "There was an exception {0}".format(e), 401
    return {'id': workout_id, 'workout_title': workout_title, 'description': description}


@ex.route('/')
class ExerciseList(Resource):
  def get(self):
    all_exercises = {}
    all_db_exercies = Exercises.query.all()
    for exercises in all_db_exercies:
      all_exercises[exercises.exercise_name] = format_workout(exercises)
    return all_exercises

@ex.route('/<int:exercise_id>')
class Exercise(Resource):
  model = api.model('Exercise',{
    "exercise_title": fields.String(required=False, description="Exercise title"),
    "description": fields.String(required=False, description="Exercise description")
  })
  post_parser = api.parser()
  post_parser.add_argument('exercise_title', type=str, help=model['exercise_title'].description, required=False, location='form')
  post_parser.add_argument('description', type=str, help=model['description'].description, required=False, location='form')
  def get(self, exercise_id):
    exercise_return = {}
    got_exercise = Exercises.query.get(exercise_id)
    # exercise_return[got_exercise.wrkout_title] = format_exercise(got_exercise)
    return exercise_return

  @api.doc(parser=post_parser)
  @api.marshal_with(model, code=200, description="Add New Exercise")
  def post(self, exercise_id):
    args = self.post_parser.parse_args()
    exercise_title = args.get('exercise_title')
    description = args.get('description')
    new_exercise = Exercises(exercise_id, exercise_title, description)
    try:
      db.session.add(new_exercise)
      db.session.flush()
      db.session.commit()
    except Exception as e:
      db.session.rollback()
    return {'id': exercise_id, 'exercise_title': exercise_title, 'description': description}

  @api.doc(parser=post_parser)
  @api.marshal_with(model, code=200, description="Exercise update")
  def put(self, exercise_id):
    args = self.post_parser.parse_args()
    exercise_title = args.get('exercise_title')
    description = args.get('description')
    try:
      updated_exercise = Exercises.query.get(exercise_id)
      if exercise_title is not None:
        updated_exercise.wrkout_title = exercise_title
      if description is not None:
        updated_exercise.description = description
      db.session.merge(updated_exercise)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      print "there was an exception!!  Rolling back"
      print "Exception: {0}".format(e)
      return "There was an exception {0}".format(e), 401
    return {'id': exercise_id, 'exercise_title': exercise_title, 'description': description}

@we.route('/<int:workout_exercise_id>')
class WorkoutExercises(Resource):
  model = api.model('Exercise',{
    "exercise_id": fields.Integer(required=True, description="Exercise ID"),
    "workout_id": fields.Integer(required=True, description="Workout ID"),
    "day": fields.Integer(required=False, descrption="A Day, 1-7"),
    "week": fields.Integer(required=False, descrption="Which Week to do the exercise"),
    "circuit": fields.Integer(required=False, descrption="Which circuit will the exercise be done?"),
    "reps": fields.Integer(required=False, descrption="Number of reps"),
    "sets": fields.Integer(required=False, descrption="Which circuit will the exercise be done?"),
    "notes": fields.String(required=False, descrption="Anything special about this exercise?")
  })
  post_parser = api.parser()
  post_parser.add_argument('exercise_id', type=int, help=model['exercise_id'].description, required=False, location='form')
  post_parser.add_argument('workout_id', type=int, help=model['workout_id'].description, required=False, location='form')
  post_parser.add_argument('day', type=int, help=model['day'].description, required=False, location='form')
  post_parser.add_argument('week', type=int, help=model['week'].description, required=False, location='form')
  post_parser.add_argument('circuit', type=int, help=model['circuit'].description, required=False, location='form')
  post_parser.add_argument('reps', type=int, help=model['reps'].description, required=False, location='form')
  post_parser.add_argument('sets', type=int, help=model['sets'].description, required=False, location='form')
  post_parser.add_argument('notes', type=str, help=model['notes'].description, required=False, location='form')
  def get(self, workout_exercise_id):
    # list all exercises associated with a workout
    get_workout_exercises = Workout_Exercises.query.get(workout_exercise_id)
    try:
        w_exercise = Exercises.query.get(get_workout_exercises.exercise_id)
        workout = Workout.query.get(get_workout_exercises.workout_id)
        return format_workout_exercises(get_workout_exercises, w_exercise, workout)
    except Exception as e:
        print "There was a problem getting exercise or workout"
        return False


  @api.doc(parser=post_parser)
  @api.marshal_with(model, code=200, description="Add an exercise to a workout")
  def post(self, workout_exercise_id):
    args = self.post_parser.parse_args()
    exercise_id = args.get('exercise_id')
    workout_id = args.get('workout_id')
    day = args.get('day')
    week = args.get('week')
    circuit = args.get('circuit')
    reps = args.get('reps')
    sets = args.get('sets')
    notes = args.get('notes')
    new_workout_exercise = Workout_Exercises(workout_exercise_id,
                                             exercise_id,
                                             workout_id,
                                             day,
                                             week,
                                             circuit,
                                             reps,
                                             sets,
                                             notes)
    try:
      db.session.add(new_workout_exercise)
      db.session.flush()
      db.session.commit()
    except Exception as e:
      db.session.rollback()
    return {'id': workout_exercise_id, 'exercise_id': exercise_id, 'workout_id': workout_id}

  @api.doc(parser=post_parser)
  @api.marshal_with(model, code=200, description="Add an exercise to a workout")
  def put(self, workout_exercise_id):
    args = self.post_parser.parse_args()
    exercise_id = args.get('exercise_id')
    workout_id = args.get('workout_id')
    day = args.get('day')
    week = args.get('week')
    circuit = args.get('circuit')
    reps = args.get('reps')
    sets = args.get('sets')
    notes = args.get('notes')
    try:
      updated_workout_exercise = Workout_Exercises.query.get(workout_exercise_id)
      w_exercise = Exercises.query.get(updated_workout_exercise.exercise_id)
      workout = Workout.query.get(updated_workout_exercise.workout_id)
      updated_workout_exercise.exercise_id = exercise_id
      updated_workout_exercise.workout_id = workout_id
      updated_workout_exercise.day = day
      updated_workout_exercise.week = week
      updated_workout_exercise.circuit = circuit
      updated_workout_exercise.reps = reps
      updated_workout_exercise.sets = sets
      updated_workout_exercise.notes = notes
      db.session.merge(updated_workout_exercise)
      db.session.commit()
    except Exception as e:
      print "There was an exception {0}".format(e)
      db.session.rollback()
    return format_workout_exercises(updated_workout_exercise, w_exercise, workout)

@we.route('/workout/<int:workout_id>')
class WorkoutExercisesList(Resource):
    def get(self, workout_id):
      all_exercises = Workout_Exercises.query.get(workout_id)
      return True



def format_workout(workout_object):
  return {'id': workout_object.id, 'description': workout_object.description}

def format_workout_exercises(workout_exercise_object, exercise_object, workout_object):
    return {'id': workout_exercise_object.id,
            'exercise name': exercise_object.exercise_name,
            'workout name': workout_object.wrkout_title,
            'exercise_id': workout_exercise_object.exercise_id,
            'workout_id': workout_exercise_object.workout_id,
            'day': workout_exercise_object.day,
            'week': workout_exercise_object.week,
            'circuit': workout_exercise_object.circuit,
            'reps': workout_exercise_object.reps,
            'sets': workout_exercise_object.sets,
            'notes': workout_exercise_object.notes}
