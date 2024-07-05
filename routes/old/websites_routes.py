from flask import Blueprint, jsonify, request
import sys
import os
from repositories.Repo import *
from playhouse.shortcuts import model_to_dict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

websites_blueprint = Blueprint('websites', __name__)

@websites_blueprint.route('/api/websites', methods=['POST'])
def create_websites():
    data = request.json
    new_websites = websites_repo.create(**data)
    return jsonify(model_to_dict(new_websites)), 201

@websites_blueprint.route('/api/websites', methods=['GET'])
def get_all_websitess():
    websitess = websites_repo.read_all()
    return jsonify(websitess)

@websites_blueprint.route('/api/websites/<int:websites_id>', methods=['GET'])
def get_websites_by_id(websites_id):
    websites = websites_repo.read_by_id(websites_id)
    if websites:
        return jsonify(websites)
    else:
        return jsonify({'error': 'websites not found'}), 404

@websites_blueprint.route('/api/websites/<int:websites_id>', methods=['PUT'])
def update_websites(websites_id):
    data = request.json
    updated_websites = websites_repo.update(websites_id, **data)
    if updated_websites:
        return jsonify(updated_websites)
    else:
        return jsonify({'error': 'websites not found'}), 404

@websites_blueprint.route('/api/websites/<int:websites_id>', methods=['DELETE'])
def delete_websites(websites_id):
    websites_repo.delete(websites_id)
    return '', 204
