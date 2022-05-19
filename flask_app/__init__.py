from flask import Flask
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

DATABASE = 'login_and_registration'