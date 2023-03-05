import pandas
from playsound import playsound
import csv
from csv import DictWriter


BACKGROUND_COLOR = "#B1DDC6"
import random
from tkinter import *
import pandas as pd
to_learn = {}
current_card = {}
to_spoof = {}
a_spoof = {}
b_spoof = {}

try: # try running this line of code
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    # If for the first time we are running it
    # the words_to_learn.csv file might not be present
    # and FileNotFoundError might pop up
    original_data = pandas.read_csv("chinese_words.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
    to_spoof = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
    to_spoof = data.to_dict(orient="records")
# data = pd.read_csv("./data/words_to_learn.csv")
# word_dict = {row.Chinese:row.English for (index, row) in df.iterrows()}
# spits out a list of dictionaries containing chinese word and english translation
# print(word_dict)


#------------------------ Generating a Chinese word ----------

def next_card():
    global current_card, a_spoof, b_spoof, flip_timer, pos, study
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    a_spoof = random.choice(to_spoof)
    b_spoof = random.choice(to_spoof)
    # chinese_word = random_pair['Chinese']
    canvas.itemconfig(card_title, text="Chinese", fill="black")
    canvas.itemconfig(card_word, text=current_card["Chinese"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    #flip_timer = window.after(5000, func=mid_card)
    sticky=[E, W, S]
    pos=(''.join(random.sample(sticky,len(sticky))))
    answer_button = Button(text=current_card["Pinyin"], command=mid_card, height = 2, width = 10)
    answer_button.grid(row=1, column=0, sticky=pos[0])
    fake_a_button = Button(text=a_spoof["Pinyin"], command=wrong_pinyin_card, height = 2, width = 10)
    fake_a_button.grid(row=1, column=0, sticky=pos[1])
    fake_b_button = Button(text=b_spoof["Pinyin"], command=wrong_pinyin_card, height = 2, width = 10)
    fake_b_button.grid(row=1, column=0, sticky=pos[2])
    
def wrong_pinyin_card():
    canvas.itemconfig(card_title, text = "Wrong", fill = "white")
    canvas.itemconfig(card_word, text=current_card["Pinyin"], fill = "white")
    canvas.itemconfig(card_background, image=card_back_img)
    #flip_timer = window.after(5000, func=mid_card)
    #next_card()

def mid_card():
    global current_card, flip_timer, a_spooflink, known_button
    window.after_cancel(flip_timer)
    link=current_card["Pinyin"]
    print(link)
    playsound(str(link)+".mp3")
    canvas.itemconfig(card_title, text="Pinyin", fill="black")
    canvas.itemconfig(card_word, text=current_card["Pinyin"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    #flip_timer = window.after(5000, func=flip_card)
    sticky=[E, W, S]
    pos=(''.join(random.sample(sticky,len(sticky))))
    answer_button = Button(text=current_card["English"], command=next_card, height = 2, width = 10)
    answer_button.grid(row=1, column=0, sticky=pos[0])
    fake_a_button = Button(text=a_spoof["English"], command=wrong_english_card, height = 2, width = 10)
    fake_a_button.grid(row=1, column=0, sticky=pos[1])
    fake_b_button = Button(text=b_spoof["English"], command=wrong_english_card, height = 2, width = 10)
    fake_b_button.grid(row=1, column=0, sticky=pos[2])
    tracker()

def tracker():
    headersCSV = ['ID', 'Pinyin', 'English', 'Chinese', 'Wrong_Pinyin', 'Wrong_English']
    dict = {'Pinyin':current_card["Pinyin"], 'English':current_card["English"], 'Chinese':current_card["Chinese"]}                 

    with open('tracker.csv', 'a', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
        dictwriter_object.writerow(dict)
        #myfile = csv.writer(file)
        #myfile.writerow(flipped)
        f_object.close()
        
def wrong_english_card():
    canvas.itemconfig(card_title, text = "Wrong", fill = "white")
    canvas.itemconfig(card_word, text=current_card["English"], fill = "white")
    canvas.itemconfig(card_background, image=card_back_img)
    #flip_timer = window.after(5000, func=mid_card)
    #next_card()
    english_wrong()

def english_wrong():
    header = ['Pinyin','English','Chinese', 'Wrong_Pinyin', 'Wrong_English', 'Wrong_Chinese']
    dict = {'Wrong_English':current_card["English"]}
    with open('tracker.csv', 'a', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=header)
        dictwriter_object.writerow(dict)
        #myfile = csv.writer(file)
        #myfile.writerow(flipped)
        f_object.close()

def flip_card():
    canvas.itemconfig(card_title, text = "English", fill = "white")
    canvas.itemconfig(card_word, text=current_card["English"], fill = "white")
    canvas.itemconfig(card_background, image=card_back_img)

def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    # index = false discrads the index numbers
    flip_timer = window.after(5000, func=mid_card)
    next_card()
#------------------------ FlashCard UI Setup -------------------------------

window = Tk()
window.title("Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(5000, func=flip_card) # 5000 milliseocnds = 5 seconds

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="./card_front.png")
card_back_img = PhotoImage(file="./card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
# Positions are related to canvas so 400 will be halfway in width
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"), tags="word")
# canvas should go in the middle
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="./wrong.png")
unknown_button = Button(image=cross_image, command = next_card)
unknown_button.grid(row=3, column=0, sticky="W")

check_image = PhotoImage(file="./right.png")
known_button = Button(image=check_image, command=is_known)
known_button.grid(row=3, column=1, sticky="E")

next_card()
window.mainloop()

