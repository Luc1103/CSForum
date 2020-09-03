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

#Displays the sidebar of all your conversations
def displayUI(window, username):

    #Frame for the conversations
    sidebar = tk.Frame(window.frame, highlightbackground="black", highlightthickness=1)
    sidebar.place(relwidth=0.2, relheight=0.925, relx=1, rely=0.075, anchor="ne")

    #Scrollable frame to add conversations to
    scConvos = sf.VerticalScrolledFrame(sidebar)
    scConvos.pack()

    convos = getConvos(username) #Gets the conversations

    convoBtns = {} #Dictionary to hold the buttons

    #Adds the conversations to the list
    for i in range(0, len(convos)):
        convoBtns[i] = tk.Button(scConvos.interior,
                            text=convos[i],
                            command=lambda a=i: displayConvo(window, username, convos[a])
                       )
        convoBtns[i].pack(padx=10, pady=5, side=tk.TOP)

    #Button to create a new conversation
    newConvo = tk.Button(sidebar, text="New", command=lambda: createNewConvoUI(window, username, sidebar))
    newConvo.place(relx=1, rely=1, relwidth=0.3, relheight=0.05, anchor="se")

#Displays UI to create a new conversation
def createNewConvoUI(window, username, sidebar):

    #Main UI for creating a new conversation
    mainPage = tk.Frame(window.frame)
    mainPage.place(relx=0, rely=0.075, relwidth=0.8, relheight=0.925)

    #Label to give user instruction
    usernameLabel = tk.Label(mainPage, text="Enter their username:", anchor="nw", justify="left")
    usernameLabel.place(relwidth=0.3, relheight=0.04, relx=0.05, rely=0.2)

    #Field for them to enter the username of the recipiant
    theirUsername = tk.Entry(mainPage)
    theirUsername.place(relwidth=0.9, relheight=0.05, relx=0.05, rely=0.25)

    createBtn = tk.Button(mainPage,
                    text="Create",
                    command=lambda: addConvo(username, theirUsername.get(), mainPage, sidebar, window)
                )
    createBtn.place(relx=0.35, rely=0.55, relwidth=0.3, relheight=0.1)

#Function to display a particular conversation
def displayConvo(window, username, recipient):
    #Main UI for displaying a conversation
    mainPage = tk.Frame(window.frame)
    mainPage.place(relx=0, rely=0.075, relwidth=0.8, relheight=0.875)

    #Gets the convo number from the conversation trying to be displayed
    sql = """SELECT convoNum FROM conversations WHERE
            (username1=%s AND username2=%s) OR
            (username1=%s AND username2=%s)"""
    strings = (username, recipient, recipient, username)

    mycursor.execute(sql, strings)

    #Fetches the convo num
    convoNum = mycursor.fetchall()[0][0]

    userLabel = tk.Label(mainPage, text=recipient)
    userLabel.place(relx=0, rely=0)

    #Creates a list to store the messages
    messagesBox = sf.VerticalScrolledFrame(mainPage)
    messagesBox.place(relx=0, rely=0.025, relwidth=1, relheight=0.975)

    messages = getMessages(convoNum) #Fetches the messages

    labels = {} #Dictionary to store the messages labels

    #Iterates through each message and creates a label for them
    for i in range(0, len(messages)):
        message = messages[i] #Variable for the current messages
        if message[1] == username:
            labels[i] = tk.Label(messagesBox.interior, text=message[0], bg="#3399FF")
            #Adds them to the right is they are sent by the user
            labels[i].pack(pady=5)
        else:
            labels[i] = tk.Label(messagesBox.interior, text=message[0])
            #Adds them to the left if they are recieved by the user
            labels[i].pack(pady=5)

    #Adds the entry for people to input their messages into
    messageBar = tk.Entry(window.frame)
    messageBar.place(rely=1, relwidth=0.7, relheight=0.05, anchor="sw")

    #Adds the button for people to send their messages
    sendMessageBtn = tk.Button(window.frame,
                        text="Send",
                        command=lambda: sendMessage(convoNum, username, recipient, messageBar.get(), window)
                     )
    sendMessageBtn.place(relx=0.7, rely=1, relwidth=0.1, relheight=0.05, anchor="sw")

#Function to add a conversation to the database
def addConvo(creator, recipient, ui, sidebar, window):

    #Ensures the user does not make a conversation with themselves
    if creator == recipient:
        print("You cannot make a conversation with yourself")
    else:
        users = getUsers() #Gets all usernames

        if not(recipient in users): #Ensures user exists
            print("User does not exist")
        else:

            convos = getConvos(creator) #Gets all conversations the user is a part of
            
            exists = False #Stores whether a conversation already exists or not

            for convo in convos:
                #Variable switch if they already have a conversation
                if convo == recipient:
                    exists = True

            if exists == True:
                print("You already have a conversation with " + recipient)
            else:
                mycursor.execute("SELECT MAX(convoNum) FROM conversations") #Fetches the last highest convo num
                prevMax = mycursor.fetchall()[0][0] #Stores the old highest convo number
                #Creates the convo number for the new convo
                if prevMax == None:
                    newNum = 1
                else:
                    newNum = int(prevMax) + 1

                #Inserts values into the database
                mycursor.execute("INSERT INTO conversations VALUES (%s, %s, %s)", (newNum, creator, recipient))
                mydb.commit()

                ui.destroy() #Removes the addition window
                displayUI(window, creator) #Updates the sidebar
                displayConvo(window, creator, recipient) #Takes you too their conversation


#Function to return a list of conversations
def getConvos(username):

    convos = [] #List to store the names of the users you currently have a conversation with
    #Fetches the data from the database
    mycursor.execute("SELECT username1, username2 FROM conversations WHERE username1 = %s OR username2 = %s",
                    (username, username)
    )

    #Adds the names that are not the users to the list
    for element in mycursor.fetchall():
        if element[0] == username:
            convos.append(element[1])
        else:
            convos.append(element[0])

    return convos

#Returns all the messages and who sent them from a conversation
def getMessages(convoNum):
    mycursor.execute("SELECT messageContent, username FROM messages WHERE convoNum = %s",
                    (convoNum,)
    )
    return mycursor.fetchall()

#Returns a list of all the usernames that exist
def getUsers():
    users = []
    mycursor.execute("SELECT username FROM users")
    for element in mycursor.fetchall():
        users.append(element[0])

    return users

#Function to add the message to the database
def sendMessage(convoNum, sender, recipient, content, window):
    #Ensures the entry has an input
    if content == "":
        print("Enter a message")
    else:
        mycursor.execute("SELECT MAX(messageNum) FROM messages") #Fetches the last highest message num
        prevMax = mycursor.fetchall()[0][0] #Stores the old highest message number
        #Creates the convo number for the new convo
        if prevMax == None:
            newNum = 1
        else:
            newNum = int(prevMax) + 1

        #Inserts values into the database
        mycursor.execute("INSERT INTO messages VALUES (%s, %s, %s, %s)", (newNum, convoNum, content, sender))
        mydb.commit()

        displayConvo(window, sender, recipient) #Updates the conversation window











#
