import tkinter as tk

def F11(event):

    global full_screen
    full_screen = not full_screen
    root.attributes("-fullscreen", full_screen)

def zoom(event):
    root.state('zoomed')


width, height = 400, 400
root=tk.Tk()

full_screen = False
#root.attributes("-zoomed", True)
root.bind("<F11>", F11)
root.bind("<Button-2>", zoom)

#app=full_screeneenApp(root)
root.mainloop()
