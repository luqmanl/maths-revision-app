'''Importing required libraries and scripts'''
#As kivy is massive, it is more efficient to import only a subset
#of the library's scripts
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import kivy.uix.button as kb
#Importing turtle module for any games that will need to be created
#as turtle module is more optimised than kivy in that specific purpose
import turtle
#Importing libraries required for mathematical analysis and graphing
import math
import numpy as np
import matplotlib.pyplot as plt
#Importing other required modules for the program#
#Hash Library for password hashing
import hashlib
#sqlite3 for all database operations
import sqlite3
#Random to generate random numbers or to pick random questions
#within a list
import random
#tabulate to make summary data outputs for user look nicer and easier to understand
from tabulate import tabulate
#Importing date time library used for scheduled date
import datetime
from datetime import date
#SMTP Library for using the SMTP Application-Layer protocol to send emails to students and teachers
import smtplib

'''Data Type Checking Functions'''
#Checks if the argument is an integer
def isInteger(UserInput):
    #uses try and except functionality
    try:
        #Attempts to convert input into an integer
        IntCheck = int(UserInput)
        #If its successful then it returns True
        return True
    #If it fails, then it returns False
    except ValueError:
        return False

#Checks if the argument is a string
def isString(UserInput):
    #uses try and except functionality
    try:
        #Attempts to convert input into a string
        StrCheck = str(UserInput)
        #If its successful then it returns True
        return True
    #If it fails, then it returns False
    except ValueError:
        return False

'''Stack Class'''
#Creating my stack data structure with its related methods as its own class
#This allows me to create a stack by instantiating it as an object of the class and
#always have these methods available to use with the stack
class Stack():
    #Constructor method creates a Python list and is used with object
    def __init__(self):
        self.elements = []
    #defining push method which adds a data element on the top of the stack
    def push(self, element):
        self.elements.append(element)
    #defining pop method which pops off the top element item
    def pop(self):
        return self.elements.pop()
    #defining method to return the contents of the stack when called
    def viewStack(self):
        return self.elements
    #Also have a method to check if the stack is empty
    def isEmpty(self):
        #checks if the stack equals an empty stack
        return self.elements == []
            
''''Pop Up Window Function''' 
#Defining my own general version of the popup tool kivy uses
#This is to reduce code repetition and improve efficiency
def PoppingUp(PopName,Text):
   #Defines a new popup with title and text given by arguments of my function
   GeneralPop = Popup(title=PopName,
              content=Label(text=Text),
              size_hint=(None, None),size=(600, 200))
   #Opens this popup on the screen
   GeneralPop.open()

'''General Database Functions'''
#Connecting or Disconnecting from database function
def DataConnect(process):
   if process == 'connect':
      #creating a connection with the database, it will be global as
      #other queries will use it, but the connection itself won't ever change
      global connection
      connection = sqlite3.connect("Mathematics.db")
      #Using a global sqlite cursor object in order to fetch results from any query when needed
      global crsr
      crsr = connection.cursor() 
   elif process == 'disconnect':
      #To ensure the SQL Query is executed
      connection.commit()
      #This closes the connection to register all changes made to the database
      connection.close()

#My generalised funtion for returning data from a database in a list for comparisons.
def FindData(Column, Table):
      #connecting to database
      DataConnect('connect')
      #Creating sql query to select data
      crsr.execute(''' SELECT %s from %s ''' %(Column, Table))
      #creating an empty list
      StoredList = []
      #Iterates through the results of the query
      for row in crsr.fetchall():
         #appends data to 'StoredList' list as a string
         StoredList.append((row[0]))
      return StoredList

#A more useful DataSearch Function where I can define my own query
#and convert the recieved list of tuples into a list of mutable data items
def DataSearch(Query):
    #connecting to database
    DataConnect('connect')
    #Creating an executable query which i can define to select data
    crsr.execute(Query)
    #creating an empty list
    StoredList = []
    #Iterates through the results of the query
    for row in crsr.fetchall():
    #appends data to 'StoredList' list as a string
        StoredList.append((row[0]))
    #The list of data is returned
    return StoredList

#Sets new ids for any of the table to ensure there is no repeated ids
def IncrementID(Query):
    #A MAX SQL aggregate function will be used in conjunction with this
    #It will use my DataSearch function to find the highest ID already set in the desired table
    MaxList = DataSearch(Query)
    #The value of the id will be stored in a variable called MaxID
    MaxID = MaxList[0]
    #This condition will check if there is nothing in the database for that table in the ID column
    if MaxID == None or MaxID == '':
        #If there isn't, then it is a new entry and therefore the ID will be set to 1
        NewID = 1
    else:
        #Otherwise, it will add one onto the MaxID 
        NewID = int(MaxID) + 1
    #The NewID is returned by the function
    return NewID



'''Main Code and GUI'''


'''Login and Registration Screen and Associated Functions'''
#Creating the log in screen as its own class and inheriting
#from the Screen and BoxLayout Superclasses
class LoginScreen(Screen, BoxLayout):
   #Creating subroutine linked to Log In button 
   def LogIn(self):
      #creates a list of all emails
      StoredEmails = FindData('Email', 'User')
      #stores user input in Username field in a variable
      global UserCheck
      UserCheck = self.ids.username_field.text
      #Checks if the user input is in the list of Stored emails from the database
      if UserCheck in StoredEmails:
         #If the condition is met, the program 
         PassCheck = self.ids.password_field.text
         #password entered is hashed with sha256 for verification checks
         PassCheck = hashlib.sha256(PassCheck.encode()).hexdigest()
         #Uses string formatting to query hashed password from database
         crsr.execute(''' SELECT HashedPassword FROM User WHERE Email=? ''', (UserCheck,))
         for row in crsr.fetchall():
            #Stores hashed value in different variable
            PassChecked = row[0]
         #compares hashed user input with hashed password in database
         if PassCheck == PassChecked:
            #if they match then they are presented with the home screen
            self.manager.current = 'Home'
         #Otherwise an error pops up telling them their password is incorrect
         else:
            PoppingUp('Password Error', 'Your password is incorrect')
      #if the username doesn't exist in the database, the user is informed.
      else:
         PoppingUp('Username Error','Username Not Found!')
         
      
#Creating the register screen as its own class and inheriting
#from the Screen and BoxLayout Superclasses
class RegisterScreen(Screen, BoxLayout):
   #using a constructor method with variable keyword arguments
   def __init__(self, **kwargs):
      super().__init__(**kwargs)
   #User Registration method for new account
   def CreateAcc(self):
      taken = FindData('Email', 'User')
      #Stores all entered text from the GUI in variables to be used 
      CreateUser = self.ids.email_field.text
      CreatePass = self.ids.NewPwd_field.text
      CheckPass = self.ids.RePwd_field.text
      NewFname = self.ids.Fname_field.text
      NewLname = self.ids.Lname_field.text
      NewStatus = self.ids.StudentS_field.text
      #Checks that there are no empty fields
      if CreateUser == '' or CreatePass == '' or CheckPass == '' or NewFname == '' or NewLname == '' or NewStatus == '':
         #if an empty field is found, a pop up is used to inform the user to retry
         PoppingUp('Empty Field','One or more fields are empty! Please fill them all in.')
      else:
         #If no empty fields found, the email is checked to see if it is already taken
         if CreateUser in taken:
            #if email is taken then a pop up informing the user to retry is shown
            PoppingUp('Existing Username','This username is already taken! Please try another one.')
         else:
            #if email is unique, it is stored in a new variable to be used
            NewEmail = CreateUser
            #This conditional statement will check which type of user it is (student or teacher)
            NewStatus = NewStatus.lower() == "student"
        
            #Checks if the two entered passwords match each other
            if CreatePass != CheckPass:
               #if they don't match then a pop is used
               PoppingUp('No Match', 'Passwords do not match! Please try again.')
          
            else:
               #Uses sha256 hashing algorithm to ensure the password cannot be easily acquired
               NewHashP = hashlib.sha256(CreatePass.encode()).hexdigest()
               #Inserts all new user data, after meeting all required conditions, in the User table
               crsr.execute(''' INSERT INTO User(Email, FirstName, LastName, HashedPassword, Student_Status)
               VALUES (?,?,?,?,?)''', (NewEmail, NewFname, NewLname, NewHashP, NewStatus))
               #Creating a new ID for the progress table for this new user using an SQL aggregate function
               NewID = IncrementID('''Select MAX(ProgressID) FROM Progress''')
               #Inserting this into the progress table
               crsr.execute('''INSERT INTO Progress(ProgressID, Email) VALUES(?,?)''',(NewID, NewEmail))
               #closing the connection with database
               DataConnect('disconnect')
               #A pop is used to inform the user that the account has been successfully created
               PoppingUp('Account Created', "Account Successfully Created!")
    

#Creating the seperate screens as their own classes and inheriting
#from the Screen and respective layout Superclasses
class FeatureScreen(Screen, FloatLayout):
    #using a constructor method with variable keyword arguments
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class HomeScreen(Screen, BoxLayout):
   #using a constructor method with variable keyword arguments
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    #Defining function to check which progress screen the user goes to
    #depending on if they are a teacher or student
    def Progress(self):
        #connects to the database
        DataConnect('connect')
        #Finds the student status using an sql query
        crsr.execute(''' SELECT Student_Status FROM User WHERE Email=? ''', (UserCheck,))
        #Stores this in a variable called status
        for row in crsr.fetchall():
            status = int(row[0])
        #if the student_status is 0 then it means it is a teacher account and
        #so moves on to the teacher progress screen
        if status == 0:
            self.manager.current = 'TeacherProgress'
        #otherwise it goes to the standard student progress screen
        else:
            self.manager.current = 'Progress'
            

