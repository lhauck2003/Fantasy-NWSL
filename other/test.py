from tkinter import *

root = Tk()

root.title("Test")

root.geometry('350x200')


lbl = Label(root, text = "Test Label")
lbl.grid()

txt = Entry(root, width=10)
txt.grid(column=1, row=0)

def clicked():
	res = "You wrote " + txt.get()
	lbl.configure(text = res)

btn = Button(root, text = "click here",
		fg = "red", command=clicked)

btn.grid(column=2,row=0)

root.mainloop()
