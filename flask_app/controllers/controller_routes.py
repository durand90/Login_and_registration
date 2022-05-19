from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import model_users



@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/success')
    return render_template('index.html')
