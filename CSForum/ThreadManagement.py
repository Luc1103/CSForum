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

    ### Sidebar code copied here so it can be ammended for the thread management ###
    #Sets the frame for the side navbar
    sidebar = tk.Frame(window.frame, highlightbackground="black", highlightthickness=1, bd=5)
    sidebar.place(relwidth=0.2, relheight=0.925, relx=0, rely=0.075)

    #Adds the buttons to the sidebar
    ownedThreadLabel = tk.Label(sidebar, text="Owned Threads:")
    ownedThreadLabel.pack()

    #Creates the vertical scrollbar for the sidebar
    scSidebar = sf.VerticalScrolledFrame(sidebar)
    scSidebar.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)

    userThreads = getOwnedThreads(username) #Gets the threads the user is a member of

    buttons = {} #Dictionary to store the buttons in the sidebar

    #Adds all the buttons to the scrollable view and sets their function
    for i in range(0, len(userThreads)):
        buttons[i] = tk.Button(scSidebar.interior,
                               text=userThreads[i],
                               command=lambda a=i: displayUI(window, username, userThreads[a]))
        buttons[i].pack(padx=10, pady=5, side=tk.TOP)


    #Adds the frame for the main section of the frame
    mainPage = tk.Frame(window.frame, highlightbackground="black", highlightthickness=1)
    mainPage.place(relwidth=0.8, relheight=0.925, relx=0.2, rely=0.075)

    #Input fields and labels
    headerLabel = tk.Label(mainPage, text=threadName + " Settings")
    headerLabel.place(relwidth=0.9, relheight=0.04, relx=0.05, rely=0.05)

    descriptionLabel = tk.Label(mainPage, text="Public Descriptor:", anchor="nw", justify="left")
    descriptionLabel.place(relwidth=0.3, relheight=0.04, relx=0.05, rely=0.15)

    description = tk.Text(mainPage, highlightbackground="gray", highlightthickness=1)
    description.insert(tk.END, getDescription(threadName))
    description.place(relwidth=0.9, relheight=0.45, relx=0.05, rely=0.2)


    #Adds the confirm button
    #Lambda means that the function is run when the button is clicked not when the button is made
    confirmBtn = tk.Button(mainPage,
                    text="Save",
                    command=lambda: updateThread(threadName, description.get("1.0","end"))
                 )
    confirmBtn.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.75)


#Gets the threads that the user owns
def getOwnedThreads(username):

    #Gets the name of all the threads the user ownes
    mycursor.execute("SELECT threadName FROM threads WHERE username = %s", (username,))

    #List to store all the thread names
    threads = []

    #Gets the thread name from each returned tuple
    for element in mycursor.fetchall():
        threads.append(element[0])

    return threads

#Gets the description of the passed thread
def getDescription(threadName):

    mycursor.execute("SELECT threadDescription FROM threads WHERE threadName = %s",
                     (threadName,))

    return mycursor.fetchall()[0][0]

#Updates the current elements in the database
def updateThread(name, desc):
    #name is the thread name
    #desc is the thread description

    desc = desc[:len(desc)-1] #Removes the new line syntax at the end of a text input

    if desc == "":
        print("Enter a description")
    else:
        mycursor.execute("UPDATE threads SET threadDescription = %s WHERE threadName = %s",
                         (desc, name))
        mydb.commit()
        print("Success")


































#hello