'''Maths Topic Test'''
#Topic test screen for users to practice their maths
class TopicTestScreen(Screen):
    #function to return the topics needed
    def WhichTopics(self):
        #Create a new list to check which topics will be in the test
        chosen_topics = []
        #Storing the status of each of the checkboxes in variables to be used
        CheckTrig = self.ids.trig_check.active
        CheckCalc = self.ids.calculus_check.active
        CheckStats = self.ids.stat_check.active
        #using boolean conditions to check status of each
        if not CheckTrig and not CheckCalc and not CheckStats:
            #if no check box is pressed then False is returned
            return False
        else:
        #checking through each checkbox to see if it is activated
            if CheckTrig:
                #if it is activated it will append the ids of the questions to the chosen topics list
                crsr.execute('''SELECT QuestionID FROM Topic WHERE QuestionID BETWEEN 500 AND 599''')
                for trig in crsr.fetchall():
                    chosen_topics.append(trig[0])
            #Same for the next two checkboxes
            if CheckCalc:
                crsr.execute('''SELECT QuestionID FROM Topic WHERE QuestionID BETWEEN 100 AND 299''')
                for calc in crsr.fetchall():
                    chosen_topics.append(calc[0])
            if CheckStats:
                crsr.execute('''SELECT QuestionID FROM Topic WHERE QuestionID BETWEEN 300 AND 399''')
                for stat in crsr.fetchall():
                    chosen_topics.append(stat[0])
            #The list of question ids are returned
            return chosen_topics

    #Function to automatically choose the question based on user's topic choices
    def WhichQuestion(self):
            #Connects to Database
            DataConnect('connect')
            #Stores the topics taken from the WhichTopics Function
            QuestionsToChoose = TopicTestScreen.WhichTopics(self)
            #Chooses a random id from the list of questions that were taken
            global NewQuestionID
            NewQuestionID = random.choice(QuestionsToChoose)
            #Finds the associated question with that ID from database
            crsr.execute('''SELECT Question FROM Topic WHERE QuestionID=?''',(NewQuestionID,))
            #Stores that question in the MainQuestion variable
            for Ques in crsr.fetchall():
                MainQuestion = Ques[0]
            #Finds the associated answer with that ID from the database
            crsr.execute('''SELECT Answer FROM Topic WHERE QuestionID=?''',(NewQuestionID,))
            #Stores that question in the MainQuestion variable
            for Ans in crsr.fetchall():
                MainAnswer = Ans[0]
            #Disconnects from the database
            DataConnect('disconnect')
            #Returns the Question and Answer
            return MainQuestion, MainAnswer

    #Function to obtain number of correct answers and total answers for each topic
    #with incrementing total value to show a new question was attempted
    def ProgressObtain(self):
        #Connecting to database
        DataConnect('Connect')
        #Assgining global variable from different function to a
        #local variable to prevent any side effects from occuring
        QuestionID = NewQuestionID
        #Checks if the question id which matches the differentiation ids
        if QuestionID >= 100 and QuestionID <=199:
            #Uses an sql query to find the total and correct values for differentiation topic
            crsr.execute('''SELECT DiffCorrect, DiffTotal FROM Progress WHERE Email =?''', (UserCheck,))
            #Assigns the integer values of the query return to variables
            for row in crsr.fetchall():
                DiffCorrect = int(row[0])
                DiffTotal = int(row[1])
            #Increments the total answered questions for topic by 1
            DiffTotal+=1 
            return QuestionID, DiffCorrect, DiffTotal
        #Similar sets of code as above for other topics in program
        elif QuestionID >= 200 and QuestionID <=299:
            #Uses an sql query to find the total and correct values for the integration topic
            crsr.execute('''SELECT IntCorrect, IntTotal FROM Progress WHERE Email =?''', (UserCheck,))
            #Assigns the integer values of the query return to variables
            for row in crsr.fetchall():
                IntCorrect = int(row[0])
                IntTotal = int(row[1])
            #Increments the total answered questions for integration topic by 1
            IntTotal+=1 
            return QuestionID, IntCorrect, IntTotal
        #data obtained for statistics topic 
        elif QuestionID >= 300 and QuestionID <=399:
            #Uses an sql query to find the total and correct values for the Statistics topic
            crsr.execute('''SELECT StatCorrect, StatTotal FROM Progress WHERE Email =?''', (UserCheck,))
            #Assigns the integer values of the query return to variables
            for row in crsr.fetchall():
                StatCorrect = int(row[0])
                StatTotal = int(row[1])
            #Increments the total answered questions for tatistics topic by 1
            StatTotal+=1 
            return QuestionID, StatCorrect, StatTotal
        #Code for Trigonometry topic
        elif QuestionID >= 500 and QuestionID <=599:
            #Uses an sql query to find the total and correct values for the integration topic
            crsr.execute('''SELECT TrigCorrect, TrigTotal FROM Progress WHERE Email =?''', (UserCheck,))
            #Assigns the integer values of the query return to variables
            for row in crsr.fetchall():
                TrigCorrect = int(row[0])
                TrigTotal = int(row[1])
            #Increments the total answered questions for integration topic by 1
            IntTotal+=1 
            return QuestionID, TrigCorrect, TrigTotal
        #Disconnecting from the database
        DataConnect('disconnect')
    
    #Function to update database and questions accordingly
    #if the user's answer was correct
    def ProgressUpdate(self, Outcome):
        #Connecting to database
        DataConnect('connect')
        #Assigning values acquired from progress obtain function
        QuestionID, Correct, Total = self.ProgressObtain()
        #if outcome was correct the Correct Variable is incremented by 1
        #otherwise it remains the same, this allows me to use one function to
        #carry out the tasks for updating the datbase when a correct or incorrect
        #answer is given
        if Outcome == 'Success':
            Correct+=1
        #Checks ids match differentiation topic ids
        if QuestionID >= 100 and QuestionID <=199:
            #Updating database to reflect these changes for that user
            #For the differentiation topic
            crsr.execute('''INSERT INTO DiffCorrect, DiffTotal
                        VALUES(?,?) WHERE Email=?''', ((Correct,), (Total,), (UserCheck,)))
        #Checking ids for integration topic
        elif QuestionID >= 200 and QuestionID <=299:
            #Updating database to reflect these changes for that user
            #For the Integration topic
            crsr.execute('''INSERT INTO IntCorrect, IntTotal
                        VALUES(?,?) WHERE Email=?''', ((Correct,), (Total,), (UserCheck,)))
        #Checking ids for Statistics topic
        elif QuestionID >= 300 and QuestionID <=399:
            #Updating database to reflect these changes for that user
            #For the Statistics topic
            crsr.execute('''INSERT INTO StatCorrect, StatTotal
                        VALUES(?,?) WHERE Email=?''', ((Correct,), (Total,), (UserCheck,)))
        #Checking ids for Trigonometry topic
        elif QuestionID >= 500 and QuestionID <=599:
            #Updating database to reflect these changes for that user
            #For the Trigonometry topic
            crsr.execute('''INSERT INTO TrigCorrect, TrigTotal
                        VALUES(?,?) WHERE Email=?''', ((Correct,), (Total,), (UserCheck,)))
        #Disconnecting from database and committing any commands that have been used
        DataConnect('disconnect')
        
        
    #Creating a method to check the user's answer
    def CheckAnswer(self):
        #First stores the user input in a variable
        CheckingAnswer = txt1.text
        #Connects to the database
        DataConnect('connect')
        #The answers are stored as a string with a list of answers inside
        #the eval converts it into a list and the answer can be searched through
        #That way many possible variations of the answer can be checked and it is NOT a
        #multiple choice test
        if CheckingAnswer in eval(MainA):
            #Stops the test to show user the result of their answer
            QuestionPopup.dismiss()
            #Pops up with correct answer statement
            PoppingUp('Answer', 'Answer correct!')
            #Running code to update database on correct answer
            self.ProgressUpdate('Success')

        else:
            #Similar to code above except it pops up with incorrect answer statement
            QuestionPopup.dismiss()
            #Tells user their answer was incorrect
            PoppingUp('Answer', 'Answer Incorrect!')
            #Updates database for wrong answer
            self.ProgressUpdate('Fail')

    #Function to open up test for user with inputs and screen widgets
    def StoreQA(self):
        #setting questions and answer as global class variables to be used with any method in this class
        global MainQ
        global MainA
        #Uses WhichQuestion function and stores the output question and answer in the two variables
        MainQ, MainA = TopicTestScreen.WhichQuestion(self)
        
        #Creating the widgets required for the test
        box = BoxLayout(orientation = 'vertical', padding = (10))
        #This is the question being outputted, taken from the database
        box.add_widget(Label(text = MainQ))
        #Creating the button to submit
        btn1 = kb.Button(text = 'Submit', background_color =(1,1,1,1), pos = (700,20), size_hint = (.1,.05))
        #Creating a global class variable which stores the user input for the question
        global txt1
        txt1 = TextInput(hint_text = 'Enter Your Answer', pos = (150,20), size_hint = (0.5, 0.08))
        #adding all of the widgets to the box layout
        box.add_widget(btn1)
        box.add_widget(txt1)
        #Setting up the Test using a popup without ability to dismiss by clicks
        global QuestionPopup
        QuestionPopup = Popup(title='Topic Test', title_size= (30), 
                      title_align = 'center', content = box,
                      auto_dismiss = False)
        #Setting button bind to CheckAnswer method created already
        btn1.bind(on_press = TopicTestScreen.CheckAnswer)
        #Opens this popup on the screen
        QuestionPopup.open()

'''First Maths Revision Game (MathsInvaders)'''
#Screen which has option to play game or view scores
#through buttons using kv
class MathsInvadersScreen(Screen):
    pass

#Screen to view game scores
class ViewLeaderboardScreen(Screen):
    #Creating a new leaderboard variable with a string property
    Leaderboard = StringProperty()
    #using a constructor method with variable keyword arguments
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #using the timetable variable as an attribute of the class' objects
        Leaderboard = str()

    #Merge sort leaderboard function for 
    def MergeSortBoard(self, LeaderSort):
        #checks if the list has more than 1 element to be sorted
        if len(LeaderSort)>1:
            #creates the midpoint using the integer division by 2
            mid=len(LeaderSort)//2
            #creates two lists by halving them
            left = LeaderSort[0:mid]
            right = LeaderSort[mid::]

            #recursively calls the function to split the list further
            MergeSort(left)
            MergeSort(right)
            #assigns 3 variables used for indexes to 0
            left_pointer = right_pointer = final_pointer = 0
            #checks that left and right pointers are less than the total number of elements
            while left_pointer < len(left) and right_pointer < len(right):
                #compares the term in the left to the term in the right list
                if left[left_pointer] < right[right_pointer]:
                    #if the left[left_pointer] is smaller, it replaces the term in the inputted list
                    LeaderSort[final_pointer]=left[left_pointer]
                    #left pointer is incremented
                    left_pointer+=1
                #otherwise the right list element is taken
                else:
                    LeaderSort[final_pointer]=right[right_pointer]
                    right_pointer+=1
                #final pointer is incremented by 1
                final_pointer+=1
            #if no more values in either of the LeaderSort lists then these loops are used
            #Finds and appends remaining values in the left list to final list
            while left_pointer < len(left):
                LeaderSort[final_pointer]=left[left_pointer]
                left_pointer+=1
                final_pointer+=1
            #Finds and appends remaining values in the left list to final list
            while right_pointer < len(right):
                LeaderSort[final_pointer]=right[right_pointer]
                right_pointer+=1
                final_pointer+=1
            #function values are returned in case of use further on for calculations
            return LeaderSort

        else:
            #if list has 1 element or none then its automatically returned as it can't be sorted further
            return LeaderSort
        
        
    #Defining view leaderboard function to allow the user to see all the game scores
    def ViewLeaderboard(self):
        #Connecting to database
        DataConnect('connect')
        #Querying data from database and storing it in a variable to be ready for output
        GameLeaderboard = crsr.execute('''SELECT Email, GameScore, MathScore FROM MathsInvader''')
        #Runs merge sort algorithm to sort out the leaderboard, with mathscore being prioritised
        GameLeaderboard = self.MergeSortBoard(GameLeaderboard)
        #Creating the headings for the displayed table on screen
        GameHeadings = ['Email', 'Game Score', 'Maths Score']
        #Tabulates the data and updates the leadeboard variable on screen
        self.Leaderboard = tabulate(GameLeaderboard, headers = GameHeadings, tablefmt = "grid")
        #Disconnecting from database
        DataConnect('disconnect')

