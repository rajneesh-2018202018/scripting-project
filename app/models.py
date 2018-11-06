import sqlite3 as sql
from flask import session
from passlib.hash import sha256_crypt

def insertUser(request):
    con = sql.connect("database.db")
    sqlQuery = "select username from user_details where (username ='" + request.form['username'] + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    print row
    
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
	con = sql.connect("database.db")
        # Uncomment line below if you want output in dictionary format
	#con.row_factory = sql.Row
	cur = con.cursor()
        if user==None:
	        cur.execute("SELECT * FROM blog_detail;")
        else:
                sqlQuery = "SELECT * from BLOGS where user = '%s'"%user
                cur.execute(sqlQuery)
	rows = cur.fetchall()
	con.close()
	return rows

# add blog (Nawab)
def addUser(user):
  try:

   msg = "Record successfully added"
  
   with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO blog_detail (user_name, title,content,date,published)  VALUES (?,?,?,?,?)",('rajneesh',user['title'],user['data'],'1nov2018',1))            
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
      cur.execute("select * from blog_detail") 
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
      cur.execute("select * from comment where blog_id = ?", (args1['blog_id'])) 
      print args1['blog_id']
      rows = cur.fetchall()
      comment=[]
      for row in rows:
           comment.append(row)
      return (comment)
  except:
      print "connection failed"
      return ([], "connection failed")
