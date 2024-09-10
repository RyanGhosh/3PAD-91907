from tkinter import *
import json
import re  # Import regular expressions module
from random import randint, choice
import tkinter as tk




# Global variables for timer and difficulty
timer = None
difficulty = None
time_remaining = None
user_data_file = "user_data.json"




# Function to load user data from JSON file
def load_user_data():
    try:
        with open(user_data_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}




# Function to save user data to JSON file
def save_user_data(data):
    with open(user_data_file, 'w') as file:
        json.dump(data, file, indent=4)




# Function to handle the transition from login to welcome page
def show_welcome_page():
    login_frame.pack_forget()
    welcome_frame.pack(fill='both', expand=True)




# Function to handle the transition from welcome page to difficulty selection
def show_difficulty_selection():
    welcome_frame.pack_forget()
    difficulty_frame.pack(fill='both', expand=True)




def go_back():
    global scoreLabel, resultLabel, questionLabel, changeModeButton
    game_frame.pack_forget()
    difficulty_frame.pack(fill='both', expand=True)
    score.set(0)
    questionNumber.set(0)




    if scoreLabel:
        scoreLabel.destroy()
    if resultLabel:
        resultLabel.destroy()
    if questionLabel:
        questionLabel.destroy()
    if changeModeButton:
        changeModeButton.destroy()




    answerEntry.config(state=NORMAL)
    clear()




    submitButton.config(state=NORMAL)
    bind_enter_key(validate_login)  # Bind Enter key to login function




# Function to handle the transition from difficulty selection to game
def start_game(selected_difficulty):
    global difficulty, scoreLabel, resultLabel, questionLabel, changeModeButton
    difficulty = selected_difficulty
    difficulty_frame.pack_forget()
    game_frame.pack(fill='both', expand=True)




    # Ensure all labels are initialized
    scoreLabel = None
    resultLabel = None
    questionLabel = None
    changeModeButton = None




    generateQuestion()
    update_timer()
    bind_enter_key(checkAnswer)  # Bind Enter key to checkAnswer function




# Function to generate a new question
def generateQuestion():
    global questionLabel




    questionNumber.set(questionNumber.get() + 1)




    # Set range based on difficulty
    if difficulty == "Easy":
        range_min, range_max = 1, 10
    else:
        range_min, range_max = 10, 15




    number1 = randint(range_min, range_max)
    number2 = randint(range_min, range_max)




    operator = choice(['+', '-', '*', '/'])




    # Ensure division results in whole numbers only
    if operator == '/':
        number1 = number1 * number2  # Ensure number1 is divisible by number2




    if operator == '-':
        if number1 < number2:
            number1, number2 = number2, number1  # Swap number1 and number2




    question.set(f"{number1} {operator} {number2}")
    answer.set(int(eval(question.get())))




    if questionLabel:
        questionLabel.destroy()




    questionLabel = Label(game_frame, text=f"Question : {question.get()}", font=('arial', 20))
    questionLabel.grid(row=2, column=0)




    start_timer()




# Function to check the answer provided by the user
def checkAnswer():
    global scoreLabel, timer, changeModeButton




    if timer:
        root.after_cancel(timer)




    if questionNumber.get() > 10:
        return




    global resultLabel




    if resultLabel:
        resultLabel.destroy()




    # Get user input
    user_input = givenAnswer.get()




    # Check if input is empty or invalid
    if user_input == "":
        resultLabel = Label(game_frame, text="Please enter a valid number", font=('arial', 20), fg="red")
        resultLabel.grid(row=4, column=0)
        user_answer = None
    else:
        try:
            user_answer = int(user_input)
        except ValueError:
            resultLabel = Label(game_frame, text="Please enter a valid number", font=('arial', 20), fg="red")
            resultLabel.grid(row=4, column=0)
            clear()
            return




    # Check the answer if provided
    if user_answer is not None:
        if str(answer.get()) == str(user_answer):
            score.set(score.get() + 1)
            resultLabel = Label(game_frame, text="Correct", font=('arial', 20), fg="green")
            resultLabel.grid(row=4, column=0)
        else:
            resultLabel = Label(game_frame, text="Incorrect", font=('arial', 20), fg="red")
            resultLabel.grid(row=4, column=0)




    # Update the score label after each question
    if scoreLabel:
        scoreLabel.destroy()
    scoreLabel = Label(game_frame, text=f"Score : {score.get()}", font=('arial', 20), fg="black")
    scoreLabel.grid(row=5, column=0)




    # Check if it was the last question
    if questionNumber.get() == 10:
        changeModeButton = Button(game_frame, text="Change Mode", fg="blue", font=('arial', 15), width=35, command=go_back)
        changeModeButton.grid(row=8, column=0)
        answerEntry.config(state=DISABLED)  # Disable the entry field
        submitButton.config(state=DISABLED)  # Disable the submit button
        unbind_enter_key()  # Unbind the Enter key
    else:
        generateQuestion()
        clear()




