import tkinter as tk
import mysql.connector
import HomePage

#Connects to the database
mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  passwd = "sD6G7Bx@f8cve$i3",
  database = "forum"
)

#Allows editing of the database
mycursor = mydb.cursor()

#Displays the welcome page UI
def displayUI(window):

    #Splits the screens into the two sections
    signUpFrame = tk.Frame(window.frame, highlightbackground="black", highlightthickness=1)
    signUpFrame.place(relwidth=0.5, relheight=1, relx=0, rely=0)

    loginFrame = tk.Frame(window.frame, highlightbackground="black", highlightthickness=1)
    loginFrame.place(relwidth=0.5, relheight=1, relx=0.5, rely=0)


    #Input fields and labels for the signup section
    signUpLabel = tk.Label(signUpFrame, text="Sign Up")
    signUpLabel.place(relwidth=0.9, relheight=0.04, relx=0.05, rely=0.05)

    usernameLabel = tk.Label(signUpFrame, text="Username:", anchor="nw", justify="left")
    usernameLabel.place(relwidth=0.3, relheight=0.04, relx=0.05, rely=0.15)

    usernameSignUp = tk.Entry(signUpFrame)
    usernameSignUp.place(relwidth=0.9, relheight=0.05, relx=0.05, rely=0.2)

    password1Label = tk.Label(signUpFrame, text="Password:", anchor="nw", justify="left")
    password1Label.place(relwidth=0.3, relheight=0.04, relx=0.05, rely=0.35)

    password1SignUp = tk.Entry(signUpFrame)
    password1SignUp.place(relwidth=0.9, relheight=0.05, relx=0.05, rely=0.4)

    password2Label = tk.Label(signUpFrame, text="Repeat Password:", anchor="nw", justify="left")
    password2Label.place(relwidth=0.3, relheight=0.04, relx=0.05, rely=0.55)

    password2SignUp = tk.Entry(signUpFrame)
    password2SignUp.place(relwidth=0.9, relheight=0.05, relx=0.05, rely=0.6)


    #Input fields and labels for the login section
    loginLabel = tk.Label(loginFrame, text="Login")
    loginLabel.place(relwidth=0.9, relheight=0.04, relx=0.05, rely=0.05)

    usernameLabelLogin = tk.Label(loginFrame, text="Username:", anchor="nw", justify="left")
    usernameLabelLogin.place(relwidth=0.3, relheight=0.04, relx=0.05, rely=0.25)

    usernameLogin = tk.Entry(loginFrame)
    usernameLogin.place(relwidth=0.9, relheight=0.05, relx=0.05, rely=0.3)

    passwordLabel = tk.Label(loginFrame, text="Password:", anchor="nw", justify="left")
    passwordLabel.place(relwidth=0.3, relheight=0.04, relx=0.05, rely=0.45)

    passwordLogin = tk.Entry(loginFrame)
    passwordLogin.place(relwidth=0.9, relheight=0.05, relx=0.05, rely=0.5)


    #Adds the buttons to each frame
    #Lambda means that the function is run when the button is clicked not when the button is made
    signUpBtn = tk.Button(signUpFrame,
                    text="Sign up",
                    command=lambda: addUser(usernameSignUp.get(), password1SignUp.get(), password2SignUp.get(), window)
                )
    signUpBtn.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.75)

    loginBtn = tk.Button(loginFrame,
                    text="Login",
                    command=lambda: login(usernameLogin.get(), passwordLogin.get(), window)
                )
    loginBtn.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.75)

    window.root.mainloop()

#Takes the user details and adds them to the database
def addUser(username, password1, password2, window):

    #Clears all the leading and trailing whitespace
    username = username.strip()
    password1 = password1.strip()
    password2 = password2.strip()

    #Ensures all the fields have been completed
    if username == "" or password1 == "" or password2 == "":
        print("Complete all fields")
    else:
        #Ensures the user does not already exist
        if checkForExistingUser(username):
            print("User already exists")
        else:
            #Ensures both passwords match
            if password1 != password2:
                print("Passwords do not match")
            else:
                #Inserts the user into the database
                mycursor.execute("INSERT INTO users VALUES (%s, %s)", (username, password1))
                mydb.commit() #Makes the entry permanent
                HomePage.displayUI(window, username, False) #Takes the user to the homepage

#Returns true if there is a user with that username
def checkForExistingUser(username):

    #Counts the number of rows that have the given username
    mycursor.execute("SELECT COUNT(username) FROM users WHERE username = %s", (username, ))

    #Stores the count
    count = mycursor.fetchall()[0][0]

    if count == 0:
        return False
    else:
        return True


def login(username, password, window):

    #Clears all the leading and trailing whitespace
    username = username.strip()
    password = password.strip()

    #Ensures all the fields have been completed
    if username == "" or password == "":
        print("Complete all fields")

    else:
        #Ensures the user exists in the database
        if not checkForExistingUser(username):
            print("User does not exist")

        #Logs the user in
        else:
            #Fetches the password for the specified user
            mycursor.execute("SELECT password FROM users WHERE username = %s", (username, ))

            #Stores the password from the database
            dbPassword = mycursor.fetchall()[0][0]

            if dbPassword == password:
                print("Success")
                #Displays the homepage for the user
                HomePage.displayUI(window, username, False)
            else:
                print("Password wrong")




















#hello
