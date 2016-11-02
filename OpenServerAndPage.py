import OpenPage as OP
import pyhtonHTTPServer as serv
from Tkinter import *

class App:

    def __init__(self, master):
        w = Label(master, text="Pencil Code", fg="blue")
        w.config(bg='white')
        w.pack()


        c = Canvas(master, width=150, height=30)
        c.config(bg='white')
        c.create_rectangle(0, 0, 150, 5, fill="blue")
        c.pack()


        frame = Frame(master, height=32, width=150)
        frame.config(bg='white')
        frame.pack_propagate(0)
        frame.pack()


        # quit button
        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit
            )

        self.button.pack(fill="both", expand=1, side=LEFT)

        # run button
        self.open_button = Button(frame, text="RUN", fg='blue', command=self.open)
        self.open_button.config(pady=10)
        self.open_button.pack(fill="both", expand = 1,side=RIGHT)


    def open(self):
        OP.OpenPage()
        serv.OpenServer()

root = Tk()

app = App(root)

root.mainloop()

root.destroy()