# Function to start the timer based on difficulty level
def start_timer():
    global timer, time_remaining




    if difficulty == "Easy":
        time_remaining = 5  # 5 seconds
    else:
        time_remaining = 10  # 10 seconds


# Function to update the timer display
def update_timer():
    global timer, time_remaining


    if time_remaining > 0:
        time_remaining -= 1
        timerLabel.config(text=f"Time remaining: {time_remaining} seconds")
    else:
        checkAnswer()


    root.after(1000, update_timer)


# Function to restart the game
def restart():
    global scoreLabel, timerLabel, changeModeButton
    if scoreLabel:
        scoreLabel.destroy()
    timerLabel.config(text="")




    score.set(0)
    questionNumber.set(0)
    generateQuestion()




    scoreLabel = Label(game_frame, text=f"Score : {score.get()}", font=('arial', 20), fg="black")
    scoreLabel.grid(row=5, column=0)




    answerEntry.config(state=NORMAL)  # Re-enable the entry field
    submitButton.config(state=NORMAL)  # Re-enable the submit button
    clear()
    bind_enter_key(checkAnswer)  # Bind Enter key to checkAnswer function




    if changeModeButton:
        changeModeButton.destroy()




# Function to clear the answer entry field
def clear():
    answerEntry.delete(0, END)




# Function to validate the username
def validate_username(username):
    return re.match("^[A-Za-z0-9]+$", username) is not None




# Function to validate the password
def validate_password(password):
    return (
        re.search("[A-Z]", password) is not None and  # At least one uppercase letter
        re.search("[a-z]", password) is not None and  # At least one lowercase letter
        re.search("[0-9]", password) is not None and  # At least one digit
        re.search("[@#$%^&+=!]", password) is not None and  # At least one special character
        len(password) >= 8  # Minimum length of 8 characters
    )




# Function to validate login credentials
def validate_login():
    username = usernameEntry.get()
    password = passwordEntry.get()




    user_data = load_user_data()




    if validate_username(username) and validate_password(password):
        if username in user_data and user_data[username] == password:
            show_welcome_page()
        else:
            login_error_label.config(text="Invalid username or password. Please try again.", fg="red")
    else:
        login_error_label.config(text="Invalid login details. Please try again.", fg="red")
        passwordEntry.delete(0, END)




# Function to create a new account
def create_account():
    username = usernameEntry.get()
    password = passwordEntry.get()




    user_data = load_user_data()




    if username in user_data:
        login_error_label.config(text="Username already exists. Please choose another.", fg="red")
        passwordEntry.delete(0, END)
    elif not validate_username(username):
        login_error_label.config(text="Username must contain only letters and numbers.", fg="red")
    elif not validate_password(password):
        login_error_label.config(text="Password must contain at least one capital letter, number, and symbol.", fg="red")
    else:
        user_data[username] = password
        save_user_data(user_data)
        login_error_label.config(text="Account created successfully! You can now login.", fg="green")




# Function to bind Enter key to a function
def bind_enter_key(func):
    root.bind("<Return>", lambda event: func())




# Function to unbind the Enter key
def unbind_enter_key():
    root.unbind("<Return>")




# Create the main application window
root = Tk()
root.geometry("600x500")
root.title("Maths Game")




