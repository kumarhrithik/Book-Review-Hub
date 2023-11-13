from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId
from ..extensions import mongo
from ..models import Task

tasks = Blueprint('tasks', __name__)

@tasks.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    user_tasks = Task.objects(user_id=current_user.id)
    tasks_data = [{'title': task.title, 'description': task.description, 'completed': task.completed} for task in user_tasks]
    return jsonify(tasks_data)

@tasks.route('/tasks', methods=['POST'])
@login_required
def create_task():
    data = request.json
    task = Task(title=data.get('title'), description=data.get('description'), user_id=current_user.id)
    task.save()
    return jsonify({'message': 'Task created successfully'})

@tasks.route('/tasks/<string:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    data = request.json
    task = Task.objects.get_or_404(id=ObjectId(task_id), user_id=current_user.id)
    task.update(**data)
    return jsonify({'message': 'Task updated successfully'})

@tasks.route('/tasks/<string:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.objects.get_or_404(id=ObjectId(task_id), user_id=current_user.id)
    task.delete()
    return jsonify({'message': 'Task deleted successfully'})
