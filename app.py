import tkinter as tk
from tkinter import ttk
win = tk.Tk()
win.title("Yyz")

# label 
label = ttk.Label(win, text="somthing to sayh")
label.grid(column = 0, row = 0)

# combobox
labelLevel = tk.Label(win, text="Level:")
labelLevel.grid(column=0, row = 1)
options = tk.StringVar()
optionSelector = ttk.Combobox(win, width = 12, textvariable = options, state ='readonly')
optionSelector['values'] = ('lv.01', 'lv. 02', 'lv.25', 'lv.26')
optionSelector.grid(column = 1, row = 1)
optionSelector.current(1)

# entry
entryContent = tk.StringVar()
cmdEntry = ttk.Entry(win, width=12, textvariable = entryContent)
cmdEntry.grid(column = 0, row = 2)

def onButtonClicked():
    text = options.get() + " is selected"
    entryContent.set( text )
    #cmdEntry.configure(text =  options.get() + )


button = ttk.Button(win, text = "OK", command = onButtonClicked)
button.grid(column = 1, row = 2)

cmdEntry.focus() # set focus to a specific widget


win.mainloop()