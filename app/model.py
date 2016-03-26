from app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.pool import Pool
from sqlalchemy import (
  event, exc, Integer,
  Column, String, Boolean,
  DateTime, ForeignKey, Table
)

class Workout(db.Model):
  __tablename__ = 'workout'
  id = Column(Integer, primary_key=True)
  wrkout_title = Column (String(1024), nullable=True)
  description = Column(String(1024), nullable=True)
  created_on = Column(DateTime, default=datetime.utcnow)
  modified_on = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  def __repr__(self):
    return '<User %r>' % (self.wrkout_title)

class Exercises(db.Model):
  __tablename__ = 'exercises'
  id = Column(Integer, primary_key=True)
  exercise_name = Column(String(1024), nullable=True)
  description = Column(String(1024), nullable=True)
  created_on = Column(DateTime, default=datetime.utcnow)
  modified_on = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Workout_Exercises(db.Model):
  __tablename__ = 'workout_exercises'
  id = Column(Integer, primary_key=True)
  exercise_id = Column(Integer, ForeignKey('exercises.id'))
  workout_id = Column(Integer, ForeignKey('workout.id'))
  day = Column(Integer, nullable=True)
  week = Column(Integer, nullable=True)
  circuit = Column(Integer, nullable=True)
  reps = Column(Integer, nullable=True)
  sets = Column(Integer, nullable=True)
  notes = Column(String(2048), nullable=True)
  created_on = Column(DateTime, default=datetime.utcnow)
  modified_on = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)