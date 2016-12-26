import tkinter as tk
import numpy as np
import copy as copy
import crocodile as cc


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


class Decrementer:
    def __init__(self, i, list, label):
        self.i = i
        self.list = list
        self.label = label

    def __call__(self):
        self.list[self.i] -= 1
        if self.list[self.i] < 0:
            self.list[self.i] = 0
        self.label['text'] = self.list[self.i]
        return self.list


class App:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("crocodile")
        self.root.geometry("1920x1080")

        frame = tk.Frame(self.root)
        frame.grid()

        self.quitbutton = tk.Button(frame, text='quit', command=frame.quit)
        self.quitbutton.grid(row=0, column=0)

        self.sethandbutton = tk.Button(frame, text='score hand', command=self.set_hand)
        self.sethandbutton.grid(row=16, column=1)
        self.handlabel = tk.Label(frame, text='')
        self.handlabel.grid(row=16, column=2)

        self.resethandbutton = tk.Button(frame, text='reset hand', command=self.reset_hand)
        self.resethandbutton.grid(row=17, column=1)

        self.scoredesclabel = tk.Label(frame, text='', justify=tk.LEFT)
        self.scoredesclabel.grid(row=19, column=4, sticky=tk.W)

        self.cribbutton = tk.Button(frame, text='test crib', command=self.test_crib)
        self.cribbutton.grid(row=18, column=1)
        self.clearcribbutton = tk.Button(frame, text='clear test crib', command=self.clear_test_crib)
        self.clearcribbutton.grid(row=18, column=3)
        self.cribdesclabel = tk.Label(frame, text='', justify=tk.LEFT)
        self.cribdesclabel.grid(row=18, column=4, sticky=tk.W)
        self.ncribtext = tk.Entry(frame)
        self.ncribtext.grid(row=18, column=2)

        self.starterlabel = tk.Label(frame, text='starter', justify=tk.LEFT)
        self.starterlabel.grid(row=15, column=3, sticky=tk.W)
        self.startertext = tk.Entry(frame)
        self.startertext.grid(row=16, column=3, sticky=tk.W)

        self.numeachcard = []
        self.incrementers = []
        self.decrementers = []
        self.cardbuttonsplus = []
        self.cardbuttonsminus = []
        self.cardlabels = []
        self.cardnames = []

        for i in np.arange(0, 13):
            self.numeachcard.append(0)

            label = tk.Label(frame, text=str(self.numeachcard[i]), justify=tk.LEFT)
            self.cardlabels.append(label)
            self.cardlabels[i].grid(row=i, column=4, sticky=tk.W)

            self.incrementers.append(Incrementer(i, self.numeachcard, self.cardlabels[i]))
            self.decrementers.append(Decrementer(i, self.numeachcard, self.cardlabels[i]))

            label = tk.Label(frame, text=str(cc.cardify(i+1)))
            self.cardnames.append(label)
            self.cardnames[i].grid(row=i, column=2)

            item = tk.Button(frame, text='+', command=self.incrementers[i])
            self.cardbuttonsplus.append(item)
            self.cardbuttonsplus[i].grid(row=i, column=1)

            item = tk.Button(frame, text='-', command=self.decrementers[i])
            self.cardbuttonsminus.append(item)
            self.cardbuttonsminus[i].grid(row=i, column=3, sticky=tk.W)

        self.hand = None

    def set_hand(self):
        self.hand = []
        for idx, numcard in enumerate(self.numeachcard):
            for n in [idx+1] * numcard:
                self.hand.append(n)
        self.handlabel['text'] = self.hand

        handplusstarter = copy.deepcopy(self.hand)
        handplusstarter.append(cc.decardify(self.startertext.get()))
        print(handplusstarter)
        ts, ps, fs, rs, desc = cc.score_hand(handplusstarter, True)
        self.scoredesclabel['text'] = desc

    def reset_hand(self):
        for i in np.arange(0, 13):
            self.numeachcard[i] = 0
            self.cardlabels[i]['text'] = self.numeachcard[i]
        self.hand = []
        self.handlabel['text'] = self.hand
        self.scoredesclabel['text'] = ''
        self.cribdesclabel['text'] = ''

    def test_crib(self):
        ntcstr = self.ncribtext.get()
        if ntcstr:
            numtocrib = int(ntcstr)
        else:
            numtocrib = 1
        desc = cc.card_to_remove(self.hand, cc.decardify(self.startertext.get()), numtocrib)
        self.cribdesclabel['text'] = desc

    def clear_test_crib(self):
        self.cribdesclabel['text'] = ''

app = App()
app.root.mainloop()
app.root.destroy()
