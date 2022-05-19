from flask_app import app, bcrypt
from flask import render_template, redirect, request, session
from flask_app.models import model_users

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/table_name/new') # create a person route
def new_table_name():
    return render_template('/new_user.html') # create a person html page

@app.route('/success')
def success_login():

    if 'uuid' not in session:
        return redirect('/')
    
    
    
    id = session['uuid']
    user = model_users.User.get_one({'id': id})

        


    return render_template('/success.html', user = user)

@app.route('/logout')
def logout():
    del session['uuid']
    return redirect('/')

@app.route('/user/login', methods=['post'])
def users_login():

    is_valid = model_users.User.validator_login(request.form)     

    if not is_valid:
        return redirect('/')

    return redirect('/')

@app.route('/users/create', methods=['post'])
def create_users():        # "new person" or "id" is equal(=) to Table_name(class name) dot(".") create function with(request.form)



    is_valid = model_users.User.validator(request.form)

    if is_valid == False:
        return redirect('/')

    #hash the incoming password

    hash_pw = bcrypt.generate_password_hash(request.form['pw'])
    #hash_confirm_pw = bcrypt.generate_password_hash(request.form['confirm_pw'])
    print(hash_pw)
    #print(hash_confirm_pw)

    data = {
        **request.form,
        'pw': hash_pw
    }

    new_user = model_users.User.create(data)

    session['uuid'] = new_user


    return redirect('/')

@app.route('/table_name/<int:id>')
def show_table_name(id):
    pass

@app.route('/table_name/<int:id>/edit')
def edit_table_name(id):
    pass

@app.route('/table_name/<int:id>/update', methods=['post'])
def update_table_name(id):
    pass

@app.route('/table_name/<int:id>/delete')
def delete_table_name(id):
    pass
