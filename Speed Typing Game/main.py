from tkinter import *
import json
from random import randint

window = Tk()
window.title("Type Racer")
window.geometry('750x900')
window.config(padx=20, pady=20, bg="#000000")

file = open("word_list.json")
word_list= json.load(file)


def start_typing():
    random = randint(0, len(word_list)-1)
    next_word.config(text=word_list[random])

    timer.config(text=0)
    time()


def done_typing(key):
    # space -> done typing detected
    if key.char == " ":
        # check typing
        if (next_word["text"]) == (user_input.get().strip()):
            new_score = str(int(score_count["text"]) + 1)
            speed = round(int(new_score)/(int(timer["text"])/60))
            score_count.config(text=new_score)
            score_speed.config(text=speed)
            feedback.config(text="Correct!", fg="green")
        else:
            feedback.config(text="Wrong", fg="red")
        # get next word
        random = randint(0, len(word_list) - 1)
        next_word.config(text=word_list[random])

        # clear input
        user_input.delete(0,END)


def time():
    seconds = str(int(timer["text"]) + 1)
    timer.config(text=seconds)
    timer.after(1000, time)


# Head
canvas = Canvas(window, width=700, height=125, bg='#000000')
canvas.grid(row=0, column=0, columnspan=2)
img = PhotoImage(file="head.png")
head_img = canvas.create_image(0, 0, anchor='nw', image=img, )

# Button
start = Button(height=1, width=15, pady=20, text="Start Typing", font=('Arial', 12), command=start_typing)
start.grid(row=1, column=0)

# Label
timer = Label(window, text="", pady=40, bg="#000", font=('Arial', 25), fg="#FFFFFF")
timer.grid(row=1, column=1)

next_word = Label(window, text="test", pady=40, bg="#000", font=('Arial', 25), fg="#FFFFFF")
next_word.grid(row=2, column=0, columnspan=2)

# User Input
user_input = Entry(window, font=('Arial', 40), bg="#000", fg="#F2994A", highlightthickness=4, highlightbackground="#F2994A", justify='center')
user_input.grid(row=3, column=0, columnspan=2)

user_input.bind("<Key>", done_typing)

# Score
score_count = Label(window, text="0", pady=90, bg="#000", font=('Arial', 20), fg="#FFFFFF")
score_count.grid(row=5, column=0)

score_speed = Label(window, text="0/min", pady=90, bg="#000", font=('Arial', 20), fg="#FFFFFF")
score_speed.grid(row=5, column=1)

# Feedback
feedback = Label(window, text="", pady=40, bg="#000", font=('Arial', 25), fg="#FFFFFF")
feedback.grid(row=6, column=0, columnspan=2)


window.mainloop()