# Variables to hold the game data
question = StringVar()
answer = StringVar()
givenAnswer = StringVar()
score = IntVar()
questionNumber = IntVar()




# Create the login frame
login_frame = Frame(root)
login_frame.pack(fill='both', expand=True)
login_frame.configure(bg = "#028090")



login_label = Label(login_frame, text="Login to Maths Game", font=("Arial", 18), bg = "#028090")
login_label.pack(pady=50)




username_label = Label(login_frame, text="Username:", font=("Arial", 12), bg = "#028090" )
username_label.pack(pady=5)
usernameEntry = Entry(login_frame, font=("Arial", 12))
usernameEntry.pack(pady=5)




password_label = Label(login_frame, text="Password:", font=("Arial", 12), bg = "#028090")
password_label.pack(pady=5)
passwordEntry = Entry(login_frame, show='*', font=("Arial", 12))
passwordEntry.pack(pady=5)




login_error_label = Label(login_frame, text="", font=("Arial", 10), bg = "#028090")
login_error_label.pack(pady=5)




login_button = Button(login_frame, text="Login", command=validate_login, font=("Arial", 14), bg = "#114B5F")
login_button.pack(pady=10)




create_account_button = Button(login_frame, text="Create Account", command=create_account, font=("Arial", 14), bg = "#114B5F")
create_account_button.pack(pady=10)




# Create the welcome frame
welcome_frame = Frame(root)
welcome_frame.configure(bg = "#028090")


welcome_label = Label(welcome_frame, text="Welcome to the Maths Game", font=("Arial", 18), bg = ("#028090"))
welcome_label.pack(pady=50)




description_label = Label(welcome_frame, text="Test your math skills with 10 questions!", font=("Arial", 12), bg = ("#028090"))
description_label.pack(pady=10)




start_button = Button(welcome_frame, text="Start Game", command=show_difficulty_selection, font=("Arial", 14), bg = "#114B5F")
start_button.pack(pady=20)




# Create the difficulty selection frame
difficulty_frame = Frame(root)
difficulty_frame.configure(bg = "#028090")



difficulty_label = Label(difficulty_frame, text="Select Difficulty", font=("Arial", 18), bg = ("#028090"))
difficulty_label.pack(pady=50)




easy_button = Button(difficulty_frame, text="Easy", command=lambda: start_game("Easy"), font=("Arial", 14), bg = "#114B5F")
easy_button.pack(pady=10)




hard_button = Button(difficulty_frame, text="Hard", command=lambda: start_game("Hard"), font=("Arial", 14), bg = "#114B5F")
hard_button.pack(pady=10)




# Create the game frame
game_frame = Frame(root)
game_frame.configure(bg = "#028090")



headingLabel = Label(game_frame, text="Maths Game", font=('arial', 25), bg = ("#028090"))
headingLabel.grid(row=0, column=0)




questionLabel = Label(game_frame, text=question.get(), font=('arial', 20), bg = ("#028090"))
questionLabel.grid(row=2, column=0)




answerEntry = Entry(game_frame, textvariable=givenAnswer, font=('arial', 20), width=25)
answerEntry.grid(row=3, column=0)




submitButton = Button(game_frame, text="Submit", fg="yellow", font=('arial', 15), command=checkAnswer, bg = "#114B5F")
submitButton.grid(row=3, column=1)




resultLabel = Label(game_frame, text="Result", font=('arial', 20), fg="blue", bg = ("#028090"))
resultLabel.grid(row=4, column=0)




scoreLabel = Label(game_frame, text=f"Score : {score.get()}", font=('arial', 20), fg="black", bg = ("#028090"))
scoreLabel.grid(row=5, column=0)




restartButton = Button(game_frame, text="Restart", fg="red", font=('arial', 15), width=35, command=restart, bg = "#114B5F")
restartButton.grid(row=6, column=0)




timerLabel = Label(game_frame, text="", font=('arial', 20), fg="black", bg = ("#028090"))
timerLabel.grid(row=7, column=0)




# Bind the Return key to login function initially
bind_enter_key(validate_login)
 
# Run the Tkinter event loop
root.mainloop()











