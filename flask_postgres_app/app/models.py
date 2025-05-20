from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

task_dependencies = db.Table(
    'task_dependencies',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
    db.Column('depends_on_id', db.Integer, db.ForeignKey('task.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    tasks = db.relationship('Task', backref='assignee', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'

class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)

    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Project {self.name}>'

class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(
        db.String(20),
        nullable=False,
        default='pending'
    ) 

    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    dependencies = db.relationship(
        'Task',
        secondary=task_dependencies,
        primaryjoin=id == task_dependencies.c.task_id,
        secondaryjoin=id == task_dependencies.c.depends_on_id,
        backref='dependents'
    )

    def __repr__(self):
        return f'<Task {self.title} - {self.status}>'
