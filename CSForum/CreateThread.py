import tkinter as tk
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

def displayUI(window, username):

    window.refresh() #Clears the Window

    window.displayNavbar(username) #Displays the top navbar

    #Adds the frame for the main section of the frame
    mainPage = tk.Frame(window.frame, highlightbackground="black", highlightthickness=1)
    mainPage.place(relwidth=1, relheight=0.925, relx=0, rely=0.075)

    #Input fields and labels
    createThreadLabel = tk.Label(mainPage, text="Create a Thread")
    createThreadLabel.place(relwidth=0.9, relheight=0.04, relx=0.05, rely=0.05)

    threadNameLabel = tk.Label(mainPage, text="Thread Name:", anchor="nw", justify="left")
    threadNameLabel.place(relwidth=0.3, relheight=0.04, relx=0.05, rely=0.15)

    threadName = tk.Entry(mainPage)
    threadName.place(relwidth=0.9, relheight=0.05, relx=0.05, rely=0.2)

    descriptionLabel = tk.Label(mainPage, text="Description:", anchor="nw", justify="left")
    descriptionLabel.place(relwidth=0.3, relheight=0.04, relx=0.05, rely=0.3)

    description = tk.Text(mainPage, highlightbackground="gray", highlightthickness=1)
    description.place(relwidth=0.9, relheight=0.3, relx=0.05, rely=0.35)


    #Adds the create button
    #Lambda means that the function is run when the button is clicked not when the button is made
    createBtn = tk.Button(mainPage,
                    text="Create",
                    command=lambda: addThread(threadName.get(), description.get("1.0","end"), username)
                )
    createBtn.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.75)

#Attempts to add the thread to the database
def addThread(name, desc, username):
    #name is the inputted name of the thread
    #desc is the description of the corresponding thread
    #username is the username of the user that wants to make the thread

    desc = desc[:len(desc)-1] #Removes the new line syntax at the end of a text input

    #Ensures the fields are all completed
    if name == "" or desc == "":
        print("Please complete all fields")
    else:
        #Gets the names of all the current threads
        mycursor.execute("SELECT threadName FROM threads")

        threadNames = [] #List to hold the names of the threads

        #Adds the names to the list
        for element in mycursor.fetchall():
            threadNames.append(element[0])

        #Ensures the name has not been used before
        if name in threadNames:
            print("Thread name already in use")
        else:
            #Adds the thread to the database
            mycursor.execute("INSERT INTO threads VALUES(%s, %s, %s)", (name, username, desc))
            mydb.commit()
            print("Success")
























    #
