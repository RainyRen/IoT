#-*- coding:utf-8 -*-  

# -----------------------------------------------------------------------------------------------------------------------
# One way is to stack the frames on top of each other, then you can simply raise one above the other in the stacking order. The one on top will be the one that is visible. This works best if all the frames are the same size, but with a little work you can get it to work with any sized frames.

# If you find the concept of creating instance in a class confusing, or if different pages need different arguments during construction, you can explicitly call each class separately. The loop serves mainly to illustrate the point that each class is identical.

# For example, to create the classes individually you can remove the loop (for F in (StartPage, ...) with this:

# self.frames["StartPage"] = StartPage(parent=container, controller=self)
# self.frames["PageOne"] = PageOne(parent=container, controller=self)
# self.frames["PageTwo"] = PageTwo(parent=container, controller=self)

# self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
# self.frames["PageOne"].grid(row=0, column=0, sticky="nsew")
# self.frames["PageTwo"].grid(row=0, column=0, sticky="nsew")

# Here's a bit of a contrived example to show you the general concept:

# import tkinter as tk   # python3
import Tkinter as tk   # python

TITLE_FONT = ("Helvetica", 18, "bold")

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
# ------------------------------------------------

 
# class GUIDemo(Frame):
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         self.grid()
#         self.createWidgets()
 
#     def createWidgets(self):
#         self.inputText = Label(self)
#         self.inputText["text"] = "Input:"
#         self.inputText.grid(row=0, column=0)
#         self.inputField = Entry(self)
#         self.inputField["width"] = 50
#         self.inputField.grid(row=0, column=1, columnspan=6)
 
#         self.outputText = Label(self)
#         self.outputText["text"] = "Output:"
#         self.outputText.grid(row=1, column=0)
#         self.outputField = Entry(self)
#         self.outputField["width"] = 50
#         self.outputField.grid(row=1, column=1, columnspan=6)
         
#         self.new = Button(self)
#         self.new["text"] = "New"
#         self.new.grid(row=2, column=0)
#         self.load = Button(self)
#         self.load["text"] = "Load"
#         self.load.grid(row=2, column=1)
#         self.save = Button(self)
#         self.save["text"] = "Save"
#         self.save.grid(row=2, column=2)
#         self.encode = Button(self)
#         self.encode["text"] = "Encode"
#         self.encode.grid(row=2, column=3)
#         self.decode = Button(self)
#         self.decode["text"] = "Decode"
#         self.decode.grid(row=2, column=4)
#         self.clear = Button(self)
#         self.clear["text"] = "Clear"
#         self.clear.grid(row=2, column=5)
#         self.copy = Button(self)
#         self.copy["text"] = "Copy"
#         self.copy.grid(row=2, column=6)
 
#         self.displayText = Label(self)
#         self.displayText["text"] = "something happened"
#         self.displayText.grid(row=3, column=0, columnspan=7)
 
# if __name__ == '__main__':
#     root = Tk()
#     app = GUIDemo(master=root)
#     app.mainloop()
