from flask import Flask
from flask import session
from flask import redirect, url_for
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap
import models as dbHandler

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'MKhJHJH798798kjhkjhkjGHh'

@app.route('/')
def index():
   blogs_sent = dbHandler.getAll()
   if 'username' in session:
       return render_template("index.html", logged_in = True,  username=session['username'], blogs=blogs_sent)
   else:
       return render_template("index.html", logged_in = False,  username=None, blogs=blogs_sent)
 

@app.route('/login', methods=['POST', 'GET'])
def login():
    blogs_sent = dbHandler.getAll()
    if 'username' in session:
        return render_template("index.html",logged_in = True, username = session["username"], blogs = blogs_sent)
    elif request.method == 'POST':
        if dbHandler.authenticate(request):
            session['username'] = request.form['username']
            return render_template("admin.html",logged_in = True, username = session["username"], blogs = blogs_sent)
        else:
            return render_template("login.html", logged_in=False, username=None)   
    return render_template('login.html', logged_in = False, username=None, blogs=blogs_sent)




@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return index()
        # return render_template("index.html")
    
    return index()


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        if dbHandler.insertUser(request):
            return render_template("login.html", logged_in=False)
        else:
	        return render_template("index.html")
    
    return render_template('register.html')


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
@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == "GET":
      res, msg = dbHandler.addUser(request.args)
   else:
      res, msg = dbHandler.addUser(request.form)

   return 'hope working'
   #return render_template("result.html", result = res, message = request.method + " : " + msg)

@app.route('/editor')
def editor():
    return render_template('editor.html')

@app.route('/admin')
def admin():
   blogs_sent = dbHandler.getAll()
   if 'username' in session:
       return render_template("admin.html", logged_in = True,  username=session['username'], blogs=blogs_sent)
   else:
       return render_template("admin.html", logged_in = False,  username=None, blogs=blogs_sent)


@app.route('/showall')
def showall():
    msg = dbHandler.getAll()
    return render_template('abc.html',user=msg)

@app.route('/comment',methods = ['POST', 'GET'])
def comments():
    if request.method == "GET":
        msg = dbHandler.comment(request.args)
    else:
        msg = dbHandler.comment(request.form)
    
    return render_template('comment_div.html',user=msg)
