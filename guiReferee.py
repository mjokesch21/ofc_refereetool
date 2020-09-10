import os
import tkinter as tk
from tkinter import filedialog


import readMatches as rM
import gambleReferees as gR


def buttonGamble():
    # set referees to games
    scheduleResults, refereeResults = gR.mainGamble(scheduleEntry.get(), refereeEntry.get())

    # save the file
    fSavePath = filedialog.askdirectory(initialdir=os.getcwd(), title="Select directory where to save result files")

    gR.writeResults(scheduleResults, refereeResults, fSavePath)

    labelText.set('Saved files to "{0}'.format(fSavePath))


def buttonOpenFile(e):
    fPath = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",
                                       filetypes=(("json files", "*.json"), ("all files", "*.*")))
    e.delete(0, tk.END)
    # insert new_text at position 0
    e.insert(0, fPath)


if __name__ == '__main__':
    # create title
    window = tk.Tk()
    # set title
    window.title("Referee Gambler")

    # create elements
    scheduleLabel = tk.Label(window, text="Path to game schedule: ")
    scheduleEntry = tk.Entry(window, bd=5, width=40)
    scheduleButton = tk.Button(window, text='...', command=lambda: buttonOpenFile(scheduleEntry))

    refereeLabel = tk.Label(window, text="Path to referees: ")
    refereeEntry = tk.Entry(window, bd=5, width=40)
    refereeButton = tk.Button(window, text='...', command=lambda: buttonOpenFile(refereeEntry))

    buttonGamble = tk.Button(window, text='Set Referees', command=buttonGamble)
    buttonExit = tk.Button(window, text='Close', command=window.quit)

    labelText = tk.StringVar()
    consoleLabel = tk.Label(window, textvariable=labelText, bg="black", fg="white")
    labelText.set('Set input file paths and press "Set Referees"...')

    # send elements to gui
    scheduleLabel.grid(row=0, column=0, pady=10)
    scheduleEntry.grid(row=0, column=1, pady=10)
    scheduleButton.grid(row=0, column=2, pady=10)
    refereeLabel.grid(row=1, column=0, pady=20)
    refereeEntry.grid(row=1, column=1, pady=20)
    refereeButton.grid(row=1, column=2, pady=10)
    buttonGamble.grid(row=2, column=0, pady=20)
    buttonExit.grid(row=2, column=1, pady=20)
    consoleLabel.grid(row=3, column=0)

    # start window loop
    window.mainloop()

    print('FINISHED')
