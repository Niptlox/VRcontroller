##

from tkinter import *

width, height = 400, 400

root = Tk()
#help(root)
"""
f = open("hroot.txt", "w")
f.write(help())
f.colse()
"""
def print_size(ev):
    global root
    print(root.winfo_height(),root.winfo_width())
    #print(root.size)

def resizeFrames(events):
    print(events)


root.title("")
canv = Canvas(root, width=width ,height=height,bg='white')
canv.pack()
canv.focus_set()
canv.bind("<Button-1>", print_size)

#app = Application(root)
root.bind('<Configure>',resizeFrames)

"""
def press(event):
    x = event.x
    y = event.y
    motion(x, y)

def motion(x, y):

    if c.coords(ball)[2] < x:
	c.move(ball, 1, 0)
	root.after(10, motion, x, y)
    if c.coords(ball)[3] < y:
	c.move(ball, 0, 1)
	root.after(10, motion, x, y)

    if c.coords(ball)[2] > x:
	c.move(ball, -1, 0)
	root.after(10, motion, x, y)
    if c.coords(ball)[3] > y:
	c.move(ball, 0, -1)
	root.after(10, motion, x, y)

c.bind('<Button-1>', press)

"""

root.mainloop()
