from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
postgresConn =('postgresql://usr:pass@localhost:5432/sqlalchemy')
app.config['SQLALCHEMY_DATABASE_URI'] = postgresConn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)