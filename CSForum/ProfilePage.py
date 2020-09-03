import tkinter as tk
import ScrollableFrame as sf
import ChangePassword
import CreateThread
import ThreadManagement
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
    window.displayNavbar(username) #Dislays the top navbar

    #Adds the frame for the main section of the frame
    mainPage = tk.Frame(window.frame)
    mainPage.place(relwidth=1, relheight=0.925, rely=0.075)

    #Adds the username label
    usernameLabel = tk.Label(mainPage, text="Username:")
    usernameLabel.pack()

    #Label to display the username
    usernameDisplay = tk.Label(mainPage, text=username)
    usernameDisplay.pack()

    #Adds the public key label
    publicKeyLabel = tk.Label(mainPage, text="Public Key:")
    publicKeyLabel.pack()

    #Label to display the public key
    publicKeyDisplay = tk.Label(mainPage, text=str(getPublicKey(username)))
    publicKeyDisplay.pack()

    #Adds the button to change your password
    changePass = tk.Button(mainPage,
                    text="Change Password",
                    command=lambda: ChangePassword.displayUI(window, username)
                 )
    changePass.pack()

    #Adds the create thread button
    createThread = tk.Button(mainPage,
                      text="Create A Thread",
                      command=lambda: CreateThread.displayUI(window, username)
                   )
    createThread.pack()

    #Adds owned threads label
    ownedThreadsLabel = tk.Label(mainPage, text="Owned Threads:")
    ownedThreadsLabel.pack()

    #List of threads owned by the user
    scMainPage = sf.VerticalScrolledFrame(mainPage)
    scMainPage.pack()

    threads = getOwnedThreads(username)

    btns = {} #Dictionary to store all the thread buttons

    for i in range(0,len(threads)):
        #Creates the button adding it to the dictionary
        btns[i] = tk.Button(scMainPage.interior, text=threads[i],
                            command=lambda a=i: ThreadManagement.displayUI(window, username, threads[a]))
        btns[i].pack(padx=10, pady=5, side=tk.TOP)

def getPublicKey(username):
    return 12345

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























#
