from flask import Flask
from flask import session
from flask import redirect, url_for
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap
import models as dbHandler

app = Flask(__name__)
Bootstrap(app)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = 'MKhJHJH798798kjhkjhkjGHh'

@app.route('/')
def index():
   if 'username' in session:
      return render_template("index.html", logged_in = True,  username=session['username'])
   else:
      return render_template("index.html", logged_in = False,  username=None)

 

@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return render_template("index.html",logged_in = True, username = session["username"])
    elif request.method == 'POST':
        if dbHandler.authenticate(request): 
            session['username'] = request.form['username']
            return render_template("index.html",logged_in = True, username = session["username"])
        else:
            return render_template("login.html", logged_in=False, username=None)
   
    return render_template('login.html', logged_in = False, username=None)




@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template("index.html")
    
    return render_template("index.html")

######################### register ################################################
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
	    return render_template("index.html")
    
    return render_template('register.html')

######################### secret page: a password protected page ################################################ 
@app.route('/secret_page')
def secret_page():

    #only logged in user is allowed see other users' details.
    if 'username' in session :
       rows = dbHandler.retrieveUsers()
       print rows
       return render_template("showall.html", rows = rows)
    else:
       return redirect(url_for('login'))

###########################################################################
