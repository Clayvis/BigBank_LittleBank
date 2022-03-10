#!/usr/bin/env python3

# importing third party libraries
import requests
import io
from tkinter import messagebox, ttk
from tkinter import *
from PIL import Image, ImageTk
from playsound import playsound

# declare the tkinter module
main = Tk()

# sending a get request and saving the response as response object
r = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")

# extracting json response and converting it into a dictionary called data

data = r.json()

def play():
    playsound('./assests/cardDeal.mp3')

def special_card_handler(x):

    # special_values = {"JACK":11, "QUEEN":12, "KING":13,"ACE":14}
    # returns the value of special card if there is one or else it returns the original card

        if x == "JACK":
            return "11"
        elif x == "QUEEN":
            return "12"
        elif x == "KING":
            return "13"
        elif x == "ACE":
            return "14"
        else:
            return x

def winner_update(message):
    # takes the winner's message and displays it in the label
    winner_label = Label(main, text=message)
    winner_label.grid(column=1,row=2,ipadx=10, ipady=10 )

def game_logic(playerCard, compCard):
    # Send the parameters to check for special cards 
    a = special_card_handler(playerCard)
    b = special_card_handler(compCard)

    # compares value of cards to determine the winner -> sends the message to winner_update function
    if int(a) == int(b):
        winner_update("    It's a Tie   ")
    elif int(a) > int(b):
        winner_update("Player Wins")
    elif int(b) > int(a):
        winner_update("Computer Wins")

def hit():
    # API requires the deck ID to keep using the same deck -> grabbed the deck ID from data
    deck_id = data["deck_id"]
    # API call to retreive two playing cards
    getTwoCards = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=2')
    # extracting json response and converting it into a dictionary called twoCardsData
    twoCardsData = getTwoCards.json()
    # Drilling down into the object and grabbing the image URLs
    cardImage = twoCardsData['cards'][0]["image"]
    computerCardImage = twoCardsData['cards'][1]["image"]
    # Drilling down into object and grabbing the Card values
    cardValue = twoCardsData['cards'][0]["value"]
    compCardValue = twoCardsData['cards'][1]["value"]
    # API call to get the card image from card image URL
    response = requests.get(cardImage)
    responseTwo = requests.get(computerCardImage)
    # using IO and streming in the PNG file and setting it as a varable
    image_bytes = io.BytesIO(response.content)
    img = ImageTk.PhotoImage(Image.open(image_bytes))
    # using IO and streming in the PNG file and setting it as a varable
    compImage_bytes = io.BytesIO(responseTwo.content)
    compImg = ImageTk.PhotoImage(Image.open(compImage_bytes))

    #placing the players card image on the UI
    player_label = Label(main, image=img)
    player_label.image = img
    player_label.grid(column=0,row=1 )
    #placing the computers card image on the UI
    comp_label = Label(main, image=compImg)
    comp_label.image = compImg
    comp_label.grid(column=2,row=1 )
    play()
    game_logic(cardValue,compCardValue)
   
# Set up the screen for player
main.title("Big Bank Takes Little Bank")
main.geometry("800x600")
main.configure(bg="green")

# create a menubar
menubar = Menu(main)
main.config(menu=menubar)

# create a menu
file_menu = Menu(menubar)

# add a menu item to the menu

file_menu.add_command(
    label='Start Over',

    # ADD START OVER METHOD
)
file_menu.add_command(
    label='Exit',
    command=main.destroy
)

# add the File menu to the menubar
menubar.add_cascade(
    label="File",
    menu=file_menu
)

main.columnconfigure(0, weight=2)
main.columnconfigure(1, weight=2)
main.columnconfigure(2, weight=2)
main.rowconfigure(0, weight=2)
main.rowconfigure(1, weight=2)
main.rowconfigure(2, weight=2)


# player button and css
player_hit_btn = ttk.Button(
    main,
    text='Hit',
    command=hit
)
player_hit_btn.pack(
    ipadx=5,
    ipady=5,
    expand=True
)
player_hit_btn.grid(column=0, row=2)

# labels and css
PlayerText_label = Label(main, text='Player',bg='green',font='14' )
PlayerText_label.grid(column=0,row=0,ipadx=10, ipady=10)

ComputerText_label = Label(main, text='Computer',bg='green', font='14')
ComputerText_label.grid(column=2,row=0,ipadx=10, ipady=10)

messagebox.showinfo("Game Rules", "Click on hit to draw two cards, Player who has the higher card wins......\nBig bank takes little bank, Have fun !!!")



# the function that starts the gui
main.mainloop()  
