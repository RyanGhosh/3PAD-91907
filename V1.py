from tkinter import *
from random import randint,choice

root = Tk()
root.geometry("600x500")
root.title("Maths Quiz")

question = StringVar()
answer = StringVar()
givenAnswer = StringVar()
score = IntVar()
questionNumber = IntVar()

def generateQuestion():

    global questionLabel

    questionNumber.set(questionNumber.get() + 1)

    number1 = randint(1 , 10)
    number2 = randint(1 , 10)

    operator = choice(['+' , '-' , '*' , '/'])

    question.set(str(number1) + operator + str(number2))
    answer.set(eval(question.get()))

    if questionLabel:
        questionLabel.destroy()

    questionLabel = Label(root , text=f"Question : {question.get()}" , font=('arial' , 20))
    questionLabel.grid(row=2 , column=0)

def checkAnswer():

    global scoreLabel

    if questionNumber.get() > 10 :
        return

    global resultLabel

    if resultLabel:
        resultLabel.destroy()

    if str(answer.get()) == givenAnswer.get():
        score.set(score.get() + 1)
        resultLabel = Label(root , text="Correct" , font=('arial' , 20), fg="green")
        resultLabel.grid(row=4 , column=0)
        scoreLabel = Label(root , text=f"Score : {score.get()}" , font=('arial' , 20) , fg="black")
        scoreLabel.grid(row=5 , column=0)

    else:
        resultLabel = Label(root , text="Incorrect" , font=('arial' , 20) , fg="red")
        resultLabel.grid(row=4 , column=0)


    if questionNumber.get() == 10:
        scoreLabel.destroy()
        scoreLabel = Label(root , text=f"Final Score : {score.get()}" , font=('arial' , 20) , fg="black")
        scoreLabel.grid(row=5 , column=0)
    
    else:
        generateQuestion()
        
def restart():

    global scoreLabel
    scoreLabel.destroy()

    score.set(0)
    questionNumber.set(0)
    generateQuestion()

    scoreLabel = Label(root , text=f"Score : {score.get()}" , font=('arial' , 20) , fg="black")
    scoreLabel.grid(row=5 , column=0)
# User Interface



headingLabel = Label(root , text="Maths Quiz" , font=('arial' , 25) )
headingLabel.grid(row=0 , column=0)

questionScale = Scale(root , from_=0 , to=10 , orient=HORIZONTAL , length=400, variable=questionNumber)
questionScale.grid(row=1 , column=0)

completeQuestionLabel = Label(root , text="10th question")
completeQuestionLabel.grid(row=1 , column=1)

questionLabel = Label(root , text=question.get() , font=('arial' , 20))
questionLabel.grid(row=2 , column=0)

answerEntry = Entry(root , textvariable=givenAnswer ,  font=('arial' , 20), width=25)
answerEntry.grid(row=3 , column=0)

submitButton = Button(root , text="Submit" , fg="yellow", bg="grey", font=('arial' , 15) , command=checkAnswer)
submitButton.grid(row=3 , column=1)

resultLabel = Label(root , text="Result" , font=('arial' , 20) , fg="blue")
resultLabel.grid(row=4 , column=0)

scoreLabel = Label(root , text=f"Score : {score.get()}" , font=('arial' , 20) , fg="black")
scoreLabel.grid(row=5 , column=0)

submitButton = Button(root , text="Restart" , fg="red", font=('arial' , 15), width=35 , command=restart)
submitButton.grid(row=6 , column=0)

generateQuestion()

root.mainloop()