from flask import Blueprint, request, jsonify
from app.models import db, User, Project, Task
from app.logic import can_mark_task_completed, has_circular_dependency, can_delete_user
from app.auth import generate_token, token_required

bp = Blueprint('api', __name__)

### ---------------- AUTH ---------------- ###

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    token = generate_token(user.id)
    return jsonify({'token': token})


### ---------------- USER ROUTES ---------------- ###

@bp.route('/users', methods=['POST'])  # Public: user registration
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created', 'id': user.id}), 201

@bp.route('/users', methods=['GET'])  
def list_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email} for u in users]), 200

@bp.route('/users/<int:user_id>', methods=['GET'])  
@token_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 200

@bp.route('/users/<int:user_id>', methods=['DELETE']) 
@token_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if not can_delete_user(user):
        return jsonify({'error': 'User has pending or in-progress tasks'}), 400

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200


### ---------------- PROJECT ROUTES ---------------- ###

@bp.route('/projects', methods=['POST']) 
@token_required
def create_project():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    project = Project(name=name, description=description)
    db.session.add(project)
    db.session.commit()
    return jsonify({'message': 'Project created', 'id': project.id}), 201

@bp.route('/projects', methods=['GET'])  
@token_required
def list_projects():
    projects = Project.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'description': p.description} for p in projects]), 200

@bp.route('/projects/<int:project_id>', methods=['GET'])  
@token_required
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify({'id': project.id, 'name': project.name, 'description': project.description}), 200

@bp.route('/projects/<int:project_id>/tasks', methods=['GET'])  
@token_required
def list_project_tasks(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'status': t.status,
        'assignee': t.assignee.name if t.assignee else None
    } for t in project.tasks]), 200


### ---------------- TASK ROUTES ---------------- ###

@bp.route('/projects/<int:project_id>/tasks', methods=['POST'])  
@token_required
def create_task(project_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    status = data.get('status', 'pending')
    assignee_id = data.get('assignee_id')
    dependency_ids = data.get('dependency_ids', [])

    if status not in ('pending', 'in-progress', 'completed'):
        return jsonify({'error': 'Invalid status value'}), 400

    project = Project.query.get_or_404(project_id)
    assignee = User.query.get(assignee_id) if assignee_id else None
    dependencies = Task.query.filter(Task.id.in_(dependency_ids)).all() if dependency_ids else []

    task = Task(title=title, description=description, status=status,
                assignee=assignee, project=project, dependencies=dependencies)

    if has_circular_dependency(task, dependencies):
        return jsonify({'error': 'Circular dependency detected'}), 400

    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task created', 'id': task.id}), 201

@bp.route('/tasks/<int:task_id>', methods=['GET'])  
@token_required
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify({
        'id': task.id,
        'title': task.title,
        'status': task.status,
        'assignee': task.assignee.name if task.assignee else None,
        'project': task.project.name,
        'dependencies': [d.id for d in task.dependencies]
    }), 200

@bp.route('/tasks/<int:task_id>/status', methods=['PATCH'])  
@token_required
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    new_status = data.get('status')

    if new_status not in ('pending', 'in-progress', 'completed'):
        return jsonify({'error': 'Invalid status'}), 400

    if new_status == 'completed' and not can_mark_task_completed(task):
        return jsonify({'error': 'Cannot mark task as completed. Dependencies incomplete.'}), 400

    task.status = new_status
    db.session.commit()
    return jsonify({'message': 'Status updated'}), 200

@bp.route('/users/<int:user_id>/tasks', methods=['GET'])  
@token_required
def list_user_tasks(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'status': t.status,
        'project': t.project.name
    } for t in user.tasks]), 200

@bp.route('/tasks', methods=['GET'])  
@token_required
def list_tasks_by_status():
    status = request.args.get('status')
    if status not in ('pending', 'in-progress', 'completed'):
        return jsonify({'error': 'Invalid or missing status'}), 400

    tasks = Task.query.filter_by(status=status).all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'assignee': t.assignee.name if t.assignee else None,
        'project': t.project.name
    } for t in tasks]), 200
