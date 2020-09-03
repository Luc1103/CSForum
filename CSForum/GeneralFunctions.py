import ThreadPage
import mysql.connector
import Sorting

#Connects to the database
mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  passwd = "sD6G7Bx@f8cve$i3",
  database = "forum"
)

######Think I do not need this file

#Allows editing of the database
mycursor = mydb.cursor()

#Function to find the index of highest number in a list
def findHighestIndex(list1):

    highest = 0 #Stores the current highest number
    index = 0  #Stores the index of the current highest number

    #Iterates through every number in the list "i" representing the index of each
    for i in range(0,len(list1)):
        #Updates the values accordingly
        if list1[i] > highest:
            highest = list1[i]
            index = i

    return index


















#
