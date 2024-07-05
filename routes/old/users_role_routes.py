from flask import Blueprint, jsonify, request
import sys
import os
from repositories.Repo import *
from playhouse.shortcuts import model_to_dict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

users_role_blueprint = Blueprint('users_role', __name__)

@users_role_blueprint.route('/api/users_role', methods=['POST'])
def create_users_role():
    data = request.json
    new_users_role = users_role_repo.create(**data)
    return jsonify(model_to_dict(new_users_role)), 201

@users_role_blueprint.route('/api/users_role', methods=['GET'])
def get_all_users_roles():
    users_roles = users_role_repo.read_all()
    return jsonify(users_roles)

@users_role_blueprint.route('/api/users_role/<int:users_role_id>', methods=['GET'])
def get_users_role_by_id(users_role_id):
    users_role = users_role_repo.read_by_id(users_role_id)
    if users_role:
        return jsonify(users_role)
    else:
        return jsonify({'error': 'users_role not found'}), 404

@users_role_blueprint.route('/api/users_role/<int:users_role_id>', methods=['PUT'])
def update_users_role(users_role_id):
    data = request.json
    updated_users_role = users_role_repo.update(users_role_id, **data)
    if updated_users_role:
        return jsonify(updated_users_role)
    else:
        return jsonify({'error': 'users_role not found'}), 404

@users_role_blueprint.route('/api/users_role/<int:users_role_id>', methods=['DELETE'])
def delete_users_role(users_role_id):
    users_role_repo.delete(users_role_id)
    return '', 204
