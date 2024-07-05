from flask import Blueprint, jsonify, request
import sys
import os
from repositories.Repo import *
from playhouse.shortcuts import model_to_dict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/api/users', methods=['POST'])
def create_users():
    data = request.json
    new_users = users_repo.create(**data)
    return jsonify(model_to_dict(new_users)), 201

@users_blueprint.route('/api/users', methods=['GET'])
def get_all_userss():
    userss = users_repo.read_all()
    return jsonify(userss)

@users_blueprint.route('/api/users/<int:users_id>', methods=['GET'])
def get_users_by_id(users_id):
    users = users_repo.read_by_id(users_id)
    if users:
        return jsonify(users)
    else:
        return jsonify({'error': 'users not found'}), 404

@users_blueprint.route('/api/users/<int:users_id>', methods=['PUT'])
def update_users(users_id):
    data = request.json
    updated_users = users_repo.update(users_id, **data)
    if updated_users:
        return jsonify(updated_users)
    else:
        return jsonify({'error': 'users not found'}), 404

@users_blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    users_repo.delete(users_id)
    return '', 204
