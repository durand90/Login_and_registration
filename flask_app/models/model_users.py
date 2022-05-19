from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_app import bcrypt, DATABASE


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw = data['pw']
        self.confirm_pw = data['confirm_pw']
        self.fullname = f'{self.first_name} {self.last_name}'

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, pw, confirm_pw) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw)s, %(confirm_pw)s);"
        users_id = connectToMySQL(DATABASE).query_db(query, data)
        return users_id

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"

        results = connectToMySQL(DATABASE).query_db(query)

        if results:
            users_list = []
            for user in results:
                users_list.append(cls(user))
            return users_list
        return []

    @classmethod
    def get_one(cls, data) -> object:
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def update_one(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, pw = %(pw)s, confirm_pw = %(confirm_pw)s, WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validator(form_data):
        is_valid = True

        if len(form_data['first_name']) < 2:
            is_valid = False
            flash('Must enter First Name', 'err_users_first_name')

        if len(form_data['last_name']) < 2:
            is_valid = False
            flash('Must enter Last Name', 'err_users_last_name')

        if len(form_data['email']) < 4:
            is_valid = False
            flash('Must enter valid Email', 'err_users_email')

        if not EMAIL_REGEX.match(form_data['email']): 
            flash('Invalid email address!', 'err_users_email')
            is_valid = False

        if len(form_data['pw']) < 2:
            is_valid = False
            flash('Must enter Valid Password', 'err_users_pw')

        if len(form_data['confirm_pw']) < 2:
            is_valid = False
            flash('Must enter valid Confirm Password', 'err_users_confirm_pw')

        elif form_data['confirm_pw'] != form_data['pw']:
            is_valid = False
            flash('Passwords do not match', 'err_users_confirm_pw')

        return is_valid

    @staticmethod
    def validator_login(form_data):
        is_valid = True


        if len(form_data['email']) < 4:
            is_valid = False
            flash('Must enter Email', 'err_users_email_login')


        elif not EMAIL_REGEX.match(form_data['email']): 
            flash('Invalid email address!', 'err_users_email_login')
            is_valid = False

        if len(form_data['pw']) < 2:
            is_valid = False
            flash('Must enter Valid Password', 'err_users_pw_login')

        else:
            potential_user = User.get_one_by_email({'email': form_data['email']})
        
            if not potential_user:
                print(potential_user)
                is_valid = False
                flash("User does't exist, Create User", "err_users_pw_login")

            elif not bcrypt.check_password_hash(potential_user.pw, form_data['pw']):
                is_valid = False
                flash('Wrong Password', 'err_users_pw_login')

            else:
                session['uuid'] = potential_user.id

            return is_valid
