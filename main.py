from tkinter import *
import pandas
import random
import sys

BACKGROUND_COLOR = "#B1DDC6"

root = Tk()
root.title("Flashy")
root.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

def choose_language(chosen_language):
    global language

    language = chosen_language

    load_language()

def load_language():
    global to_learn, pair_of_words, language, flip_timer

    for button in [french_button, italian_button, russian_button]:
        button.destroy()

    for button in [check_button, cross_button]:
        button.config(state=NORMAL)

    try:
        data = pandas.read_csv(f"data/{language}_words_to_learn.csv")
    except FileNotFoundError:
        data = pandas.read_csv(f"data/{language}_words.csv")
    except pandas.errors.EmptyDataError:
        print("No words to learn.")
        sys.exit()

    to_learn = data.to_dict(orient="records")
    pair_of_words = {}

    flip_timer = root.after(3000, rotate_card)
    next_card()

def next_card():
    global flip_timer, pair_of_words, language

    if len(to_learn) == 0:
        canvas.itemconfig(word, text="You've learned all the words!", fill="black", font=("Arial", 30, "bold"))
        root.after_cancel(flip_timer)
        return

    root.after_cancel(flip_timer)

    pair_of_words = random.choice(to_learn)

    canvas.itemconfig(card_image, image=card_front_image)
    canvas.itemconfig(language_text, text=language.title(), fill="black")
    canvas.itemconfig(word, text=pair_of_words[language.title()], fill="black")

    flip_timer = root.after(3000, rotate_card)

def rotate_card():
    canvas.itemconfig(card_image, image=card_back_image)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word, text=pair_of_words["English"], fill="white")

def remove_card():
    global to_learn, pair_of_words

    to_learn.remove(pair_of_words)

    to_learn_df = pandas.DataFrame(to_learn)
    to_learn_df.to_csv(f"data/{language}_words_to_learn.csv", index=False)

    next_card()

canvas = Canvas()

card_back_image = PhotoImage(file="images/card_back.png")
card_front_image = PhotoImage(file="images/card_front.png")

french_button = Button(text="French", bg="white", font=("Arial", 30, "bold"), command=lambda: choose_language("french"))
canvas.create_window(400, 150, window=french_button)

italian_button = Button(text="Italian", bg="white", font=("Arial", 30, "bold"), command=lambda: choose_language("italian"))
canvas.create_window(400, 263, window=italian_button)

russian_button = Button(text="Russian", bg="white", font=("Arial", 30, "bold"), command=lambda: choose_language("russian"))
canvas.create_window(400, 376, window=russian_button)

card_image = canvas.create_image(400, 263, image=card_front_image)
language_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))

canvas.config(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=1, column=1, columnspan=2)

check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, bg=BACKGROUND_COLOR, highlightthickness=0, command=remove_card)
check_button.config(state=DISABLED)
check_button.grid(row=2, column=2, pady=(10, 0))

cross_image = PhotoImage(file="./images/wrong.png")
cross_button = Button(image=cross_image, bg=BACKGROUND_COLOR, highlightthickness=0, command=lambda:next_card())
cross_button.config(state=DISABLED)
cross_button.grid(row=2, column=1, pady=(10, 0))

root.mainloop()