#Main Game class and screen
class MathsInvadersGame(Screen):
    #using a constructor method with variable keyword arguments
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    #Defining function to update database when game is played
    def GameData(self, GameScore, MathScore):
        #Connecting to database
        DataConnect('connect')
        #Selecting progress id to match with user's email
        crsr.execute('''SELECT ProgressID From Progress WHERE Email=?''', (UserCheck,))
        #Storing progress id for that user in a variable
        for row in crsr.fetchall():
            ProgressID = Row[0]
        #Creating a new GameID for the game session using my IncrementID function
        GameID = IncrementID('''Select MAX(GameID) FROM MathsInvader''')
        #Inserting all information into the database
        crsr.execute('''INSERT INTO MathsInvader(GameID, Email, ProgressID, GameScore, MathScore
                    VALUES(?,?,?,?,?)''', (GameID, UserCheck, ProgressID, GameScore, MathScore))
        #Comitting all commands and disconnecting from database
        DataConnect('disconnect')
        
    #Creating a function to allow the user to move left and right
    def MoveLeft(self):
            #Finds user's x coordinate
            x = player.xcor()
            #Moves player the amount of pixels that the speed is set to
            x -= playerspeed
            if x < -280:
                    x = - 280
            #Shows player on that position on screen
            player.setx(x)

    #This function is the same as above but inversed the negative to move right instead
    def MoveRight(self):
            x = player.xcor()
            x += playerspeed
            if x > 280:
                    x = 280
            player.setx(x)

    #function for how the bullet is shot when spacebar is pressed
    def FireBullet(self):
            #Declare bulletstate as a global variable as it will change outside the function
            global bulletstate
            #Checks if the bullet is ready to fire
            if bulletstate == "ready":
                    #changes bullet state to fire mode
                    bulletstate = "fire"
                    #Move the bullet to the just above the player
                    x = player.xcor()
                    y = player.ycor() + 10
                    bullet.setposition(x, y)
                    bullet.showturtle()

    #Function to check if a collision occurs
    def isCollision(self, t1, t2):
            #Using the cartestian coordinates distance formula to work out how far
            #an alien is from the student spaceship
            distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
            #Checks the distance is less than 15 as that is when the alien would be touching the user
            return distance < 15
                    
     
    #Setting game as a function to be run when button is pressed  
    def MathsInvadersGame(self):
        #Using turtle mod to create a screen for which the game can be played on
        #as kivy alone will not be able to track movement
        MathsInvaders = turtle.Screen()
        #Set the colour to black
        MathsInvaders.bgcolor("black")
        #Naming it as Maths Invaders, as it is related to a maths application
        MathsInvaders.title("Maths Invaders")
        #Found an online background image to match with the space invaders theme
        MathsInvaders.bgpic("MathsInvaders_Images/MathsInvaders - Background.gif")
        #Also used images for the aliens and the user controlled ship from online
        turtle.register_shape("MathsInvaders_Images/Alien.gif")
        turtle.register_shape("MathsInvaders_Images/Student.gif")

        #Creating the border around the game using turtle module
        SpaceCreator = turtle.Turtle()
        #Changed the speed from 0 to create an interesting animation when opened
        SpaceCreator.speed(10)
        #Setting the colour of the border
        SpaceCreator.color("green")
        SpaceCreator.penup()
        SpaceCreator.setposition(-300,-300)
        SpaceCreator.pendown()
        #Creating the size of the border
        SpaceCreator.pensize(10)
        #Creating a 4 sided square border around main game area
        for side in range(4):
                #pen moves forward for 600 pixels
                SpaceCreator.fd(600)
                #pen takes a 90 degree left turn 
                SpaceCreator.lt(90)     
        #After the borders and the main space is setup the pen can be hidden
        SpaceCreator.hideturtle()	

        #The user's Maths and Game Scores begins at 0
        GameScore = 0
        MathScore = 0
        #Showing the game score on the top left corner for the user to see
        score_pen = turtle.Turtle()
        #Score shown instantly
        score_pen.speed(0)
        #Setting colour of score text
        score_pen.color("white")
        score_pen.penup()
        #Setting at top left corner
        score_pen.setposition(-290, 270)
        #Creating a string showing it is the Game score
        GameScoreText = "Game Score: %s" %GameScore
        #Setting textual styles and font size to the Game Score indicator
        score_pen.write(GameScoreText, False, align="left", font=("Arial", 15, "normal"))
        #Pen is hidden once finished making score
        score_pen.hideturtle()

        #Similar code below but to draw maths score as well
        #Showing the game score on the top left corner for the user to see
        mscore_pen = turtle.Turtle()
        #Maths Score shown instantly
        mscore_pen.speed(0)
        #Setting colour of score text
        mscore_pen.color("red")
        mscore_pen.penup()
        #Setting at top left corner
        mscore_pen.setposition(-140, 270)
        #Creating a string showing it is the Game score
        MathScoreText = "Maths Score: %s" %MathScore
        #Setting textual styles and font size to the Maths Score indicator
        mscore_pen.write(MathScoreText, False, align="left", font=("Arial", 15, "normal"))
        #Pen is hidden once finished making score
        mscore_pen.hideturtle()

        #Creating the Student's Spaceship
        player = turtle.Turtle()
        #Using blue colour for spaceship
        player.color("blue")
        #using downloaded image to replace base image
        player.shape("MathsInvaders_Images/Student.gif")
        player.penup()
        player.speed(0)
        player.setposition(0, -250)
        player.setheading(90)
        #Setting how fast the player can move
        playerspeed = 15

        #Setting the amount of aliens that are on screen
        number_of_aliens = 5
        #Create an empty list for the aliens
        aliens = []
        #Add each alien on screen to the list using for loop
        for i in range(number_of_aliens):
                #Create the alien
                aliens.append(turtle.Turtle())

        #Creating the aliens themselves with required design
        for alien in aliens:
                #setting alien colour to red
                alien.color("red")
                #using the downloaded image file as the alien
                alien.shape("MathsInvaders_Images/Alien.gif")
                alien.penup()
                alien.speed(0)
                #Aliens 'spawn' in at a random point at start using random integer
                #for both x and y coordinates, with the range within the borders of the game
                x = random.randint(-200, 200)
                y = random.randint(100, 250)
                #sets the starting position of the alien
                alien.setposition(x, y)
        alienspeed = 5


        #Create the spaceship's bullet
        bullet = turtle.Turtle()
        bullet.color("blue")
        #using a triangular shaped bullet
        bullet.shape("triangle")
        bullet.penup()
        bullet.speed(0)
        bullet.setheading(90)
        bullet.shapesize(0.5, 0.5)
        bullet.hideturtle()
        #Setting the bullet's speed 
        bulletspeed = 20

        #Define bullet state
        #ready - ready to fire
        #fire - bullet is firing
        global bulletstate
        bulletstate = "ready"
        
        #Create keyboard bindings to allow student
        #to control spaceship with respective keys
        turtle.listen()
        turtle.onkey(self.MoveLeft, "Left")
        turtle.onkey(self.MoveRight, "Right")
        turtle.onkey(self.FireBullet, "space")

        #Main game loop
        while True:
                #Allow all aliens to keep moving in the horizontal direction
                for alien in aliens:
                        #Move the enemy
                        x = alien.xcor()
                        #uses alien speed to move the amount of pixels per second
                        x += alienspeed
                        alien.setx(x)
                        #If aliens reach border, they move down a step
                        if alien.xcor() > 280:
                                #This loops so all aliens are moved down
                                for a in aliens:
                                        y = a.ycor()
                                        y -= 40
                                        a.sety(y)
                                #The direction is switched so they move towards opposite border
                                alienspeed *= -1
                        #This performs the same actions as above but for the opposite border
                        if alien.xcor() < -280:
                                #This loops so all aliens are moved down
                                for a in aliens:
                                        y = a.ycor()
                                        y -= 40
                                        a.sety(y)
                                #The direction is switched so they move towards opposite border
                                alienspeed *= -1
                                
                        #This checks if a collision occurs between a bullet and alien using function
                        if self.isCollision(bullet, alien):
                                #The bullet gets reset and its state changes to ready mode
                                bullet.hideturtle()
                                bulletstate = "ready"
                                bullet.setposition(0, -400)
                                #The enemy also gets reset so student can attempt to reach higher scores
                                x = random.randint(-200, 200)
                                y = random.randint(100, 250)
                                alien.setposition(x, y)
                                #The GameScore increases by 100 per success
                                GameScore += 100
                                GameScoreText = "Game Score: %s" %GameScore
                                score_pen.clear()
                                #Setting textual styles and font size to the Game Score indicator
                                score_pen.write(GameScoreText, False, align="left", font=("Arial", 15, "normal"))

                        #This checks a collision occurs between the student and alien
                        if self.isCollision(player, alien):
                                #The alien and player both get taken off the screen
                                player.hideturtle()
                                alien.hideturtle()
                                #Iterates over 3 times to give player another chance
                                #Opens up Topic Test Screen to allow user to gain another chance
                                #by answering questions
                                self.manager.current = 'TopicTest'
                                #Works out topics for testing
                                TopicTestScreen.WhichTopics()
                                #Question pops up
                                TopicTestScreen.StoreQA()
                                #Answer is checked and updates progress database table
                                TopicTestScreen.CheckAnswer()
                                #Checks if user input was correct
                                if txt1.text in eval(MainA):
                                    #adds on 100 score to the math score
                                    MathScore+=100
                                #After Question is complete the database is updated
                                self.GameData(GameScore, MathScore)
                                #Once the chances have finished, the game ends and a message is popped up
                                PoppingUp('End', 'You have no more lives remaining!')
                                break
                        
                #This sets how the bullet will move up when in fire mode
                if bulletstate == "fire":
                        #sets y coordinate and moves according to bulletspeed variable
                        y = bullet.ycor()
                        y += bulletspeed
                        bullet.sety(y)
                
                #If the bullet has reached the top border
                if bullet.ycor() > 275:
                        #Bullet gets hidden from screen
                        bullet.hideturtle()
                        #Bullet set to fire mode so student can shoot again
                        bulletstate = "ready"


'''Revision Classes for Calculus associated Screens and Functions'''  
class CalculusScreen(Screen, BoxLayout):
    pass

