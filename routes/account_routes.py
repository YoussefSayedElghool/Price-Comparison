from flask import Blueprint, jsonify, request , render_template, redirect, session , url_for
import repositories.Repo as repo   
from playhouse.shortcuts import model_to_dict
import re

# from google.oauth2 import id_token
# from google.auth.transport import requests

account_blueprint = Blueprint('account', __name__)


@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = repo.users_repo.verify_user(email, password)
        if user:
            session['user_id'] = user.user_id
            session['email'] = user.email
            # Redirect to home page after successful login
            return redirect('/')
        else:
            return render_template('Acounting.html', error='Invalid email or password')

    return render_template('Acounting.html')

@account_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        if not name or not phone or not email or not password or not confirmPassword:
            return render_template('Acounting.html', error="Missing required fields"), 400
        
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$'
        is_valid_password = bool(re.match(pattern, password))
        
        if password != confirmPassword:
            return render_template('Acounting.html', error="Password field not equal Confirm Password field" , name=name , phone=phone , email=email), 400


        error ="""
        Must be between 8 and 16 characters.\n
        Must contain at least one lowercase letter (a-z).\n
        Must contain at least one uppercase letter (A-Z).\n
        Must contain at least one digit (0-9).\n
        Must contain at least one special character @$!%*?&\n
        """
        if not is_valid_password:
            return render_template('Acounting.html', error=error , name=name , phone=phone , email=email), 400

        try:
            new_user = repo.users_repo.register(name, phone, email, password)
            session['user_id'] = new_user.user_id
            session['email'] = new_user.email
            return redirect('/')
        except Exception as e:
            return render_template('Acounting.html')

    return render_template('Acounting.html')



@account_blueprint.route('/logout')
def logout():
    session.clear()
    return render_template('Acounting.html')





# @account_blueprint.route('/api/users/gsingin', methods=['POST'])
# def singIn_with_google():
#     data = request.json
#     token = data['idToken']

#     try:
#         idinfo = verify_token(token)

#         isExist = Repo.check_user_existence(idinfo['sub'])

#         if not isExist:
#             new_products = products_repo.create(**data)
#             # return jsonify(model_to_dict(new_products)), 201
#             Repo.insert_user(idinfo['sub'], idinfo['given_name'],
#                              idinfo['family_name'], idinfo['picture'], idinfo['email'])

#             response_data = {
#                 'message': 'user added seuccessfully '}
#             response = json.dumps(
#                 response_data, ensure_ascii=False).encode('utf-8')

#             return response, 200

#     except ValueError:
#         # Invalid token
#         return "Invalid token"





# def verify_token(token: str):
#     try:
#         idinfo = id_token.verify_oauth2_token(token, requests.Request())
#         if idinfo['iss'] == "https://accounts.google.com" and bool(idinfo['email_verified']):
#             return idinfo
#         else:
#             raise "this user mayby haker"
#     except ValueError as e:
#         raise e

