from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import Relationship

db = SQLAlchemy()


class Hypothesis(db.Model):
    __tablename__ = 'hypothesis'
    id = Column(Integer, primary_key=True)
    user_input = Column(Text)
    predicted_var = Column(Text)
    predicted_graph_str = Column(Text)
    question_id = Column(Integer, ForeignKey('question.id', ondelete="CASCADE"))
    question = Relationship('Question', backref='hypothesis')

    def __str__(self):
        return f"hypothesis id: {self.id}"


class Question(db.Model):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    question_text = Column(Text)