class CalculusSeries(Screen, BoxLayout):
    #using a constructor method with variable keyword arguments
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    #Defining the recursive factorial function
    def Factorial(n):
        #For recursion, I must establish my base case and I will cover all
        #non-negative integers as that is what the series uses, starting from 0
        if n == 0:
            #this is for returning 1 if n = 0
            return 1
        else:
            #Otherwise it calls itself recursively to find the nth factorial number
            return n * CalculusSeries.Factorial(n-1)
    #defining factorial link to user interface function when calculate button is pressed
    def giveFactorial(self):
        #taking in user input from the text input field
        InputNumber = self.ids.Factorial.text
        #checks if the number is an integer and the field is not empty
        if InputNumber != '' and isInteger(InputNumber):
            InputNumber = int(InputNumber)
            #applying my Factorial function to it and storing it in the variable
            FactorialNumber = CalculusSeries.Factorial(InputNumber)
            #Providing a popup to tell user what their answer was
            PoppingUp('Factorial', 'Your requested answer to %d Factorial is: %d' %(InputNumber, FactorialNumber))
        #otherwise a pop up shows that you need to type an integer into the field.     
        else:
            PoppingUp('Error Factorial','Please Type an Integer!')

class CalculusGraphs(Screen):
    #Using my Stack class to instantiate a stack data structure to store the details
    #of the graph and make this stack available to any function within this CalculusGraph Class
    global StoredEquations
    StoredEquations = Stack()
    #function to plot user defined graph
    def openGraph(UserEquation, x_Start, x_End):
        #Store important details of graph in a list
        UserGraphs = [UserEquation, x_Start, x_End]
        #pushes this list to be stored onto the stack
        StoredEquations.push(UserGraphs)
        #Checks if any input fields are empty using error handingling
        try:
            #Utilising List Comprehension techniques to iterate over the ranges
            #and create the list of x values that will be plotted
            x_values = [x for x in range(int(x_Start), int(x_End)+1)]
            #using list comprehension again to produce the y values using the evaluated equation
            #and taking the inputs of the graph equation from an iteration over the x_values
            plt.plot(x_values, [eval(UserEquation) for x in x_values])
            #Bringing the graph forward to be visible to the user
            plt.show()
        #if a field is empty, a ValueError is thrown and this deals with it with a popup
        except ValueError:
            #Uses error pop up window
            PoppingUp('Empty Field', 'Please fill in all the fields before submitting')

    #Takes in GUI user input for creating the graph including equation and domain       
    def AcquireDetails(self):
        #Defining global variable for the equation of the graph as it will be used
        #in the other functions
        global UserEquation
        UserEquation = self.ids.graph_equation.text
        #Takes in starting and end points of the graph
        x_Start = self.ids.equation_x1.text
        x_End = self.ids.equation_x2.text
        #Runs openGraph function to plot and open graph with user input
        CalculusGraphs.openGraph(UserEquation, x_Start, x_End)
        
    #using equation after being inputted through openGraph function to be used again  
    def f(x):
        #returns the evaluated form of the user input to allow numerical manipulations
        return eval(UserEquation)
    
    #Using the differentiation from first principles to calculate the gradient
    #this nullifies the need to import a symbolic derivative calculator script which will
    #be less efficient than my own defined function.
    def FindGradient(self):
        #Takes in the point the user wants to find the gradient for
        GradientPoint = float(self.ids.gradient_point.text)
        #Mathematically known as delta x - small change in x (as dx tends to 0, derivative = gradient)
        dx = 1/10000
        #Change in the y function defined by the difference in the y values of x and 
        #the minute change in x 
        dy = CalculusGraphs.f(GradientPoint+dx) - CalculusGraphs.f(GradientPoint)
        #dy/dx is the Leibniz derivative notation which is well known in mathematics
        #Rounded to 2 decimal places for the user to make easier comparisons
        gradient = round(dy/dx, 2)
        #Outputs the gradient as a window popup
        PoppingUp('Gradient', 'Your requested gradient at the point x=%s is: %s' % (GradientPoint, gradient))

    #Similar to above, this uses Integration from first principles to calculate the area
    #under the graph between two points, and is more efficient than importing someone else's
    #code as this is an important part of the Mathematics A Level that I know
    def FindArea(self):
        #Converting user input into a float to calculate with
        Area_Start = float(self.ids.area_start.text)
        Area_End = float(self.ids.area_end.text)
        #This finds the range and divides by the number of rectangles that I choose to
        #I have chosen 10000 as this gives a very accurate answer to my chosen 2 decimal
        #places but does not slow down the program and make the user wait unnecessarily
        RecWidth = (float(Area_Start)-float(Area_End))/10000
        #Will use this as a cumulative area variable for the 'for loop'
        Area = 0
        #Loops over the number of rectangles
        for i in range(10000):
            #Finds the y values for the tiny changes in width
            RecHeight = CalculusGraphs.f(Area_Start + i * RecWidth)
            #Sums up all the areas of the rectangles under the graph to find total area
            Area += RecWidth * RecHeight
        PoppingUp('Area', 'Your requested Area under the curve between x=%s and x=%s is: %s' % (Area_Start, Area_End, Area))

    #Undo function utilising the stack
    def Undo(self):
        #Checks if the stack is not empty after popping of list of details
        if not StoredEquations.isEmpty():
            #current equation is popped of stack
            StoredEquations.pop()
            #Pops off next list of details and stores it into a string
            UndoneGraph = StoredEquations.pop()
            #Storing the equation seperately so it can be used by the gradient and area functions
            #even after doing an undo
            UserEquation = UndoneGraph[0]
            #Calls openGraph function with order of details as arguments
            CalculusGraphs.openGraph(UserEquation, UndoneGraph[1],UndoneGraph[2])
        #If the stack is found to be empty, then the user cannot undo further
        else:
            #a pop up is used to notify the user 
            PoppingUp('Empty!', 'There are no more equations to Undo!')

'''Revision Class for Trigonometry Revision Section'''
#Defining Screen and functions for trigonometry revision
class Trigonometry(Screen, FloatLayout):
    #Creating function to plot the user defined triangle
    def PlotTriangle(self):
        #Taking in user coordinates to plot their triangle
        Co_One = self.ids.xy_1.text
        Co_Two = self.ids.xy_2.text
        Co_Three = self.ids.xy_3.text
        #Using error handling to prevent user from breaking program when typing incorrectly
        try:
            #Creating numpy array which stores the evaluated coordinates given by the user
            #numpy arrays are more optimised for this task which is why I decided to use it
            Tri = np.array([eval(Co_One), eval(Co_Two), eval(Co_Three)])
            #Creating a new figure which is going to be the triangle
            plt.figure()
            #Plotting triangle as a scatter graph with each point with size 50
            #using python number slicing to allow plot to be cyclic
            #this means the first point will act as starting and ending point to close the shape
            plt.scatter(Tri[:, 0], Tri[:, 1], s = 50, color = 'red')
            #Plotting the triangle and setting internal colour to be blue
            Triangle = plt.Polygon(Tri[:3,:], color='blue')
            plt.gca().add_patch(Triangle)
            #Bringing plot to front for user to see
            plt.show()
        #Prevents the two possible errors that can occur and pops up warning user   
        except NameError or SyntaxError:
            PoppingUp('Co-ordinate Error', 'Please enter the co-ordinates in the correct format')
            
    #Creating function to convert degrees into radians
    def ConvertDegrees(self):
        #Taking user input from text box
        user_degrees = self.ids.angle_degrees.text
        #Using error handling to ensure user inputs a number
        try:
            #converting the input into a float data type to be used in calculations
            user_degrees = float(user_degrees)
            #using the mathematical conversion to change degrees into radians
            convertedD = user_degrees *((math.pi)/180)
            #Outputting the answer as a pop up
            PoppingUp('Converted Radians', '%s degrees converted into radians is: %s' % (user_degrees, convertedD))
        #Checks for the ValueError
        except ValueError:
            #Pop up to notify user to input a number
            PoppingUp('Not Number', 'Please enter a number to be converted to radians!')

    #Creating function to convert radians into degrees
    def ConvertRadians(self):
        #Taking user input from text box
        user_radians = self.ids.angle_radians.text
        #Using error handling code to make sure that the inputs a number
        try:
            #converting the input into a float data type to be used in calculations
            user_radians = float(user_radians)
            #using the inverse mathematical conversion to change radians into degrees
            convertedR = user_radians *(180/(math.pi))
            #Outputting the answer as a pop up
            PoppingUp('Converted Degrees', '%s radians converted into degrees is: %s' % (user_radians, convertedR))
        #Checks for a possible ValueError
        except ValueError:
            #A Pop up is used to notify the user to input a number
            PoppingUp('Not Number', 'Please enter a number to be converted to degrees!')


