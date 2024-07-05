from flask import Blueprint, jsonify, request , session
import sys
import os
import repositories.Repo as repo
from playhouse.shortcuts import model_to_dict
from loginRequired import login_required 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

cart_blueprint = Blueprint('cart', __name__)


@cart_blueprint.route('/api/cart', methods=['POST'])
@login_required
def create_cart():
    data = request.json
    user_id = session.get('user_id')
    products = repo.products_repo.create(name = data["name"] ,
                                    image = data["image"] ,
                                    link = data["link"] ,
                                    price = data["price"] ,
                                    rating = data["rating"] ,
                                    stars = data["stars"],
                                    source = data["source"])
    cart = repo.cart_repo.create(product_id = products.product_id , user_id = user_id)
    return jsonify(model_to_dict(cart)), 201

@cart_blueprint.route('/api/cart', methods=['GET'])
@login_required
def get_cart():
    user_id = session.get('user_id')
    cart = repo.cart_repo.get_by_user_id(user_id)
    if cart :
        return jsonify([model_to_dict(obj) for obj in cart]), 200
    else:
        return jsonify({'error': 'Cart not found'}), 404

@cart_blueprint.route('/api/cart/<int:cart_id>', methods=['DELETE'])
def delete_cart(cart_id):
    repo.cart_repo.delete(cart_id)
    return '', 204