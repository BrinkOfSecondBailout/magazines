from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.controllers import users
from flask_app.models import user
from flask_app import app
from flask import flash, session

class Magazine:
    def __init__(self, data):
        self.magazine_id = data['magazine_id']
        self.name = data['name']
        self.descriptions = data['descriptions']
        self.num_of_subscribers = data['num_of_subscribers']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @staticmethod
    def validate_magazine(data):
        is_valid = True
        if len(data['name']) < 2:
            flash('Title must be at least 2 characters!', 'magazine')
            is_valid = False
        if len(data['descriptions']) < 10:
            flash('Descriptions must be at least 10 characters!', 'magazine')
            is_valid = False
        return is_valid

    @classmethod
    def validate_matching_id(cls, data):
        query = 'SELECT * FROM magazines WHERE magazine_id = %(magazine_id)s;'
        results = connectToMySQL('subscriptions_schema').query_db(query, data)
        my_magazine = results[0]
        if session['user_id'] != my_magazine['user_id']:
            return False
        else:
            return True

    @classmethod
    def add_new_magazine(cls, data):
        query = 'INSERT INTO magazines (name, descriptions, user_id) VALUES (%(name)s, %(descriptions)s, %(user_id)s);'
        return connectToMySQL('subscriptions_schema').query_db(query, data)

    @classmethod
    def show_all_magazines(cls):
        query = 'SELECT * FROM magazines JOIN users ON magazines.user_id = users.id;'
        results = connectToMySQL('subscriptions_schema').query_db(query)
        all_magazines = []
        for row in results:
            one_magazine = cls(row)
            one_magazines_creator_info = {
                'id': row['id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
            }
            creator1 = user.User(one_magazines_creator_info)
            one_magazine.creator = creator1
            all_magazines.append(one_magazine)
        return all_magazines

    @classmethod
    def show_one_magazine(cls, data):
        query = 'SELECT * FROM magazines JOIN users ON magazines.user_id = users.id WHERE magazines.magazine_id = %(magazine_id)s;'
        results = connectToMySQL('subscriptions_schema').query_db(query, data)
        one_magazine = cls(results[0])
        row = results[0]
        one_magazines_creator_info = {
            'id': row['id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': row['password'],
            'created_at': row['created_at'],
            'updated_at': row['updated_at'],
        }
        creator1 = user.User(one_magazines_creator_info)
        one_magazine.creator = creator1
        return one_magazine

    @classmethod
    def add_subscriber(cls, data):
        query = 'INSERT INTO subscriptions (subscriber_id, magazine_id) VALUES (%(subscriber_id)s, %(magazine_id)s);'
        return connectToMySQL('subscriptions_schema').query_db(query, data)

    @classmethod
    def update_subscriber_count(cls, data):
        query = 'UPDATE magazines SET num_of_subscribers = num_of_subscribers + 1 WHERE magazine_id = %(magazine_id)s;'
        return connectToMySQL('subscriptions_schema').query_db(query, data)

    @classmethod
    def get_all_subscribers_by_mag_id(cls, data):
        query = 'SELECT * FROM users JOIN subscriptions ON users.id = subscriptions.subscriber_id WHERE subscriptions.magazine_id = %(magazine_id)s;'
        results = connectToMySQL('subscriptions_schema').query_db(query, data)
        all_subscribers = []
        for row in results:
            one_subscriber_user_info = {
                'id': row['id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
            }
            subscriber1 = user.User(one_subscriber_user_info)
            all_subscribers.append(subscriber1)
        return all_subscribers

    @classmethod
    def get_all_magazines_by_user(cls, data):
        query = 'SELECT * FROM magazines WHERE magazines.user_id = %(id)s;'
        results = connectToMySQL('subscriptions_schema').query_db(query, data)
        all_magazines = []
        for row in results:
            one_magazine = cls(row)
            all_magazines.append(one_magazine)
        return all_magazines

    @classmethod
    def disable_foreign_key(cls):
        query = 'SET FOREIGN_KEY_CHECKS=0;'
        return connectToMySQL('subscriptions_schema').query_db(query)

    @classmethod
    def destroy_magazine(cls, data):
        query = 'DELETE FROM magazines WHERE magazine_id = %(magazine_id)s LIMIT 1;'
        return connectToMySQL('subscriptions_schema').query_db(query, data)