class StatScreen(Screen, FloatLayout):
    #Creating a new attribute with a string property for this class so
    #there can be live updates to it when the user generates new set
    data_set = StringProperty()
    #using a constructor method with variable keyword arguments
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #setting the data_set variable as an attribute of the objects in this class
        data_set = str()
           
    #Defining function to generate random set of ten numbers to be used in calculations
    def GenerateSet(self):
        #Creates new list
        random_set = []
        #Creates a loop to append 10 random numbers to the list
        for i in range (10):
            random_set.append(random.randint(0,100))
        #Sets the data_set variable as the random_set to update the screen live
        self.data_set = str(random_set)
        
    #Creating a function for the average of a list as this will be useful for
    #the other statistical functions
    def Average(self, numlist):
        total = 0
        #Adding up all the numbers
        for i in range(len(numlist)):
            total += numlist[i]
        #Dividing by the length of the list
        return total/len(numlist)
    
    #Defining function to calculate the variance of the given set of numbers       
    def Variance(self, numlist):
        #Setting average of list using defined function
        average = self.Average(numlist)
        #setting variance to 0
        variance = 0
        #creating a for loop to iterate over the numbers in the list
        for i in range(len(numlist)):
            #Adding a cumulative sum of the difference between each value and the average
            #then squaring that
            variance += (numlist[i] - average)**2
        #the variance is the above calculation divided by the amount of numbers
        return variance/len(numlist)

    #Function for when StatCalc Button is clicked
    def StatCalc(self):
        #assigning the evaluated list of numbers to a variable
        DataList = eval(self.data_set)
        #Calculating the mean of the data set
        mean = self.Average(DataList)
        #Calculating the variance of the data set
        variance = round(self.Variance(DataList), 3)
        #for efficiency, rather than creating a seperate function for the standard deviation
        #I can use the fact that it is the square root of the value of the variance
        #This means the program can be more efficient as there is less redundant code
        deviation = round(math.sqrt(variance), 3)
        #A pop up provides all these statistical calculations for the user
        PoppingUp('Statistic Calculations', "Mean = %s, Standard Deviation = %s, Variance = %s" %(mean, deviation, variance))     

    #Defining Binomial Probability Distribution Function
    def BinomialDistribution(self, trialx, totaltrials, probability):
        #Using error handling to prevent user from making incorrect inputs
        try:
            #checking if probability is between 0 and 1, and that the trials given is below
            #the total trials that are given
            if probability > 0 and probability <=1 and trialx <= totaltrials:
                #Finding the binomial coefficient which uses combinatorics (N choose x)
                #This uses my recursive factorial function to calculate the required values
                BiCo1 = CalculusSeries.Factorial(totaltrials)
                BiCo2 = CalculusSeries.Factorial(trialx)
                BiCo3 = CalculusSeries.Factorial(totaltrials - trialx)
                #Working out the binomial coefficient from its calculated parts
                BiCoefficient = BiCo1/(BiCo2*BiCo3)
                #Calculating the probability of the 'successes' occuring
                p_successes = probability ** trialx
                #Calculating the probability of the remaining trials being 'failures'
                p_failures = (1-probability) ** (totaltrials - trialx)
                #Returning the binomial distribution generated probability
                return BiCoefficient * p_successes * p_failures
            else:
                #Notifying user if their inputs cannot be processed using the distribution
                #as they can not be used within the binomial distribution
                PoppingUp('Numbers', 'Values cannot be processed, check them carefully')
        #Notifying user that they have to check they have inputted the correct values
        except ValueError:
            PoppingUp('Numbers', 'Please check that you have inputted your values correctly')

    #defining function to be used with the GUI and distribution button
    def BinomialInterface(self):
        #Adding Error Handling
        try:
            #assigning the user inputs to variables
            trialx = int(self.ids.binomial_x.text)
            totaltrials = int(self.ids.binomial_N.text)
            probability = float(self.ids.binomial_p.text)
            #Calculating the binomial probability from the distribution function
            BinomialProbability = self.BinomialDistribution(trialx, totaltrials, probability)
            #Displaying the calculated probability to the user
            PoppingUp('Binomial Distribution', 'Your requested probability is: %s' %(BinomialProbability))
        #Notifying user that they have to check they have inputted the correct values
        except ValueError:
            PoppingUp('Numbers', 'Please check that you have inputted your values correctly')
    
        
    #Defining Cumulative Binomial Probability Distribution Function
    def CumulativeBinomial(self):
        #Adding Error Handling
        try:
            #assigning the user inputs to variables
            trialx = int(self.ids.Cbinomial_x.text)
            totaltrials = int(self.ids.Cbinomial_N.text)
            probability = float(self.ids.Cbinomial_p.text)
            #setting cumulative probability to 0
            CumulativeProbability = 0
            #Adding up all probabilities for trials occuring from 0 up to the given number
            for i in range(0, trialx + 1):
                #running the binomial distribution function over all values in range and summing
                CumulativeProbability += self.BinomialDistribution(i, totaltrials, probability)
            #returning the cumulative probability
            PoppingUp('Binomial Cumulative Distribution', 'Your requested probability is: %s' %(CumulativeProbability))
        #Notifying user that they have to check they have inputted the correct values
        except ValueError:
            PoppingUp('Numbers', 'Please check that you have inputted your values correctly')

    #Using the central limit theorem, this will calculate the probability of the
    #generated set containing a given value by the user
    def NormalDistribution(self):
        #assigning the evaluated list of numbers to a variable
        DataList = eval(self.data_set)
        #Calculating the mean of the data set
        mean = self.Average(DataList)
        #Calculating the variance of the data set
        deviation = math.sqrt(self.Variance(DataList))
        #Using error handling to catch any invalid inputs by the user
        try:
            #assigning user input to variable and converting into a float data type
            normalx = float(self.ids.normal_x.text)
            #Calculating the Normal Coefficient (coefficient of the exponential in equation)
            NCoefficient = 1/(deviation*math.sqrt(2*math.pi))
            #Calculating both parts of the exponential's power
            power1 = -1 * (normalx - mean)**2
            power2 = 2*(deviation**2)
            #Calculating final probability from distribution using Euler's number e
            NormalProbability = NCoefficient * ((math.e)**(power1/power2))
            #Outputs the final probability to the user
            PoppingUp('Normal Distribution', 'Your requested probability is: %s' %(NormalProbability))
        #Checks for Value Error and informs user when error is caught
        except ValueError:
            PoppingUp('Numbers', 'Please check that you have inputted your value correctly')

#New class for the Progress Tracking Screen
class ProgressScreen(Screen):
    user_data = StringProperty()
    #using a constructor method with variable keyword arguments
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        user_data = str()

    #Defining function to acquire results across all topics for the user
    def GetAll(Email):
        #connecting to database
        DataConnect('connect')
        #Retrieving required data using SQL queries and specifying the user's email to ensure only their data is shown
        crsr.execute('''SELECT DiffCorrect, DiffTotal, IntCorrect, IntTotal, StatCorrect, StatTotal, TrigCorrect, TrigTotal, AvgDifficulty
                               FROM Progress WHERE Email=?''', (Email,))
        #Stores all data taken from the query in named variables to carry out calculations with
        for row in crsr.fetchall():
            diffCorrect = row[0]
            diffTotal = row[1]
            intCorrect = row[2]
            intTotal = row[3]
            statCorrect = row[4]
            statTotal = row[5]
            trigCorrect = row[6]
            trigTotal = row[7]
            AverageDif = row[8]

        #Calculating percentage correct for each of the topics that the program currently supports
        DiffPercent = int((diffCorrect/diffTotal) * 100)
        IntPercent = int((intCorrect/intTotal) * 100)
        StatPercent = int((statCorrect/statTotal) * 100)
        TrigPercent = int((trigCorrect/trigTotal) * 100)
        #returns all these values to be used in other functions
        return DiffPercent, IntPercent, StatPercent, TrigPercent, AverageDif

    #defining function to output overall data about user
    def All(self):
        #Storing results from GetAll() function in variables to be used
        DiffPercent, IntPercent, StatPercent, TrigPercent, AverageDif = ProgressScreen.GetAll(UserCheck)
        #creating a results list which holds a tuple of all the data calculated to be outputted to the user
        results = [(str(DiffPercent)+'%', str(IntPercent)+'%', str(StatPercent)+'%', str(TrigPercent)+'%', AverageDif)]
        #creating the table headings as a tuple to be used for displaying the data to the user
        resultheadings = ('Differentiation', 'Integration', 'Statistics' , 'Trigonometry', 'Average Difficulty')
        #tabulating the data and updating the user_data text variable so the Progress Screen updates for the user
        self.user_data = tabulate(results, headers = resultheadings, tablefmt = "simple")
        #Disconnecting from the database
        DataConnect('disconnect')

    #Defining function for outputting user's best topic with their percentage for that topic
    def Best(self):
        #Assigning returned values from GetAll function to named variables
        DiffPercent, IntPercent, StatPercent, TrigPercent, AverageDif = ProgressScreen.GetAll(UserCheck)
        #creating a new list to store variables in
        CheckList = [DiffPercent, IntPercent, StatPercent, TrigPercent]
        #Using MAX function to find the user's highest correct percentage topic and then outputs it on the page
        #by updating the text variable
        if max(CheckList) == DiffPercent:
            self.user_data = "Differentiation is your best subject with: " + str(DiffPercent) + "% of answers being correct"
        elif max(CheckList) == IntPercent:
            self.user_data = "Integration is your best subject with: " + str(IntPercent) + "% of answers being correct"
        elif max(CheckList) == StatPercent:
            self.user_data = "Statistics is your best subject with: " + str(StatPercent) + "% of answers being correct"
        else:
            self.user_data = "Trigonometry is your best subject with: " + str(TrigPercent) + "% of answers being correct"

    #This function is similar to the one above and uses the MIN list function instead
    def Worst(self):
        DiffPercent, IntPercent, StatPercent, TrigPercent, AverageDif = ProgressScreen.GetAll(UserCheck)
        CheckList = [DiffPercent, IntPercent, StatPercent, TrigPercent]
        if min(CheckList) == DiffPercent:
            self.user_data = "Differentiation is your worst subject with: " + str(DiffPercent) + "% of answers being correct"
        elif min(CheckList) == IntPercent:
            self.user_data = "Integration is your worst subject with: " + str(IntPercent) + "% of answers being correct"
        elif min(CheckList) == StatPercent:
            self.user_data = "Statistics is your worst subject with: " + str(StatPercent) + "% of answers being correct"
        else:
            self.user_data = "Trigonometry is your worst subject with: " + str(TrigPercent) + "% of answers being correct"

        
    #As specific topic functions are very similar, and as some formatting requirements of SQLITE3,
    #I have placed as much code into a seperate reusuable function as possible to minimise
    #redundancy and improve the efficiency of the program
    def General(Correct, Total):
        #Calculating percentage correct for each of the topics that the program currently supports
        Incorrect = Total - Correct
        Percent = int((Correct/Total) * 100)
        #creating a results list which holds a tuple of all the data calculated to be outputted to the user
        results = [(Correct, Incorrect, Total, str(Percent)+'%')]
        #creating the table headings as a tuple to be used for displaying the data to the user
        resultheadings = ('Total Correct', 'Total Incorrect', 'Total Answered' , 'Success Rate')
        #tabulating the data and storing it in a variable so the Progress Screen can update for the user
        Final = tabulate(results, headers = resultheadings, tablefmt = "simple")
        #Disconnecting from the database
        DataConnect('disconnect')
        #returning the tabulated version of the data
        return Final


    #The next 4 functions use similar techniques to find the user data for a specfic topic
    #display information to the user on the screen.
    def Differentiation(self):
        #connecting to database
        DataConnect('connect')
        #Using query to get the differentiation parts of the progress table
        crsr.execute('''SELECT DiffCorrect, DiffTotal
                    FROM Progress WHERE Email=? ''', (UserCheck,))
        #Stores all data taken from the query in named variables to carry out calculations with
        for row in crsr.fetchall():
            Correct = int(row[0])
            Total = int(row[1])
        #Updates user data text property to display on the screen using my General Function defined above
        self.user_data = ProgressScreen.General(Correct, Total)
        
    
    def Integration(self):
        #connecting to database
        DataConnect('connect')
        #Using query to get the Integration topic information
        crsr.execute('''SELECT IntCorrect, IntTotal
                    FROM Progress WHERE Email=? ''', (UserCheck,))
        #Stores all data taken from the query in named variables to carry out calculations with
        for row in crsr.fetchall():
            Correct = int(row[0])
            Total = int(row[1])
        #Updates user data text property to display on the screen
        self.user_data = ProgressScreen.General(Correct, Total)


    def Trigonometry(self):
        #connecting to database
        DataConnect('connect')
        #Using query to get the Trigonometry data
        crsr.execute('''SELECT TrigCorrect, TrigTotal
                    FROM Progress WHERE Email=? ''', (UserCheck,))
        #Stores all data taken from the query in named variables to carry out calculations with
        for row in crsr.fetchall():
            Correct = int(row[0])
            Total = int(row[1])
        #Updates user data text property to display on the screen
        self.user_data = ProgressScreen.General(Correct, Total)


    def Statistics(self):
        #connecting to database
        DataConnect('connect')
        #Using query to get the Statistics Topic data for that user
        crsr.execute('''SELECT StatCorrect, StatTotal
                    FROM Progress WHERE Email=? ''', (UserCheck,))
        #Stores all data taken from the query in named variables to carry out calculations with
        for row in crsr.fetchall():
            Correct = int(row[0])
            Total = int(row[1])
        #Updates user data text property to display on the screen
        self.user_data = ProgressScreen.General(Correct, Total)


