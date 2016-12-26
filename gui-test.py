import tkinter as tk
import numpy as np
import crocodile as cc


def cardify(num):
    i = str(num)
    if num == 13:
        i = 'K'
    elif num == 12:
        i = 'Q'
    elif num == 11:
        i = 'J'
    elif num == 1:
        i = 'A'
    return i


class Incrementer:
    def __init__(self, i, list, label):
        self.i = i
        self.list = list
        self.label = label

    def __call__(self):
        self.list[self.i] += 1
        if self.list[self.i] > 4:
            self.list[self.i] = 0
        self.label['text'] = self.list[self.i]
        return self.list


class App:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("crocodile")
        self.root.geometry("600x600")

        frame = tk.Frame(self.root)
        frame.grid()

        self.quitbutton = tk.Button(frame, text='quit', command=frame.quit)
        self.quitbutton.grid(row=16, column=0)

        self.sethandbutton = tk.Button(frame, text='set hand', command=self.set_hand)
        self.sethandbutton.grid(row=16, column=1)
        self.handlabel = tk.Label(frame, text='')
        self.handlabel.grid(row=16, column=2)

        self.resethandbutton = tk.Button(frame, text='reset hand', command=self.reset_hand)
        self.resethandbutton.grid(row=17, column=1)

        self.scorebutton = tk.Button(frame, text='score hand', command=self.score_hand)
        self.scorebutton.grid(row=18, column=1)
        self.scorelabel = tk.Label(frame, text='')
        self.scorelabel.grid(row=18, column=2)

        self.numeachcard = []
        self.incrementers = []
        self.cardbuttons = []
        self.cardlabels = []

        for i in np.arange(0, 13):
            self.numeachcard.append(0)

            label = tk.Label(frame, text=str(self.numeachcard[i]))
            self.cardlabels.append(label)
            self.cardlabels[i].grid(row=i, column=2)

            self.incrementers.append(Incrementer(i, self.numeachcard, self.cardlabels[i]))

            item = tk.Button(frame, text=cardify(i+1), command=self.incrementers[i])
            self.cardbuttons.append(item)
            self.cardbuttons[i].grid(row=i, column=1)

        self.hand = None

    def set_hand(self):
        self.hand = []
        for idx, numcard in enumerate(self.numeachcard):
            for n in [idx+1] * numcard:
                self.hand.append(n)
        self.handlabel['text'] = self.hand

    def reset_hand(self):
        for i in np.arange(0,13):
            self.numeachcard[i] = 0
            self.cardlabels[i]['text'] = self.numeachcard[i]
        self.hand = []
        self.handlabel['text'] = self.hand

    def score_hand(self):
        cc.score_hand(self.hand, True)

app = App()
app.root.mainloop()
app.root.destroy()
