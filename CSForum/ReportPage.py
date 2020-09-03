import tkinter as tk
import WindowSetup
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

#Displays the report page UI
def displayUI(window, username):

    window.refresh() #Clears the Window

    window.displayNavbar(username) #Displays the top navbar

    #Adds the frame for the main section of the frame
    mainPage = tk.Frame(window.frame, highlightbackground="black", highlightthickness=1)
    mainPage.place(relwidth=1, relheight=0.925, relx=0, rely=0.075)

    #Input fields and labels
    reportLabel = tk.Label(mainPage, text="Make A Report")
    reportLabel.place(relwidth=0.9, relheight=0.04, relx=0.05, rely=0.05)

    subjectLabel = tk.Label(mainPage, text="Subject:", anchor="nw", justify="left")
    subjectLabel.place(relwidth=0.3, relheight=0.04, relx=0.05, rely=0.15)

    subject = tk.Entry(mainPage)
    subject.place(relwidth=0.9, relheight=0.05, relx=0.05, rely=0.2)

    detailsLabel = tk.Label(mainPage, text="Details:", anchor="nw", justify="left")
    detailsLabel.place(relwidth=0.3, relheight=0.04, relx=0.05, rely=0.3)

    details = tk.Text(mainPage, highlightbackground="gray", highlightthickness=1)
    details.place(relwidth=0.9, relheight=0.3, relx=0.05, rely=0.35)


    #Adds the confirm button
    #Lambda means that the function is run when the button is clicked not when the button is made
    confirmBtn = tk.Button(mainPage,
                    text="Confirm",
                    command=lambda: addReport(subject.get(), details.get("1.0","end"),
                    username,
                    window)
                 )
    confirmBtn.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.75)

#Function to add details to the database
def addReport(subject, details, username, window):
    #Here the details parameter corresonds to the reportContent field in the database.

    details = details[:len(details)-1] #Removes the new line syntax at the end of a text input

    if subject == "" or details == "": #Ensures all the fields are completed
        print("Please complete all fields")
    else:
        #Gets the previous reportNum
        mycursor.execute("SELECT MAX(reportNum) FROM reports")
        prevMax = mycursor.fetchall()[0][0]

        #Ensures no errors are made if trying to insert the first comment
        if prevMax == None:
            newNum = 1
        else:
            newNum = prevMax +1

        #Inserts the values into the database
        mycursor.execute("INSERT INTO reports VALUES (%s, %s, %s, %s)", (newNum, subject, details, username))
        mydb.commit()

        print("Success")

        #Resets the view in case the user wants to create another report
        displayUI(window, username)
































#
