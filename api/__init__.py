from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, render_template
from werkzeug.exceptions import HTTPException
from config import config

db = SQLAlchemy()


class ExtendedAPI(Api):
    """
    credit to https://stackoverflow.com/a/57921890
    This class overrides 'handle_error' method of 'Api' class in Flask-RESTful,
    to extend global exception handing functionality
    """
    def handle_error(self, err):  # pragma: no cover
        """
        prevents writing unnecessary try/except block throughout the app
        """
        # log every exception raised in the application
        print('we ended up in the API handle_error()', err, err.__class__)

        # catch other HTTP errors
        if isinstance(err, HTTPException):
            original = getattr(err, "original_exception", None)
            return jsonify({
                'success': False,
                'error': err.code,
                "message": getattr(err.error, 'message')
                }), err.code

        # if 'message' attribute isn't set, assume it's a core Python exception
        if not getattr(err, 'message', None):
            original = getattr(err, "original_exception", None)
            return jsonify({
                'message': 'Server has encountered an unknown error'
                }), 500

        # Handle application-specific custom exceptions
        return jsonify(**err.kwargs), err.http_status_code


def create_app(config_name='default'):
    # set up Flask here
    app = Flask(__name__, static_folder='static')

    # use our 'config_name' to set up our config.py settings
    app.config.from_object(config[config_name])

    # set up our database
    db.init_app(app)

    # set up CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # set up Flask-RESTful
    api = ExtendedAPI(app)

    @app.after_request
    def after_request(response):
        """
        CORS setup
        """
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.errorhandler(404)
    def not_found(error):
        """
        error handler for 404
        """
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.route('/')
    def reroute_root():
        return render_template('start.html')

    @app.route('/api/v1/')
    def display_start_doc():
        return render_template('start.html')

    @app.route('/api/v1/users-doc/')
    def display_users_doc():
        return render_template('users.html')

    @app.route('/api/v1/reminders-doc/')
    def display_reminders_doc():
        return render_template('reminders.html')

    @app.route('/api/v1/schedules-doc/')
    def display_schedules_doc():
        return render_template('schedules.html')

    @app.route('/api/v1/locations-doc/')
    def display_locations_doc():
        return render_template('locations.html')

    @app.route('/api/v1/github-repo/')
    def display_github_doc():
        return render_template('github_repo.html')

    from api.resources.users import UsersResource, UserResource
    from api.resources.locations import LocationsResource
    from api.resources.schedules import SchedulesResource
    from api.resources.reminders import UsersRemindersResource, ReminderResource, RemindersResource

    api.add_resource(UserResource, '/api/v1/users/<user_id>')
    api.add_resource(UsersResource, '/api/v1/users')
    api.add_resource(LocationsResource, '/api/v1/locations')
    api.add_resource(SchedulesResource, '/api/v1/schedules')
    api.add_resource(ReminderResource, '/api/v1/reminders/<reminder_id>')
    api.add_resource(RemindersResource, '/api/v1/reminders')
    api.add_resource(UsersRemindersResource, '/api/v1/users/<user_id>/reminders')

    return app
