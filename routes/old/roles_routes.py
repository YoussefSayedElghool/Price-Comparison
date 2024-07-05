from flask import Blueprint, jsonify, request
import sys
import os
from repositories.Repo import *
from playhouse.shortcuts import model_to_dict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

roles_blueprint = Blueprint('roles', __name__)

@roles_blueprint.route('/api/roles', methods=['POST'])
def create_roles():
    data = request.json
    new_roles = roles_repo.create(**data)
    return jsonify(model_to_dict(new_roles)), 201

@roles_blueprint.route('/api/roles', methods=['GET'])
def get_all_roless():
    roless = roles_repo.read_all()
    return jsonify(roless)

@roles_blueprint.route('/api/roles/<int:roles_id>', methods=['GET'])
def get_roles_by_id(roles_id):
    roles = roles_repo.read_by_id(roles_id)
    if roles:
        return jsonify(roles)
    else:
        return jsonify({'error': 'roles not found'}), 404

@roles_blueprint.route('/api/roles/<int:roles_id>', methods=['PUT'])
def update_roles(roles_id):
    data = request.json
    updated_roles = roles_repo.update(roles_id, **data)
    if updated_roles:
        return jsonify(updated_roles)
    else:
        return jsonify({'error': 'roles not found'}), 404

@roles_blueprint.route('/api/roles/<int:roles_id>', methods=['DELETE'])
def delete_roles(roles_id):
    roles_repo.delete(roles_id)
    return '', 204
