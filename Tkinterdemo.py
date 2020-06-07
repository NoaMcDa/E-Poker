import tkinter

from PIL import ImageTk, Image


def cutCard(location, CardDeck):
    x, y = location
    left = x
    right = x + 100
    top = y
    bottom = y + 130

    card = CardDeck.crop((left, top, right, bottom))
    card = ImageTk.PhotoImage(card)

    return card

window = tkinter.Tk()
Backg = Image.open(r"C:\Users\noada\PycharmProjects\Poker\Game Poker\Background.jpg")
Background= ImageTk.PhotoImage(Backg)
BgroundCanvas = tkinter.Canvas(window,width = 1000,height = 600)
BgroundCanvas.place(x = 0, y = 0)
BgroundCanvas.create_image(0,0,anchor = "nw" ,image=Background)

CardDeck = Image.open(r"C:\Users\noada\PycharmProjects\Poker\Game Poker\Carddeck.jpg")


window.title("GUI")
loc = (300, 390)
card1 = cutCard(loc, CardDeck)
loc = (500, 260)
card2 = cutCard(loc, CardDeck)
print(type(card1))
print(type(CardDeck))
# pack is used to show the object in the window
canvas1 = tkinter.Canvas(window,width = 100,height = 130)
canvas1.place(x = 395, y = 400)
canvas1.create_image(0,0,anchor = "nw" ,image=card1)
canvas2 = tkinter.Canvas(window,width = 100,height = 130)
canvas2.place(x = 505, y = 400)
canvas2.create_image(0,0,anchor = "nw" ,image=card2)
window.geometry("1000x600")
window.mainloop()
