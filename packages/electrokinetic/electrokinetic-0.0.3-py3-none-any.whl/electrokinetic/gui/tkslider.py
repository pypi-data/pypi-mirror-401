# https://stackoverflow.com/questions/69348288/setting-a-label-text-with-a-slider

from tkinter import *


class NewsPaper:
    def __init__(self, title, pageNumber):
        self.title = title
        self.pageNumber = pageNumber

newsPapers = []
newsPaper1 = NewsPaper("daily news", 52)
newsPapers.append(newsPaper1)
root = Tk()
var1 = IntVar()
var2 = IntVar()


def setCost(var, newsPaper):
    var2.set( var1.get() * newsPaper.pageNumber)

Label(root, textvariable=var2).pack()
Scale(root, from_=0, to=20, variable=var1, command=lambda val, var=var1:setCost(var1, newsPapers[0])).pack()

root.mainloop()