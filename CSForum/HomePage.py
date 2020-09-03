import tkinter as tk
import ScrollableFrame as sf
import Sorting
import ProfilePage
import ThreadPage

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

def displayUI(window, username, searched, text=None):
    """Searched is a boolean that tells the program whether a user has navigated
       to the homepage normally or via the search function in oder to know which
       infomation it should display"""
    """text is the string that the user has searched for, only used when
       the user had been directed to the homepage from the search function"""

    window.refresh() #Clears the Window

    window.displayNavbar(username)
    window.displaySidebar(username, getUserThreads(username))

    #Adds the frame for the main section of the frame
    mainPage = tk.Frame(window.frame, highlightbackground="black", highlightthickness=1)
    mainPage.place(relwidth=0.8, relheight=0.925, relx=0.2, rely=0.075)

#Adds information to the main page

    if searched == False: #When the user just normally accesses the homepage

        popThreadLabel = tk.Label(mainPage, text="Popular Threads:")
        popThreadLabel.pack()

        scMainPage = sf.VerticalScrolledFrame(mainPage)
        scMainPage.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)

        popThreads = getPopThreads(username) #Gets the information of all the popular threads

        popThreadsBtns = {} #Dictionary to store all the thread buttons

        for i in range(0,len(popThreads)):
            #Text to display all the thread info
            btnText = popThreads[i][0] + "\nDescription: " + popThreads[i][2] + "\nUsers: " + str(popThreads[i][1]) + "\nPosts: " + str(popThreads[i][3])
            #Creates the button adding it to the dictionary
            popThreadsBtns[i] = tk.Button(scMainPage.interior, text=btnText, command=lambda a=i: joinThread(username, popThreads[a][0], window))
            popThreadsBtns[i].pack(padx=10, pady=5, side=tk.TOP)

    else: #When the user searches for something

        threads = getSearchedThreads(username, text) #Gets the threads info

        #Sets the text of the heading label
        if len(threads) == 0:
            #Ensures the user is informed if no results are found
            labelText = "No results"
        else:
            labelText = "Threads relating to: "+text

        #Label to give context to the display
        searchedForLabel = tk.Label(mainPage, text=labelText)
        searchedForLabel.pack()

        #Container for the threads
        scMainPage = sf.VerticalScrolledFrame(mainPage)
        scMainPage.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)

        btns = {} #Dictionary to store all the thread buttons

        for i in range(0,len(threads)):
            #Text to display all the thread info
            btnText = threads[i][0] + "\nDescription: " + threads[i][2] + "\nUsers: " + str(threads[i][1]) + "\nPosts: " + str(threads[i][3])
            #Creates the button adding it to the dictionary
            btns[i] = tk.Button(scMainPage.interior, text=btnText, command=lambda a=i: joinThread(username, threads[a][0], window))
            btns[i].pack(padx=10, pady=5, side=tk.TOP)

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

#Function to get all the threads the user is not a member of
def getNewThreads(username):

    userThreads = getUserThreads(username) #Threads the user is a member of
    newThreads = [] #List of the threads the user is not a member of

    #Gets all the thread names and descriptions
    mycursor.execute("SELECT threadName, threadDescription FROM threads")

    #Adds the threads that the user is not a part of to the list
    for element in mycursor.fetchall():
        if not(element[0] in userThreads):
            newThreads.append(element)

    return newThreads

#Function to get all the popular threads
def getPopThreads(username):

    #Gets the threads the user is not a member of
    threads = getNewThreads(username)

    # List to store the name of the thread, the number of users and description together as a tuple
    popThreads = []

    #Gets the number of users and posts that are part of each thread
    for thread in threads:
        #Counts every instance of a user being in the specifies thread
        mycursor.execute("SELECT COUNT(username) FROM threadParticipants WHERE threadName = %s", (thread[0],))
        users = mycursor.fetchall()[0][0]
        #Counts every instance of a post being in the specifies thread
        mycursor.execute("SELECT COUNT(commentNum) FROM comments WHERE threadName = %s", (thread[0],))
        posts = mycursor.fetchall()[0][0]
        popThreads.append((thread[0], users , thread[1], posts)) #Adds the thread name, number of users and posts as a tuple


    #At this point popthreads are unsorted

    #Uses merge sort to sort the list into descending order by number of users
    popThreads = Sorting.mergeSort(popThreads, 0, len(popThreads)-1)

    return popThreads

#Allows a user to join a thread
def joinThread(username, threadName, window):

    #Adds them to the database
    mycursor.execute("INSERT INTO threadParticipants VALUES(%s, %s)", (username, threadName))
    mydb.commit() #Makes the change permanent

    displayUI(window, username, False) #Updates the display

#Gets the information of the searched for threads
def getSearchedThreads(username, text):
    #Here the parameter 'text' holds the string the user is trying to search for.

    #Fetches all the threads that contain the text the user searched for either in the description or name
    mycursor.execute("""SELECT threadName, threadDescription FROM threads
                        WHERE (threadName LIKE %s)
                        OR (threadDescription LIKE %s)""",
                        ('%'+text+'%', '%'+text+'%')
                    )
    threads = mycursor.fetchall()

    userThreads = getUserThreads(username) #Threads the user is a member of

    i = 0 #Index of the thread in the list 'threads'
          #currently being evaluated

    while i < len(threads):
        if threads[i][0] in userThreads:
            #Deletes the element at index "i"
            del threads[i] #if the user is already part of the thread
        i += 1

    threadsInfo = [] #List to hold the threads with all the information in

    #Gets the number of users and posts that are part of each thread
    for thread in threads:
        #Counts every instance of a user being in the specifies thread
        mycursor.execute("SELECT COUNT(username) FROM threadParticipants WHERE threadName = %s", (thread[0],))
        users = mycursor.fetchall()[0][0]
        #Counts every instance of a post being in the specifies thread
        mycursor.execute("SELECT COUNT(commentNum) FROM comments WHERE threadName = %s", (thread[0],))
        posts = mycursor.fetchall()[0][0]
        #Adds the thread name, number of users and posts as a tuple
        threadsInfo.append((thread[0], users , thread[1], posts))

    return threadsInfo












#hello
