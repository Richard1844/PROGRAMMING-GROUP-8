from tkinter import*




def doNothing():
    print("ok ok i wont...")


win=Tk()
win.geometry("350x250")
win.title("Pokemon Battle RPS Style")


menu = Menu(win)
win.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="New Project...",command=doNothing)
subMenu.add_command(label="New...",command=doNothing)
subMenu.add_separator()
subMenu.add_command(label="Exit...",command=doNothing)

editMenu=Menu(menu)
menu.add_cascade(label="Rules",menu=subMenu)
editMenu.add_command(label="New Game",command=doNothing)

subMenu = Menu(menu)
menu.add_cascade(label="Restart",menu=subMenu)
subMenu.add_command(label="Redo",command=doNothing)
subMenu.add_command(label="Edit",command=doNothing)

lblChoice = Label(win,text="Choice").grid(row=20,column=0)
v = StringVar(win,"1")

values={"Chartzard  1" : "1",
        "Blastoise  2" : "2",
        "Venusaur   3" : "3"}
for (text,value) in values.items():
    Radiobutton(win,text=text,variable=v,
                value = value).grid(padx=4,pady=20,column=0)

lblScore=Label(win,text="Score").grid(row=80,column=0)
lblHealth=Label(win,text="Health:").grid(row=100,column=0,pady=75)
btnButton=Button(win,text="Attack").grid(row=105,column=12,padx=400)
lblEnemy=Label(win,text="Enemy").grid(row=150,column=0,pady=90)


win.mainloop()


