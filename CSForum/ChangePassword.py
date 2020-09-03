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

#Displays the change password page UI
def displayUI(window, username):

    window.refresh() #Clears the Window

    window.displayNavbar(username)

    #Adds the frame for the main section of the frame
    mainPage = tk.Frame(window.frame)
    mainPage.place(relwidth=1, relheight=0.925, relx=0, rely=0.075)

    #Input fields and labels
    changeLabel = tk.Label(mainPage, text="Change Password")
    changeLabel.place(relwidth=0.9, relheight=0.04, relx=0.05, rely=0.05)

    oldPasswordLabel = tk.Label(mainPage, text="Old Password:", anchor="nw", justify="left")
    oldPasswordLabel.place(relwidth=0.3, relheight=0.04, relx=0.05, rely=0.15)

    oldPassword = tk.Entry(mainPage)
    oldPassword.place(relwidth=0.9, relheight=0.05, relx=0.05, rely=0.2)

    newPassword1Label = tk.Label(mainPage, text="New Password:", anchor="nw", justify="left")
    newPassword1Label.place(relwidth=0.3, relheight=0.04, relx=0.05, rely=0.35)

    newPassword1 = tk.Entry(mainPage)
    newPassword1.place(relwidth=0.9, relheight=0.05, relx=0.05, rely=0.4)

    newPassword2Label = tk.Label(mainPage, text="Repeat New Password:", anchor="nw", justify="left")
    newPassword2Label.place(relwidth=0.3, relheight=0.04, relx=0.05, rely=0.55)

    newPassword2 = tk.Entry(mainPage)
    newPassword2.place(relwidth=0.9, relheight=0.05, relx=0.05, rely=0.6)


    #Adds the confirm button
    #Lambda means that the function is run when the button is clicked not when the button is made
    confirmBtn = tk.Button(mainPage,
                    text="Confirm",
                    command=lambda: changePassword(username, oldPassword.get(), newPassword1.get(), newPassword2.get(), window)
                 )
    confirmBtn.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.75)

def changePassword(username, p1, p2, p3, window):
    # Here p1 refers to the current password of the user
    # p2 and p3 refers to the new password

    #Ensures all the fields have been completed
    if p1 == "" or p2 == "" or p3 == "":
        print("Complete all fields")
    else:
        #Fetches the password for the specified user
        mycursor.execute("SELECT password FROM users WHERE username = %s", (username, ))

        #Stores the password from the database
        dbPassword = mycursor.fetchall()[0][0]

        #Ensures it is the correct user that is changing the password
        if dbPassword != p1:
            print("Incorrect password")
        else:
            #Ensures the user does not make a typo while entering the new password
            if p2 != p3:
                print("Passwords do not match")
            else:
                #Updates the users password
                mycursor.execute("UPDATE users SET password = %s WHERE username = %s",
                                 (p2, username))
                mydb.commit()
                print("Success")
                #Refreshes the window
                displayUI(window, username)


























#
