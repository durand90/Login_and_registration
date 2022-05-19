from flask_app import app #CHECK SPELLING EVERYWHERE
from flask_app.controllers import controller_routes, controller_users #CHECK SPELLING EVERYWHERE

if __name__ =="__main__":
    app.run(debug=True)