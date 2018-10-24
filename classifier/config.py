import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

#connex_app = connexion.App(__name__, specification_dir=basedir)
connex_app = connexion.App(__name__, specification_dir='./swagger/')

app = connex_app.app

sqlite_url = "sqlite:///" + os.path.join(basedir, 'db.sqlite')
#sqlite_url = 'jdbc:sqlite:L:\Folder4Autumn\Classifier3\classifier\db.sqlite'

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLACLHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)
