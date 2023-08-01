# app/models/course.py

from app import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100))
    # Add other course fields as needed

    def __repr__(self):
        return f"<Course {self.title}>"

