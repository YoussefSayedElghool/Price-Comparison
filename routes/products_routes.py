from flask import Blueprint, jsonify, request
import sys
import os
import repositories.Repo as repo  
from playhouse.shortcuts import model_to_dict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


products_blueprint = Blueprint('products', __name__)

@products_blueprint.route('/api/products', methods=['POST'])
def create_products():
    data = request.json
    new_products = repo.products_repo.create(**data)
    return jsonify(model_to_dict(new_products)), 201

@products_blueprint.route('/api/products', methods=['GET'])
def get_all_productss():
    productss = repo.products_repo.read_all()
    return jsonify(productss)

@products_blueprint.route('/api/products/<int:products_id>', methods=['GET'])
def get_products_by_id(products_id):
    products = repo.products_repo.read_by_id(products_id)
    if products:
        return jsonify(products)
    else:
        return jsonify({'error': 'products not found'}), 404

@products_blueprint.route('/api/products/<int:products_id>', methods=['PUT'])
def update_products(products_id):
    data = request.json
    updated_products = repo.products_repo.update(products_id, **data)
    if updated_products:
        return jsonify(updated_products)
    else:
        return jsonify({'error': 'products not found'}), 404

@products_blueprint.route('/api/products/<int:products_id>', methods=['DELETE'])
def delete_products(products_id):
    repo.products_repo.delete(products_id)
    return '', 204
