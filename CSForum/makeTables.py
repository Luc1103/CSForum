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


mycursor.execute("""
    CREATE TABLE users (
        username varchar(25),
        password varchar(100),
        PRIMARY KEY (username)
    )
""")

mycursor.execute("""
    CREATE TABLE threads (
        threadName varchar(25),
        username varchar(25),
        threadDescription varchar(250),
        PRIMARY KEY (threadName),
        FOREIGN KEY (username) REFERENCES users(username)
    )
""")

mycursor.execute("""
    CREATE TABLE threadParticipants (
        username varchar(25),
        threadName varchar(25),
        PRIMARY KEY (username, threadName)
    )
""")

mycursor.execute("""
    CREATE TABLE comments (
        commentNum int,
        username varchar(25),
        commentContent varchar(250),
        threadName varchar(25),
        PRIMARY KEY (commentNum),
        FOREIGN KEY (username) REFERENCES users(username),
        FOREIGN KEY (threadName) REFERENCES threads(threadName)
    )
""")

mycursor.execute("""
    CREATE TABLE replies (
        replyNum int,
        commentNum int,
        username varchar(25),
        replyContent varchar(250),
        PRIMARY KEY (replyNum),
        FOREIGN KEY (commentNum) REFERENCES comments(commentNum),
        FOREIGN KEY (username) REFERENCES users(username)
    )
""")

mycursor.execute("""
    CREATE TABLE reports (
        reportNum int,
        subject varchar(25),
        reportContent varchar(250),
        username varchar(25),
        PRIMARY KEY (reportNum),
        FOREIGN KEY (username) REFERENCES users(username)
    )
""")

mycursor.execute("""
    CREATE TABLE conversations (
        convoNum int,
        username1 varchar(25),
        username2 varchar(25),
        PRIMARY KEY (convoNum),
        FOREIGN KEY (username1) REFERENCES users(username),
        FOREIGN KEY (username2) REFERENCES users(username)
    )
""")

mycursor.execute("""
    CREATE TABLE messages (
        messageNum int,
        convoNum int,
        messageContent varchar(250),
        username varchar(25),
        PRIMARY KEY (messageNum),
        FOREIGN KEY (convoNum) REFERENCES conversations(convoNum),
        FOREIGN KEY (username) REFERENCES users(username)
    )
""")



mycursor.execute("SHOW TABLES")

print(mycursor.fetchall())
