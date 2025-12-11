from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
    if data.empty:
        data = pandas.read_csv("data/french_words.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
to_learn = data.to_dict(orient="records")
flip_timer = None

def next_card():
    global current_card
    global flip_timer
    if flip_timer is not None:
        window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card, image=front_card)
    canvas.image = front_card
    french_word = current_card["French"]
    canvas.itemconfig(title_text, text="French")
    canvas.itemconfig(title_text, fill = "black")
    canvas.itemconfig(content_text, fill="black")
    canvas.itemconfig(content_text, text=french_word)
    flip_timer = window.after(3000, change_to_back)

def change_to_back():
    back_image = PhotoImage(file="images/card_back.png")
    canvas.itemconfig(card, image=back_image)
    canvas.image = back_image
    canvas.itemconfig(title_text, text="English")
    canvas.itemconfig(title_text, fill = "white")
    canvas.itemconfig(content_text, fill="white")
    canvas.itemconfig(content_text, text = current_card["English"])

def tick_click():
    to_learn.remove(current_card)
    file_data = pandas.DataFrame(to_learn)
    file_data.to_csv("data/words_to_learn.csv", index=False)

    next_card()

window = Tk()
window.title("flashcard project")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(height=526, width=800, highlightthickness=0, bg=BACKGROUND_COLOR)
front_card = PhotoImage(file="images/card_front.png")
card = canvas.create_image(400, 263, image=front_card)
canvas.grid(column=0, row=0, columnspan=2)

title_text = canvas.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
content_text = canvas.create_text(400, 263, text="French", font=("Arial", 60, "bold"))

tick_image = PhotoImage(file="images/right.png")
tick_button = Button(image=tick_image,command=tick_click)
tick_button.grid(column=0, row=1)

cross_image = PhotoImage(file="images/wrong.png")
cross_button = Button(image=cross_image, command=next_card)
cross_button.grid(column=1, row=1)

next_card()

window.mainloop()