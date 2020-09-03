import mysql.connector

#Connects to the database
mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  passwd = "sD6G7Bx@f8cve$i3",
  database = "forum"
)

#Allows editing of the database
mycursor = mydb.cursor()
'''
mycursor.execute("DELETE FROM reports")
mydb.commit()
'''
mycursor.execute("SELECT * FROM users")
print(mycursor.fetchall())
'''
for e in mycursor.fetchall():
    print(e)
'''