#New class for the Progress Tracking Screen
class TeacherProgressScreen(Screen):
    student_data = StringProperty()
    #using a constructor method with variable keyword arguments
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        student_data = str()


    #Defining function to retrieve and display overall information on the class or a specific student
    def TOverall(self):
        #Takes in input from the student email field
        ProgressEmail = self.ids.student_email.text
        #Connects to the database
        DataConnect('connect')
        #Creating the result headings for the tables that will be generated for the teacher
        resultheadings = ('First Name', 'Last Name', 'Diff Correct' , 'Int Correct', 'Stat Correct', 'Trig Correct')
        #Checks if it is empty and therefore means the teacher wants to see whole class results
        if ProgressEmail == '':
            #Uses an sqlite INNER JOIN to connect the Progress Table with the User Table using the student email foreign key
            #This allows the teacher to see which students have been getting which questions correct which is useful for the student
            results = crsr.execute('''SELECT FirstName, LastName, DiffCorrect, IntCorrect, StatCorrect, TrigCorrect FROM Progress INNER JOIN User
                         ON Progress.Email = User.Email;''')
        #If it is not empty then the teacher has specified a specific student to see the results for
        else:
            #Uses an sqlite INNER JOIN with another constraint using the email provided by the teacher and assigns this result to a variable
            #This means the teacher can view the results for a single specified student
            results = crsr.execute('''SELECT FirstName, LastName, DiffCorrect, IntCorrect, StatCorrect, TrigCorrect FROM Progress INNER JOIN User
                         ON Progress.Email = User.Email AND Progress.Email = ?;''', (ProgressEmail,))

        #setting the on screen text variable to be the tabulated set of results for the student(s)
        self.student_data = tabulate(results, headers = resultheadings, tablefmt = "grid")
        #Disconnecting from the database
        DataConnect('disconnect')
        print(self.student_data)

    #Function to return totals for each topic's answered and correct questions
    #This is placed in a seperate function as both the TBest and TWorst functions will
    #need to use simiar code for retrieving the data and this avoids redundancy and improves efficiency
    def TSummation(self):
        DataConnect('connect')
        ProgressEmail = self.ids.student_email.text
        #Setting up a list of column names to use within my SQLITE Aggregate Functions to calculate total answered questions
        #and correctly answered questions
        Columns = ['DiffTotal', 'IntTotal', 'StatTotal', 'TrigTotal','DiffCorrect', 'IntCorrect', 'StatCorrect', 'TrigCorrect']
        #Creating a list for each of the total answered questions and the total correct questions
        TotalAnswered = []
        TotalCorrect = []
        #If the input field is empty then the teacher wants to view data for entire class
        if ProgressEmail == '':
            #Loops through all 'Total' columns and uses the SQLITE SUM Aggregate function to find the total answered questions
            #for each topic
            for i in range(0,4):
                #Uses string formatting with aggregate functions to create sqlite statement
                crsr.execute('''SELECT SUM(%s) FROM Progress''' % (Columns[i]))
                #Uses list comprehension to get rid of additional tuples created by sqlite cursor object
                #then appends the answer onto the TotalAnswered list
                TotalAnswered.append([row[0] for row in crsr.fetchall()])
            print(TotalAnswered)
            #This is similar to code above but is used to find the total of the 'Correct' Columns for each
            for i in range(4,8):
                #Uses string formatting with aggregate functions to create sqlite statement
                crsr.execute('''SELECT SUM(%s) FROM Progress''' % (Columns[i]))
                #Uses list comprehension to get rid of additional tuples created by sqlite cursor object
                #then appends the answer onto the TotalAnswered list
                TotalCorrect.append([row[0] for row in crsr.fetchall()])
            #Calculates percentages for each overall topic by using the values from the
            #generated two way list from the sqlite queries above
            DiffPercent = (int(TotalCorrect[0][0])/int(TotalAnswered[0][0]))*100
            IntPercent = (int(TotalCorrect[1][0])/int(TotalAnswered[1][0])) * 100
            StatPercent = (int(TotalCorrect[2][0])/int(TotalAnswered[2][0])) * 100
            TrigPercent = (int(TotalCorrect[3][0])/int(TotalAnswered[3][0])) * 100
        else:
            #If a specific student email is given, then the function from the GetAll function from the
            #Student progress screen is used to obtain the percentages again reducing data redundancy
            DiffPercent, IntPercent, StatPercent, TrigPercent, AverageDif = ProgressScreen.GetAll(ProgressEmail)
        #Disconnects from the database
        DataConnect('disconnect')
        #Returns the percentages of success for each topic
        return ProgressEmail, int(DiffPercent), int(IntPercent), int(StatPercent), int(TrigPercent)
        
    #Function for teacher to find the best topic for the entire class or a specified student
    def TBest(self):
        #Takes in the text of the email field and the percentages for all the topics from my TSummation function
        ProgressEmail, DiffPercent, IntPercent, StatPercent, TrigPercent = self.TSummation()
        #Places the percentages in a list
        TPercentages = [DiffPercent, IntPercent, StatPercent, TrigPercent]
        #Finds max number of the list and assigns it to the 'Best' variable
        Best = max(TPercentages)
        #Checks if email input field was empty
        if ProgressEmail == '':
            #Goes through the topics with a message showing which topic was the best for the overall class
            #and gives the percentage
            if Best == DiffPercent:
                self.student_data = "Differentiation is your class' best subject with: " + str(DiffPercent) + "% of answers being correct"
            elif Best == IntPercent:
                self.student_data = "Integration is your class' best subject with: " + str(IntPercent) + "% of answers being correct"
            elif Best == StatPercent:
                self.student_data = "Statistics is your class' best subject with: " + str(StatPercent) + "% of answers being correct"
            else:
                self.student_data = "Trigonometry is your class' best subject with: " + str(TrigPercent) + "% of answers being correct"
        #If an email was given then this is run
        else:
            #Connects to database
            DataConnect('connect')
            #Adds personalisation by finding the first name of the user associated with that given email
            #to be used in the output messages
            crsr.execute('''SELECT FirstName From User WHERE Email =?''', (ProgressEmail,))
            for row in crsr.fetchall():
                #Assigns their first name to the FirstName variable
                FirstName = row[0]
            #Checks which topic was that student's best and provides a message with their name, topic and the percentage of correct questions
            #Message is then outputted on the application Progress Screen for the teacher to view
            if Best == DiffPercent:
                self.student_data = "Differentiation is " + str(FirstName)+ "'s best subject with: " + str(DiffPercent) + "% of answers being correct"
            elif Best == IntPercent:
                self.student_data = "Integration is " + str(FirstName)+ "'s best subject with: " + str(IntPercent) + "% of answers being correct"
            elif Best == StatPercent:
                self.student_data = "Statistics is " + str(FirstName)+ "'s best subject with: " + str(StatPercent) + "% of answers being correct"
            else:
                self.student_data = "Trigonometry is " + str(FirstName)+ "'s best subject with: " + str(TrigPercent) + "% of answers being correct"
            #Disconnects from the database
            DataConnect('disconnect')    
            
        
    #This function is very similar to the one above with some changes to find the worst topic for a class or specific student
    def TWorst(self):
        #Takes in the text of the email field and the percentages for all the topics from my TSummation function
        ProgressEmail, DiffPercent, IntPercent, StatPercent, TrigPercent = self.TSummation()
        #Places the percentages in a list
        TPercentages = [DiffPercent, IntPercent, StatPercent, TrigPercent]
        #Finds max number of the list and assigns it to the 'Best' variable
        Worst = min(TPercentages)
        #Checks if email input field was empty
        if ProgressEmail == '':
            #Goes through the topics with a message showing which topic was the best for the overall class
            #and gives the percentage
            if Worst == DiffPercent:
                self.student_data = "Differentiation is your class' worst subject with: " + str(DiffPercent) + "% of answers being correct"
            elif Worst == IntPercent:
                self.student_data = "Integration is your class' worst subject with: " + str(IntPercent) + "% of answers being correct"
            elif Worst == StatPercent:
                self.student_data = "Statistics is your class' worst subject with: " + str(StatPercent) + "% of answers being correct"
            else:
                self.student_data = "Trigonometry is your class' worst subject with: " + str(TrigPercent) + "% of answers being correct"
        #If an email was given then this is run
        else:
            #Connects to database
            DataConnect('connect')
            #Adds personalisation by finding the first name of the user associated with that given email
            #to be used in the output messages
            crsr.execute('''SELECT FirstName From User WHERE Email =?''', (ProgressEmail,))
            for row in crsr.fetchall():
                #Assigns their first name to the FirstName variable
                FirstName = row[0]
            #Checks which topic was that student's worst and provides a message with their name, topic and the percentage of correct questions
            #Message is then outputted on the application Progress Screen for the teacher to view
            if Worst == DiffPercent:
                self.student_data = "Differentiation is " + str(FirstName)+ "'s worst subject with: " + str(DiffPercent) + "% of answers being correct"
            elif Worst == IntPercent:
                self.student_data = "Integration is " + str(FirstName)+ "'s worst subject with: " + str(IntPercent) + "% of answers being correct"
            elif Worst == StatPercent:
                self.student_data = "Statistics is " + str(FirstName)+ "'s worst subject with: " + str(StatPercent) + "% of answers being correct"
            else:
                self.student_data = "Trigonometry is " + str(FirstName)+ "'s worst subject with: " + str(TrigPercent) + "% of answers being correct"
            #Disconnects from the database
            DataConnect('disconnect')  


    #Creating a general topic results function to retrieve the results from the database and display it 
    def TGeneral(self, ProgressEmail, CorrectName, TotalName):
        #Uses an SQLITE INNER JOIN to combine the results of the User Table and Progress Table which will allow 
        #a teacher to view the entire class' results and the name of the student
        results = crsr.execute('''SELECT FirstName, LastName, %s, %s FROM Progress INNER JOIN User
                        ON Progress.Email = User.Email''' %(CorrectName, TotalName))
        #Creating the result headings
        resultheadings = ['FirstName', 'LastName', 'Total Correct', 'Total Answered']
        #Tabulating the data and updating the screen text variable
        self.student_data = tabulate(results, headers = resultheadings, tablefmt = "grid")
        print(self.student_data)
        #Disconnecting from the database
        DataConnect('disconnect')

    #Topic Functions will display information about the class or a specified student on a single topic
    #The name of the function is the topic it is referring to
    def TDifferentiation(self):
        #Connecting to the database
        DataConnect('connect')
        #Taking in text field input for email and assigining it to ProgressEmail
        ProgressEmail = self.ids.student_email.text
        #If it is empty, then the entire class data is displayed
        if ProgressEmail == '':
            #This uses the TGeneral Function with the parameters being the specific column names for the topic
            self.TGeneral(ProgressEmail, 'DiffCorrect', 'DiffTotal')
        #Otherwise it will only find the results for the specific student email that was inputted
        else:
            #Uses another INNER JOIN to combine the tables and show the data to the teacher with a 
            #condition to find the data that is only associated to the teacher-inputted email
            results = crsr.execute('''SELECT FirstName, LastName, DiffCorrect, DiffTotal FROM
            Progress INNER JOIN User ON Progress.Email = User.Email AND Progress.Email = ?''',(ProgressEmail,))
            #Creates the headings for the reported table
            resultheadings = ['FirstName', 'LastName', 'Differentiation Correct', 'Differentiation Total']
            #Tabulates the data and updates the student_data screen text variable
            self.student_data = tabulate(results, headers = resultheadings, tablefmt = "grid")
            print(self.student_data)
            #Disconnects from the database
            DataConnect('disconnect')
            
    def TIntegration(self):
        #Connecting to the database
        DataConnect('connect')
        #Taking in text field input for email and assigining it to ProgressEmail
        ProgressEmail = self.ids.student_email.text
        #If it is empty, then the entire class data is displayed
        if ProgressEmail == '':
            #This uses the TGeneral Function with the parameters being the specific column names for the topic
            self.TGeneral(ProgressEmail, 'IntCorrect', 'IntTotal')
        #Otherwise it will only find the results for the specific student email that was inputted
        else:
            #Uses another INNER JOIN to combine the tables and show the data to the teacher with a condition to find the data
            #that is only associated to the teacher-inputted email
            results = crsr.execute('''SELECT FirstName, LastName, IntCorrect, IntTotal FROM Progress INNER JOIN User
                        ON Progress.Email = User.Email AND Progress.Email = ?''',(ProgressEmail,))
            #Creates the headings for the reported table
            resultheadings = ['FirstName', 'LastName', 'Integration Correct', 'Integration Total']
            #Tabulates the data and updates the student_data screen text variable
            self.student_data = tabulate(results, headers = resultheadings, tablefmt = "grid")
            print(self.student_data)
            #Disconnects from the database
            DataConnect('disconnect')

    def TStatistics(self):
        #Connecting to the database
        DataConnect('connect')
        #Taking in text field input for email and assigining it to ProgressEmail
        ProgressEmail = self.ids.student_email.text
        #If it is empty, then the entire class data is displayed
        if ProgressEmail == '':
            #This uses the TGeneral Function with the parameters being the specific column names for the topic
            self.TGeneral(ProgressEmail, 'StatCorrect', 'StatTotal')
        #Otherwise it will only find the results for the specific student email that was inputted
        else:
            #Uses another INNER JOIN to combine the tables and show the data to the teacher with a condition to find the data
            #that is only associated to the teacher-inputted email
            results = crsr.execute('''SELECT FirstName, LastName, StatCorrect, StatTotal FROM Progress INNER JOIN User
                        ON Progress.Email = User.Email AND Progress.Email = ?''',(ProgressEmail,))
            #Creates the headings for the reported table
            resultheadings = ['FirstName', 'LastName', 'Statistics Correct', 'Statistics Total']
            #Tabulates the data and updates the student_data screen text variable
            self.student_data = tabulate(results, headers = resultheadings, tablefmt = "grid")
            #Disconnects from the database
            DataConnect('disconnect')

    def TTrigonometry(self):
        #Connecting to the database
        DataConnect('connect')
        #Taking in text field input for email and assigining it to ProgressEmail
        ProgressEmail = self.ids.student_email.text
        #If it is empty, then the entire class data is displayed
        if ProgressEmail == '':
            #This uses the TGeneral Function with the parameters being the specific column names for the topic
            self.TGeneral(ProgressEmail, 'TrigCorrect', 'TrigTotal')
        #Otherwise it will only find the results for the specific student email that was inputted
        else:
            #Uses another INNER JOIN to combine the tables and show the data to the teacher with a condition to find the data
            #that is only associated to the teacher-inputted email
            results = crsr.execute('''SELECT FirstName, LastName, TrigCorrect, TrigTotal FROM Progress INNER JOIN User
                        ON Progress.Email = User.Email AND Progress.Email = ?''',(ProgressEmail,))
            #Creates the headings for the reported table
            resultheadings = ['FirstName', 'LastName', 'Trigonometry Correct', 'Trigonometry Total']
            #Tabulates the data and updates the student_data screen text variable
            self.student_data = tabulate(results, headers = resultheadings, tablefmt = "grid")
            #Disconnects from the database
            DataConnect('disconnect')


