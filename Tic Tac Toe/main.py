import random
from tkinter import *
from tkinter import messagebox

window = Tk()
window.title("TicTacToe!")
window.config(padx=20, pady=20, bg="#F4F4F4")

def check_board():
    # Check rows, columns
    all_board = ""
    for i in range(3):
        strike_row = ""
        strike_column = ""
        for j in range(3):
            strike_row += b[i][j]["text"]
            strike_column += b[j][i]["text"]
            all_board += b[i][j]["text"]
        if (strike_row == "XXX") or (strike_column == "XXX"):
            return "X"
        elif (strike_row == "OOO") or (strike_column == "OOO"):
            return "O"
    # Check diagonals
    if b[0][0]["text"] == b[1][1]["text"] == b[2][2]["text"] == "X":
        return "X"
    elif b[0][0]["text"] == b[1][1]["text"] == b[2][2]["text"] == "O":
        return "O"
    elif b[2][0]["text"] == b[1][1]["text"] == b[0][2]["text"] == "X":
        return "X"
    elif b[2][0]["text"] == b[1][1]["text"] == b[0][2]["text"] == "O":
        return "O"
    # Check tie
    elif len(all_board) == 9:
        return "tie"
    else:
        return ""


def update_score(winner):
    if winner == "X":
        new_score = int(X_score.get()) + 1
        print(new_score)
        X_score.delete(0, END)
        X_score.insert(0, str(new_score))
        clear_board(winner)
    elif winner == "O":
        new_score = int(O_score.get()) + 1
        O_score.delete(0, END)
        O_score.insert(0, str(new_score))
        clear_board(winner)
    # Tie
    else:
        clear_board(winner)

def clear_board(winner):
    messagebox.showinfo("Game Over", f"Winner is: {winner}")
    for i in range(3):
        for j in range(3):
            b[i][j] = Button(height=2, width=5, font=("Helvetica", "48"), text="",
                             command=lambda r=i, c=j: clicked(r, c))
            b[i][j].grid(row=i + 2, column=j)
    if winner != "tie":
        turn["text"] = winner
    else:
        turn["text"] = random.choice(["X", "O"])


def clicked(r,c):
    if b[r][c]["text"] == "":
        if turn["text"] == "X":
            b[r][c].configure(text='X')
            turn['text'] = "O"
        elif turn["text"] == "O":
            b[r][c].configure(text='O')
            turn['text'] = "X"
    winner = check_board()
    if winner != "":
        update_score(winner)



# Labels
title = Label(text="Turn")
title.grid(row=0, column=1, columnspan=1)
X_score_label = Label(text="X score:")
X_score_label.grid(row=0, column=0, columnspan=1)
O_score_label = Label(text="O score:")
O_score_label.grid(row=0, column=2, columnspan=1)
turn = Label(text="X",font=("Helvetica", "40"))
turn.grid(row=1, column=1, columnspan=1)

# Indicators
X_score = Entry(width=20)
X_score.grid(row=1, column=0, columnspan=1)
X_score.insert(0, "0")
O_score = Entry(width=20)
O_score.grid(row=1, column=2, columnspan=1)
O_score.insert(0, "0")

# Buttons
b = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
    ]

for i in range(3):
    for j in range(3):
        b[i][j] = Button(height=2, width=5, font=("Helvetica", "48"), text="", command = lambda r=i, c=j : clicked(r,c))
        b[i][j].grid(row=i+2, column=j)


window.mainloop()
