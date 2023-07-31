# app/models/progress.py

from app import db

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('progress', lazy=True))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    lesson = db.relationship('Lesson', backref=db.backref('progress', lazy=True))
    # completed = db.Column(db.Boolean, default=False)
    is_completed = db.Column(db.Boolean, default=False)
    # Add other progress fields as needed

    def __repr__(self):
        return f"<Progress user_id={self.user_id}, lesson_id={self.lesson_id}, completed={self.completed}>"

