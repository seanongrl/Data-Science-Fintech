from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin


app = Flask(__name__)
app.config.from_object(Config)
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

admin = Admin(app, url='/')


from app import routes, models