#New class for the Timetable functions and screen
class TimetableScreen(Screen):
    timetable = StringProperty()
    #using a constructor method with variable keyword arguments
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        timetable = str()

#New class for the Timetable functions and screen
class CreateTimetableScreen(Screen):
    timetable = StringProperty()
    #using a constructor method with variable keyword arguments
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        timetable = str()

    #Function to clear the contents of the Text Input fields when user presses the button
    #to add a timetable entry so they can enter another one quickly
    def ClearTable(self):
        #This just goes through and sets the text for each field as an empty string
        self.ids.day_number.text = ''
        self.ids.period_one.text = ''
        self.ids.period_two.text = ''
        self.ids.period_three.text = ''
        self.ids.period_four.text = ''
        self.ids.period_five.text = ''
        self.ids.period_six.text = ''
        
    #Function to take in user's input of timetable and store it in the database to
    #be used with the schedule system
    def AddTimetable(self):
        #Uses exception handling to prevent the program from being stopped if user
        #enters incorrect values
        try:
            #Takes in all inputs from the time table creation screen and stores it in
            #respective variables
            day_number = int(self.ids.day_number.text)
            period_one = self.ids.period_one.text
            period_two = self.ids.period_two.text
            period_three = self.ids.period_three.text
            period_four = self.ids.period_four.text
            period_five = self.ids.period_five.text
            period_six = self.ids.period_six.text
            #Connecting to the database
            DataConnect('connect')
            #Using SQL Aggregate function to find a new ID and increment it when
            #new timetable entry is added
            NewTimeID = IncrementID('''Select MAX(TimeID) FROM TimeTable''')
            #Inserting all the new timetable data into the TimeTable table in the database
            crsr.execute('''INSERT INTO TimeTable(TimeID, DayNumber, Period_1, Period_2, Period_3, Period_4, Period_5, Period_6, Email)
            VALUES(?,?,?,?,?,?,?,?,?)''', (NewTimeID, day_number, period_one, period_two, period_three, period_four, period_five, period_six, UserCheck))
            #Disconnecting from database
            DataConnect('disconnect')
        #If missing or incorrect values are found then a PopUp is used to inform the user
        except ValueError:
            PoppingUp("Missing Values", "Please fill in all of the fields before pressing 'Add Timetable'!")
        #Clears table after rest of function has run
        self.ClearTable()
    
#New class for screen to view user's timetable
class ViewTimetableScreen(Screen):
    #Creating a new timetable variable with a string property
    timetable = StringProperty()
    #using a constructor method with variable keyword arguments
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #using the timetable variable as an attribute of the class' objects
        timetable = str()

    #Defining view timetable function to allow the user to see their stored timetable
    #This will run when the View Timetable button is pressed from the Timetable Screen
    def ViewTimetable(self):
        #Connecting to database
        DataConnect('connect')
        #Querying data from database and storing it in a variable to be ready for output
        UserTimetable = crsr.execute('''SELECT DayNumber, Period_1, Period_2, Period_3, Period_4, Period_5,
                                    Period_6 FROM TimeTable WHERE Email = ?''', (UserCheck,))
        #Creating the headings for the displayed table on screen
        TimeHeadings = ['Day Number', 'Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5', 'Period 6']
        #Tabulates the data and updates the timetable variable on screen
        self.timetable = tabulate(UserTimetable, headers = TimeHeadings, tablefmt = "grid")
        #Disconnecting from database
        DataConnect('disconnect')

#Creating Schedule Screen to be midpoint to get to both
#Creating the meeting and viewing the meeting screens
#code for this is in the kv file as it is only GUI elements
class ScheduleScreen(Screen):
    pass

