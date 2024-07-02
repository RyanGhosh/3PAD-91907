from tkinter import *
from random import randint, choice

# Function to handle the transition from welcome page to game
def start_game():
    welcome_frame.pack_forget()
    game_frame.pack()

# Function to generate a new question
def generateQuestion():
    global questionLabel

    questionNumber.set(questionNumber.get() + 1)

    number1 = randint(1, 10)
    number2 = randint(1, 10)

    operator = choice(['+', '-', '*', '/'])

    # Ensure division results in whole numbers only
    if operator == '/':
        number1 = number1 * number2  # Ensure number1 is divisible by number2

    if operator == '-':
        if number1 < number2:
            number1, number2 = number2, number1 #Swaps number 1 and 2

    question.set(f"{number1} {operator} {number2}")
    answer.set(int(eval(question.get())))

    if questionLabel:
        questionLabel.destroy()

    questionLabel = Label(game_frame, text=f"Question : {question.get()}", font=('arial', 20))
    questionLabel.grid(row=2, column=0)

# Function to check the answer provided by the user
def checkAnswer():
    global scoreLabel

    if questionNumber.get() > 10:
        return

    global resultLabel

    if resultLabel:
        resultLabel.destroy()

    if str(answer.get()) == givenAnswer.get():
        score.set(score.get() + 1)
        resultLabel = Label(game_frame, text="Correct", font=('arial', 20), fg="green")
        resultLabel.grid(row=4, column=0)
        scoreLabel = Label(game_frame, text=f"Score : {score.get()}", font=('arial', 20), fg="black")
        scoreLabel.grid(row=5, column=0)
    else:
        resultLabel = Label(game_frame, text="Incorrect", font=('arial', 20), fg="red")
        resultLabel.grid(row=4, column=0)

    if questionNumber.get() == 10:
        scoreLabel.destroy()
        scoreLabel = Label(game_frame, text=f"Final Score : {score.get()}", font=('arial', 20), fg="black")
        scoreLabel.grid(row=5, column=0)
    else:
        generateQuestion()
        clear()

# Function to restart the game
def restart():
    global scoreLabel
    scoreLabel.destroy()

    score.set(0)
    questionNumber.set(0)
    generateQuestion()

    scoreLabel = Label(game_frame, text=f"Score : {score.get()}", font=('arial', 20), fg="black")
    scoreLabel.grid(row=5, column=0)

# Function to clear the answer entry field
def clear():
    answerEntry.delete(0, END)

# Create the main application window
root = Tk()
root.geometry("600x500")
root.title("Maths game")

# Variables to hold the game data
question = StringVar()
answer = StringVar()
givenAnswer = StringVar()
score = IntVar()
questionNumber = IntVar()

# Create the welcome frame
welcome_frame = Frame(root)
welcome_frame.pack(fill='both', expand=True)

welcome_label = Label(welcome_frame, text="Welcome to the Maths Game", font=("Helvetica", 18))
welcome_label.pack(pady=50)

description_label = Label(welcome_frame, text="Test your math skills with 10 questions!", font=("Helvetica", 12))
description_label.pack(pady=10)

start_button = Button(welcome_frame, text="Start Game", command=start_game, font=("Helvetica", 14))
start_button.pack(pady=20)

# Create the game frame
game_frame = Frame(root)

headingLabel = Label(game_frame, text="Maths game", font=('arial', 25))
headingLabel.grid(row=0, column=0)

completeQuestionLabel = Label(game_frame, text="10th question")
completeQuestionLabel.grid(row=1, column=1)

questionLabel = Label(game_frame, text=question.get(), font=('arial', 20))
questionLabel.grid(row=2, column=0)

answerEntry = Entry(game_frame, textvariable=givenAnswer, font=('arial', 20), width=25)
answerEntry.grid(row=3, column=0)

submitButton = Button(game_frame, text="Submit", fg="yellow", bg="grey", font=('arial', 15), command=checkAnswer)
submitButton.grid(row=3, column=1)

resultLabel = Label(game_frame, text="Result", font=('arial', 20), fg="blue")
resultLabel.grid(row=4, column=0)

scoreLabel = Label(game_frame, text=f"Score : {score.get()}", font=('arial', 20), fg="black")
scoreLabel.grid(row=5, column=0)

restartButton = Button(game_frame, text="Restart", fg="red", font=('arial', 15), width=35, command=restart)
restartButton.grid(row=6, column=0)

# Bind the Return key to checkAnswer function
root.bind("<Return>", lambda x: checkAnswer())

# Initialize the first question
generateQuestion()

# Run the Tkinter event loop
root.mainloop()
