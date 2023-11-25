"""
Module for task-related routes and functionalities.

This module includes routes for getting, creating, updating, and deleting tasks.

Headers:
    Authorization: Bearer <access_token>
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId
from ..extensions import mongo
from ..models import Task

tasks = Blueprint('tasks', __name__)


# Endpoint for getting tasks associated with the current user.
@tasks.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    """
    Endpoint to retrieve tasks associated with the current user.

    Returns:
        JSON: List of tasks in JSON format.
    """
    user_tasks = Task.objects(user_id=current_user.id)
    tasks_data = [{'title': task.title, 'description': task.description, 'completed': task.completed} for task in user_tasks]
    return jsonify(tasks_data)


#  Endpoint for creating a new task.
@tasks.route('/tasks', methods=['POST'])
@login_required
def create_task():
    """
    Endpoint to create a new task for the current user.

    Returns:
        JSON: Confirmation message.
    """
    data = request.json
    task = Task(title=data.get('title'), description=data.get('description'), user_id=current_user.id)
    task.save()
    return jsonify({'message': 'Task created successfully'})


# Endpoint for updating an existing task.
@tasks.route('/tasks/<string:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    """
    Endpoint to update an existing task for the current user.

    Returns:
        JSON: Confirmation message.
    """
    data = request.json
    task = Task.objects.get_or_404(id=ObjectId(task_id), user_id=current_user.id)
    task.update(**data)
    return jsonify({'message': 'Task updated successfully'})


# Endpoint for deleting an existing task.
@tasks.route('/tasks/<string:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    """
    Endpoint to delete an existing task for the current user.

    Returns:
        JSON: Confirmation message.
    """
    task = Task.objects.get_or_404(id=ObjectId(task_id), user_id=current_user.id)
    task.delete()
    return jsonify({'message': 'Task deleted successfully'})
