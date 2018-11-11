import sqlite3 as sql
from flask import session
from passlib.hash import sha256_crypt
import requests
import datetime
def insertUser(request):
    con = sql.connect("database.db")
    sqlQuery = "select username from user_details where (username ='" + request.form['username'] + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    print row #check
    
    if not row:
        cur.execute("INSERT INTO user_details (username,password,name,dob,email,gender,isadmin,facebook) VALUES (?,?,?,?,?,?,?,?)", (request.form['username'], 
                   sha256_crypt.encrypt(request.form['password']),request.form['name'],request.form['dob'],request.form['email'],request.form['gender'],request.form['isAdmin'],request.form['facebook']))
        con.commit()
        print "added user successfully"
       
    con.close()
    return not row


def authenticate(request):
    con = sql.connect("database.db")
    sqlQuery = "select password from user_details where username = '%s'"%request.form['username']  
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    con.close()
    if row:
       return sha256_crypt.verify(request.form['password'], row[0])
    else:
       return False


def retrieveUsers(): 
	con = sql.connect("database.db")
        # Uncomment line below if you want output in dictionary format
	#con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute("SELECT * FROM users;")
	rows = cur.fetchall()
	con.close()
	return rows
  
def retrieveBlogs(user=None): 
  try:
    with sql.connect("database.db") as con:
      print "-------------------------------inside Retrieve blogs------------------------------------------------"
      con.row_factory = sql.Row
      cur = con.cursor()
      if user!=None:
        print "======================Value of user=============================" + user
        cur.execute("select * from blog_detail ORDER BY date")
        print "Query successfully executed-----------------------------------------"
        rows = cur.fetchall()
        print "tag"
        users=[]
        for row in rows:
          if row['user_name']==user:
            users.append(row)
        return users
  except:
    print "Connection Error"
    return([],"connection Fault")

def retrieveParticular(blog_id): 
  try:
    with sql.connect("database.db") as con:
      print "-------------------------------inside Retrieve blogs------------------------------------------------"
      con.row_factory = sql.Row
      cur = con.cursor()
      if blog_id!=None:
        print "======================Value of user=============================" + blog_id
        cur.execute("select content from blog_detail WHERE blog_id={x}".format(x=blog_id))
        print "Query successfully executed-----------------------------------------"
        rows = cur.fetchone()
        return rows["content"]
  except:
    print "Connection Error"
    return([],"connection Fault")


# add blog (Nawab)
def addUser(user):
  try:

   msg = "Record successfully added"
   with sql.connect("database.db") as con:
        cur = con.cursor()
        sqlQuery = "select * from blog_detail where blog_id = '%s'"%user['blog_id']  
        # print user['data'], user['blog_id']
        cur.execute(sqlQuery)
        row = cur.fetchone()
        now = datetime.datetime.now()

        if not row:
          cur.execute("INSERT INTO blog_detail (user_name, title,content,date,published)  VALUES (?,?,?,?,?)",(session['username'],user['title'],user['data'],now.strftime("%Y-%m-%d"),user['published']))
          con.commit()
        else:
          print "inside update condition "
          print user["blog_id"]
          # sqlQuery1="update blog_detail set content='"+ user['data']+"' where blog_id='"+user['blog_id']+"'"
          # cur.execute(sqlQuery1)
          # sqlQuery1="update blog_detail set content=? where blog_id='?'"
          cur.execute("SELECT (user_name) from blog_detail WHERE blog_id={x}".format(x=user["blog_id"]))
          print "hi"
          rows = cur.fetchone()
          info=[]
          for row in rows:
            info.append(row)
          print info[0]
          if info[0]==session["username"]:
            print user["published"]
            cur.execute("UPDATE blog_detail SET content='{x}', published={y} WHERE blog_id={id}".format(x=user["data"],y=int(user["published"]),id=user["blog_id"]))
            con.commit()

        
      #print msg, '---', dict
        return  (user, msg)
  except:
      msg = "Unexpected Error in insert operation"
      print msg
      return ({}, msg)

def getAll():
  msg = "Records were fetched successfully"
  try:  
    with sql.connect("database.db") as con:
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("select * from blog_detail WHERE published = 1 ORDER BY date ASC") 
      rows = cur.fetchall()
      user=[]
      for row in rows:
           user.append(row)
      return (user)
  except:
      print "connection failed"
      return ([], "connection failed")

def comment(args1):
  try:  
    with sql.connect("database.db") as con:
      con.row_factory = sql.Row
      cur = con.cursor()
      print "args in model.comment",args1
      cur.execute("select * from comment") 
      print args1
      rows = cur.fetchall()
      comment=[]
      for row in rows:
        if row['blog_id']==int(args1):
           comment.append(row)
      return (comment)
  except:
      print "connection failed"
      return ([], "connection failed")

def add_comment(arg,s):
  try:
    with sql.connect("database.db") as con:
      cur = con.cursor()

      cur.execute("INSERT INTO comment (comment,blog_id,user_name) VALUES(?,?,?)", (arg["plain_text"],arg["blog_id"],s["username"]))
  except:
    print "INSIDE ADD_EXCEPT"

def del_blogs(arg):
  try:
    with sql.connect("database.db") as con:
      cur=con.cursor()
      print "value of arg = " , arg
      queryString = "Delete from blog_detail where blog_id='%s'"%arg
      cur.execute(queryString)
      return "success"
  except:
    return "Failure"


def particularProfile(arg):
  try:
    with sql.connect("database.db") as con:
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("SELECT * FROM blog_detail WHERE user_name = '{x}' and PUBLISHED = 1".format(x=arg))
      print "here"
      rows = cur.fetchall()
      user_blogs = []
      for row in rows:
        user_blogs.append(row)
      return user_blogs
  except:
    return "Error occured"