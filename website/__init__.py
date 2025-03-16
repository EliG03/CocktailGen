'''
This file is the __init__.py file for the website package.
'''

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    '''
    This function creates the Flask application.
    '''
    app = Flask(__name__)

    if os.environ.get('CONFIG_TYPE') == 'config.TestingConfig':
        app.config['SECRET_KEY'] = 'secret'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    db.init_app(app)

    from .views import main_blueprint

    # Register blueprint for routes
    app.register_blueprint(main_blueprint)
    # app.register_blueprint(auth_blueprint)

    #if __name__ == '__main__':
    with app.app_context():
        print('Creating tables')
        db.create_all()  # Create tables (if not created)
        #app.run(debug=True)

    return app

if __name__ == '__main__':
    create_app()
