from flask import Blueprint , request , render_template, session
from loginRequired import login_required 
from flask_caching import Cache


views_blueprint = Blueprint('views', __name__)


@views_blueprint.route('/searchPage', methods=['GET'])
def to_search_page():
    query = request.args.get('query')
    email = session.get('email')
    return render_template('Products.html', query = query , email = email ), 200


@views_blueprint.route('/')
@login_required
def home():
    email = session.get('email')
    return render_template('Home.html' , email = email )


@views_blueprint.route('/wishlist')
def to_wishlist_page():
    email = session.get('email')
    return render_template('Wishlist.html' ,email = email)
