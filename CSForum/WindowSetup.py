import tkinter as tk
import HomePage
import ReportPage
import ProfilePage
import Messages
import ThreadPage
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


#Template for the window object that will be edited by each function
class Window:

    def __init__(self):

        #Initial size of the window
        self.height = 800
        self.width = 1200

        #Sets up the inital window
        self.root = tk.Tk()
        #Sets up the canvas for the window so it is resisable
        self.canvas = tk.Canvas(self.root, height=self.height, width=self.width)
        self.canvas.pack()

        #Placed in the root so it resises with the window
        self.frame = tk.Frame(self.root)
        self.frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    def refresh(self):

        #Deletes all the elements currently on the screen
        self.frame.destroy()
        #Creates the new frame
        self.frame = tk.Frame(self.root)
        self.frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    #Function to display the top navbar
    def displayNavbar(self, username):

        #Splits the window into the two main sections
        #Sets the frame for the top navbar
        self.navbar = tk.Frame(self.frame, bd=10, highlightbackground="black", highlightthickness=1)
        self.navbar.place(relwidth=1, relheight=0.075, relx=0, rely=0)

        #Adds icons to the top navbar
        #Button for the icon and navigating back to the homescreen
        self.icon = tk.Button(self.navbar, text="CS Forum", command=lambda: HomePage.displayUI(self, username, False))
        self.icon.place(relx=0, rely=0, relwidth=0.15, relheight=1)

        #Entry for the searchbar
        self.searchbar = tk.Entry(self.navbar)
        self.searchbar.place(relx=0.16, rely=0, relwidth=0.55, relheight=1)

        #Button to confirm your search
        self.search = tk.Button(self.navbar, text="Search", command=lambda: HomePage.displayUI(self, username, True, self.searchbar.get()))
        self.search.place(relx=0.72, rely=0, relwidth=0.1, relheight=1)

        #Button to take to you to the report page
        self.report = tk.Button(self.navbar, text="Report", command=lambda: ReportPage.displayUI(self, username))
        self.report.place(relx=0.88, rely=0, relwidth=0.05, relheight=1, anchor="ne")

        #Button to take you to your profile page
        self.profile = tk.Button(self.navbar, text="Profile", command=lambda: ProfilePage.displayUI(self, username))
        self.profile.place(relx=0.94, rely=0, relwidth=0.05, relheight=1, anchor="ne")

        #Button to bring up your messages
        self.messages = tk.Button(self.navbar, text="Messages", command=lambda: Messages.displayUI(self, username))
        self.messages.place(relx=1, rely=0, relwidth=0.05, relheight=1, anchor="ne")


    #Displays the side bar for threads the user is a member of
    def displaySidebar(self, username, threads):

        #Sets the frame for the side navbar
        self.sidebar = tk.Frame(self.frame, highlightbackground="black", highlightthickness=1, bd=5)
        self.sidebar.place(relwidth=0.2, relheight=0.925, relx=0, rely=0.075)

        #Adds the buttons to the sidebar
        self.memberThreadLabel = tk.Label(self.sidebar, text="Your Threads:")
        self.memberThreadLabel.pack()

        #Creates the vertical scrollbar for the sidebar
        self.scSidebar = sf.VerticalScrolledFrame(self.sidebar)
        self.scSidebar.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)

        self.userThreads = threads #Gets the threads the user is a member of

        self.buttons = {} #Dictionary to store the buttons in the sidebar

        #Adds all the buttons to the scrollable view and sets their function
        for i in range(0, len(self.userThreads)):
            self.buttons[i] = tk.Button(self.scSidebar.interior,
                                        text=self.userThreads[i],
                                        command=lambda a=i: ThreadPage.displayUI(self, username, self.userThreads[a]))
            self.buttons[i].pack(padx=10, pady=5, side=tk.TOP)








        #