#Screen Class for all methods associated with creating a one-to-one meeting 
class CreateMeetingScreen(Screen):
    #defining my constructor method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    #Function to get values from text fields
    def GetValues(self):
        #Assigning text field inputs to variables to be processed
        PreferredDay = int(self.ids.preferred_day_number.text)
        Reason = self.ids.reason.text
        teacher_email= self.ids.teacher_email.text
        student_email = UserCheck
        #returns all the values 
        return PreferredDay, Reason, teacher_email, student_email

    #Creating a function which will check if there is already a scheduled
    #day in the Possible Options then removes it to prevent clashes
    def RectifyClash(self, Possible):
        #Connecting to database
        DataConnect('connect')
        #retrieving the day and period of already scheduled meetings
        #from database
        crsr.execute('''SELECT ScheduleDay, SchedulePeriod
        FROM Scheduled''')
        #storing results of query in variable
        Schedules = crsr.fetchall()
        #creating a new list to store any clashes 
        deleted = []
        #Compares possible free periods with already
        #scheduled times to ensure there are no clashes
        for i in range(len(Possible)):
            if Possible[i] in Schedules:
                #if a clash is found, the tuple with the schedule
                #information is added to a delete list
                deleted.append(Possible[i])
                
        #Two seperate loops are used as if one loop was used then the 'for loop'
        #condition would change whilst the loop is running (as the list size decreases)
        #and therefore len of the list will be out of the index range;
        #using two loops prevents this error from happening

        #This then iterates through the delete list
        for i in range(len(deleted)):
            #it then removes all clashes from the Possible list
            Possible.remove(deleted[i])
        #Disconnects from the database
        DataConnect('disconnect')
        #returns the correct Possible list of meetings
        return Possible

    #Creating a new function which finds the date of the scheduled meeting
    #making it easier for the user to know when they need to be at the meeting
    def ScheduleDate(Day):
        #Works out the date at the current time
        Today = date.today()
        #'Day' variable is the targeted day for when the meeting will occur
        #DayDifference calculates the difference in days between the current day
        #and the targeted day modulo 7 to ensure the number is positive 
        DayDifference = (Day - Today.weekday()) %7
        #The function returns the new date by using a timedelta method, adding on
        #the correct number of days to today's date and then formatting it to the
        #well known day, month, year format.
        return (Today + datetime.timedelta(DayDifference)).strftime("%d/%m/%Y")


    #Schedule Meeting method, all functionality in this is seperate from the CreateMeeting Screen
    #objects or fields (shown by the general parameters) so that it may be used again in other
    #screens or functions outside this class
    def ScheduleMeeting(self, PreferredDay, Reason, T_Email, S_Email):
        #Connecting to the database
        DataConnect('connect')
        #storing timetable of the teacher
        crsr.execute('''SELECT DayNumber, Period_1, Period_2, Period_3, Period_4, Period_5,
        Period_6 FROM TimeTable WHERE Email =?''', (T_Email,))
        teacher_timetable = crsr.fetchall()
        #storing timetable of the student
        crsr.execute('''SELECT DayNumber, Period_1, Period_2, Period_3, Period_4, Period_5,
        Period_6 FROM TimeTable WHERE Email =?''', (S_Email,))
        student_timetable = crsr.fetchall()

        #Creates a new list to store the available combinations of days and periods
        #when the student is free to have a meeting
        Available = []

        #Preferred day code is run first to place it at the front of the list
        #Iterates for the length of the timetable of the student on one day
        for i in range(len(student_timetable[PreferredDay-1])):
            #As it is a tuple stored within a list, the referencing of a particular field is done
            #using a similar method to matricies with the 'row' and 'column'
            #This checks if any of the lessons are FREE
            if student_timetable[PreferredDay-1][i] == 'FREE':
                #If it is free then it is added on to the list of available meeting days
                Available.append((PreferredDay, i))
  
        #Iterates for the length of the timetable of the student on each day
        #to prevent it from unnecessarily iterating over the 'PreferredDay' Day,
        #I have used list comprehension with a condition to remove it from the range
        for j in [x for x in range(len(student_timetable)) if x != PreferredDay]:
            #Once in a specific day, it loops over the periods in that day by checking length of the list
            for k in range(len(student_timetable[j])):
                #This checks if any of the lessons are FREE using the method from above
                if student_timetable[j][k] == 'FREE':
                    #If it is free then it is added on to the list of available meeting days as a tuple
                    Available.append((j, k))

        #The Possible list stores the possible meeting days and periods where both the student and the teacher
        #are free
        Possible = []
        #This iterates for how many available day-period combinations the student is available for
        for i in range(len(Available)):
            #Checks if the teacher is free on the day and period that the student is free
            if teacher_timetable[Available[i][0]][Available[i][1]] == 'FREE':
                #If the student and teacher are both free then a tuple is appended to the Possible List
                Possible.append((Available[i][0]+1,Available[i][1]))

        #After the possible meeting times have been generated and appended to the list,
        #The rectify clash functions checks and fixes any possible clashes
        Possible = CreateMeetingScreen.RectifyClash(self, Possible)
        
        #Checks if no times were found to have the one-to-one meeting
        if Possible == []:
            #A pop up is used to inform the user that a meeting could not be placed
            PoppingUp("None Found", "An attempt was made to find a meeting time, however there were none available!")
        else:
            #Setting the schedule days and periods from the first available time in the Possible list (which has a preference for preferred day)
            ScheduledDay = Possible[0][0]
            ScheduledPeriod = Possible[0][1]+1
            #Creating a new ID for the Scheduled table for the new meeting using an SQL aggregate function
            ScheduleID = IncrementID('''Select MAX(ScheduleID) FROM Scheduled''')
            #Inserting the new information for the schedule into the database
            crsr.execute('''INSERT INTO Scheduled(ScheduleID, ScheduleDay, SchedulePeriod, Reason, Email)
            VALUES(?,?,?,?,?)''', (ScheduleID, ScheduledDay, ScheduledPeriod, Reason, S_Email))
            #Finds the date of the meeting using the ScheduleDate function
            NewDate = CreateMeetingScreen.ScheduleDate(ScheduledDay-1)
            #After completion, user is informed when their meeting is set with the full date and the Period
            PoppingUp('Success', ("Your meeting has been set up for: "+ str(NewDate) + " at Period " + str(ScheduledPeriod)))
            #Sending email to teacher and student when meeting has been set up
            CreateMeetingScreen.MeetingEmails(T_Email, S_Email, NewDate, ScheduledPeriod, Reason)
        #Disconnecting from the database
        DataConnect('disconnect')
                
    #This function is for the GUI button to take in the user inputted values
    #and call the ScheduleMeeting function
    def RequestMeeting(self):
        #Variables assigned to the return values from the GetValues() method
        PreferredDay, Reason, teacher_email, student_email = self.GetValues()
        #ScheduleMeeting function is called
        self.ScheduleMeeting(PreferredDay, Reason, teacher_email, student_email)

    #Creating a function to get the user's first name to personalise the emails
    def GetName(self, Email):
        #Creating a new variable to store the name in
        Name = ''
        #connecting to database
        DataConnect('connect')
        #Selecting name from database for the email given 
        crsr.execute('SELECT FirstName FROM User WHERE Email=?''', (Email,))
        #converts list of tuples into a single variable that can be used easily
        for row in crsr.fetchall():
            #assigns the first name to the Name variable
            Name = row[0]
        #Returns the first name of user
        return Name

    #Creating function to produce and send emails to the student and teacher
    #after a meeting has been scheduled
    def MeetingEmails(self, T_Email, S_Email, Date, ScheduledPeriod, Reason):
        #Assigning Username and Password for the maths gmail account that was
        #created for this project
        SenderAccount = 'mathematicsnea@gmail.com'
        #Password for this account (redacted for security reasons)
        SenderPassword = 'Mathematics1!'

        #Making a connection to the SMTP gmail server using port 587
        EmailServer = smtplib.SMTP('smtp.gmail.com', 587)
        #Sending an 'Extended Hello' command to the server to initiate SMTP Conversation
        EmailServer.ehlo()
        #Using the Start TLS protocol command to upgrade security with a secure connection
        #using either TLS or SSL
        EmailServer.starttls()
        #Sends the login command with the username and password to the server to attempt logging in
        EmailServer.login(SenderAccount, SenderPassword)
        #assigning a general variable with the email subject for both teacher and student being
        #a new scheduled meeting
        EmailSubject = 'New Scheduled Meeting'

        #using the GetName function to assign the first name of the student to a variable
        StudentName = CreateMeetingScreen.GetName(S_Email)
        #Creating a personalised email message for the student
        StudentMessage = ('''Dear %s,
                    \nYou have a scheduled one-to-one meeting with your maths teacher on the %s at Period %s.
                    \nThe reason given for this meeting is: %s
                    \nPlease ensure you attend this meeting.
                    \nKind Regards,
                    \nLuqman's Mathematics Application''' % (StudentName, Date, ScheduledPeriod, Reason))
        #Creating a body to fill in and join the fields for To, From and the Subject of an email
        #along with the message itself and assigning to a variable to be used in the sendmail function 
        StudentBody = '\r\n'.join(['To: %s' % S_Email,'From: %s' % SenderAccount, 'Subject: %s' % EmailSubject,
                            '', StudentMessage])

        #Similar code for the maths teacher which personalises it to them
        #using the GetName function to assign the first name of the teacher to a variable
        TeacherName = CreateMeetingScreen.GetName(T_Email)
        #Creating a personalised email message for the teacher
        TeacherMessage = ('''Dear %s,
                    \nYou have a scheduled one-to-one meeting with your student (%s) on the %s at Period %s.
                    \nThe reason given for this meeting is: %s
                    \nKind Regards,
                    \nLuqman's Mathematics Application''' % (TeacherName, StudentName, Date, ScheduledPeriod, Reason))
        #Creating the body to fill in all fields and the message
        TeacherBody = '\r\n'.join(['To: %s' % T_Email,'From: %s' % SenderAccount, 'Subject: %s' % EmailSubject,
                            '', TeacherMessage])

        #Uses exception handling to send emails in case there is an error to prevent the program
        #from stopping
        try:
            #Sends an email to both the teacher and the student
            EmailServer.sendmail(SenderAccount, [S_Email], StudentBody)
            EmailServer.sendmail(SenderAccount, [T_Email], TeacherBody)
        #If email fails to send then a message pops up to inform the user
        except:
            PoppingUp('Email Error', '''An attempt was made to send an email but it has failed.
                     Please keep note of your meeting date and time''')
        #exits and closes the connection to the server after emails are sent
        EmailServer.quit()
        
        
#New screen and Class for viewing the upcoming meetings for that particular user
#and option to cancel an upcoming meeting (only meetings for that user are shown)
class ViewMeetingScreen(Screen):
    #Creating a new scheduler variable with a string property
    user_schedule = StringProperty()
    #using a constructor method with variable keyword arguments
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #using the user_schedule variable as an attribute of the class' objects
        user_schedule = str()

    #Function to view upcoming meetings
    def ViewMeeting(self):
        #Connecting to database
        DataConnect('connect')
        #Uses as an sqlite query to obtain the required information
        #from the Scheduled table in the database
        crsr.execute('''SELECT ScheduleID, ScheduleDay, SchedulePeriod, Reason
                    FROM Scheduled WHERE Email =?''', (UserCheck,))
        #Assigns the result from the sql query to a variable
        Meetings = crsr.fetchall()
        #Goes through all meetings and attaches a date using the
        #ScheduleDate function I created
        #Iterates through the Meetings list of queried data
        for i in range(len(Meetings)):
            #Calculates the date by working out the day the meeting is set out for
            #and then finding the next available date using the ScheduleDate function
            AddDate = CreateMeetingScreen.ScheduleDate(Meetings[i][1]-1)
            #Concatenates the original tuple of data for one meeting with
            #a tuple that stores the date for the meeting and replaces
            #the original tuple(as the returned query data is in tuples which are immutable)
            Meetings[i] = Meetings[i] + (AddDate,)

        #Creating headers for the tabulated meeting table to display to user
        MeetingHeaders = ["Schedule ID", "Meeting Day", "Meeting Period", "Reason", "Date"]
        #tabulating data and updating on screen text variable to show to user
        self.user_schedule = tabulate(Meetings, headers = MeetingHeaders, tablefmt = "grid")
        #Disconnecting from database
        DataConnect('disconnect')

        print(self.user_schedule)


        
    #Function for user to cancel a meeting specified by the ID
    def CancelMeeting(self):
        DataConnect('connect')
        #Takes in user input from field
        ScheduleID = self.ids.meeting_id.text
        #Uses error handling to check if user input is valid
        try:
            #Runs query to delete the entry in the table matching the id given by user
            #and ensures that they can only delete their own meetings by checking if the
            #Email as well
            crsr.execute('''DELETE FROM Scheduled WHERE ScheduleID =? AND Email=?''', ((ScheduleID,), (UserCheck,)))
            #Pop up message telling user their meeting has been deleted
            PoppingUp('Success', "Your meeting has been deleted")
            #Commiting query and disconnecting from database 
            DataConnect('disconnect')
            #Runs the View Meetings again to refresh the page and show the remaining meetings
            self.ViewMeeting()
        #If the ID given by the user does not exist or the entry they try to delete is not
        #associated with their email then an sqlite3 operational error occurs
        #this code catches that error 
        except sqlite3.OperationalError:
            #Informs user of the error when trying to delete the meeting
            PoppingUp('Error', "That ID does not exist or is not associated with your Account!")
            
    
#Creating a manager class which will handle the different screens
#of the application's GUI
class Manager(ScreenManager):
    login_screen = ObjectProperty(None)
    home_screen = ObjectProperty(None)
    register_screen = ObjectProperty(None)
    feature_screen = ObjectProperty(None)
    invader_screen = ObjectProperty(None)
    progress_screen = ObjectProperty(None)
    calculus_screen = ObjectProperty(None)
    calc1_screen = ObjectProperty(None)
    calc2_screen = ObjectProperty(None)
    topictest_screen = ObjectProperty(None)
   
   
#This defines the overall application gui class
class Mathematics(App):
   #the builder method will return manager class as that handles the screens
   def build(self):
       return Manager()
        
#Program runs if it is not imported from other files.
if __name__ == "__main__":
    Mathematics().run()
