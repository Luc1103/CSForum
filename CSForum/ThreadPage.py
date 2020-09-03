import tkinter as tk
import ScrollableFrame as sf
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

def displayUI(window, username, threadName):

    window.refresh() #Clears the Window

    window.displayNavbar(username) #Displays the top navbar
    window.displaySidebar(username, getUserThreads(username)) #Displays the sidebar


    #Adds the frame for the main section of the frame
    mainPage = tk.Frame(window.frame, highlightbackground="black", highlightthickness=1)
    mainPage.place(relwidth=0.8, relheight=0.925, relx=0.2, rely=0.075)

    #Label for the threads name
    nameLabel = tk.Label(mainPage, text=threadName, anchor="nw", justify="left")
    nameLabel.place(relx=0, rely=0, relwidth=0.2, relheight=0.025)

    #Scrollable container for the comments
    commentBox = sf.VerticalScrolledFrame(mainPage)
    commentBox.place(relx=0, rely=0.025, relwidth=1, relheight=0.925)

    comments = getComments(threadName) #Gets comment information

    labels = {} #Dictionary to store the comment labels

    #Iterates through each comment and creates a label for them
    for i in range(0, len(comments)):
        labels[i] = tk.Label(commentBox.interior, text=comments[i][1] + ": " + comments[i][2])
        #Adds them to the right is they are sent by the user
        labels[i].pack(pady=5)

    #Adds comment bar and post button
    commentbar = tk.Entry(mainPage)
    commentbar.place(rely=1, relwidth=0.9, relheight=0.05, anchor="sw")

    postCommentBtn = tk.Button(mainPage,
                        text="Post",
                        command=lambda: postComment(username, threadName, commentbar.get(), window)
                     )
    postCommentBtn.place(relx=0.9, rely=1, relwidth=0.1, relheight=0.05, anchor="sw")


#Subroutine to add comments to the database
def postComment(username, threadName, comment, window):

    if comment == "": #Ensures there is a comment to add
        print("Enter a comment")
    else:
        mycursor.execute("SELECT MAX(commentNum) FROM comments") #Fetches the last stored comment
        prevMax = mycursor.fetchall()[0][0] #Stores the old highest comment number
        if prevMax == None:
            newNum = 1
        else:
            newNum = str(int(prevMax) + 1) #Creates the comment number for the new comment

        #Adds the comment to the database
        mycursor.execute("INSERT INTO comments VALUES(%s, %s, %s, %s)",
                        (newNum, username, comment, threadName)
        )
        mydb.commit()
        print("Success")

        displayUI(window, username, threadName)


#Gets the comment info from the database
def getComments(threadName):

    mycursor.execute("SELECT commentNum, username, commentContent FROM comments WHERE threadName = %s",
                    (threadName,)
    )
    return mycursor.fetchall()

#Function to get all the threads a user is in
def getUserThreads(username):

    #Gets the name of all the threads the user is a member of
    mycursor.execute("SELECT threadName FROM threadParticipants WHERE username = %s", (username,))

    #List to store all the thread names
    threads = []

    #Gets the thread name from each returned tuple
    for element in mycursor.fetchall():
        threads.append(element[0])

    return threads























    #
