import tkinter

window = tkinter.Tk()
window.title("GUI")

# creating a function called say_hi()
def post():
    tkinter.Label(window, text = "Posting right now!!!").pack()
def like():
    tkinter.Label(window, text = "Liking right now!!!").pack()
def comment_other_photos():
    tkinter.Label(window, text = "Commenting right now!!!").pack()
def follow_other_people():
    tkinter.Label(window, text = "Following right now!!!").pack()
def get_analytics():
    tkinter.Label(window, text = "Getting analytics right now!!!").pack()
def quit_program():
    tkinter.Label(window, text = "Quitting right now, have a good day!!!").pack()

btn = tkinter.Button(window, text = "Click Me!")
btn.bind("<Button-1>", post) # 'bind' takes 2 parameters 1st is 'event' 2nd is 'function'
btn.pack()


window.mainloop()

