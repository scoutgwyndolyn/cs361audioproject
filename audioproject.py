from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from pydub import *
from os import *
from os.path import isfile, join

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 


from scipy import signal
from scipy.io import wavfile

# tooltip code to show more info when a label is hovered
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def showSpecGram():
    file = selectedFile.get()
    sampleRate, samples = wavfile.read(file)
    samples = samples[:,0] # this selects just the left channel since we need mono
    powerSpectrum, freqsFound, time, imageAxis = plt.specgram(samples, sampleRate)
    plt.show()

path = getcwd()

root = Tk()
root.geometry("1200x800")

root.title("Audio Manager")

audiofiles = ["select a file"]

audiofiles = [f for f in listdir(path) if isfile(join(path, f)) and f != "audioproject.py"]
audiofiles.append(audiofiles[0]) # fixes an issue where tkinter doesnt show the first item in the list

formats = [ ".mp3", ".aiff", ".ogg", ".flac", ".wav", ".flv", ".mp3"]

# initializing to get these to play nice with tkinter
selectedFormat = StringVar()
selectedFormat.set(formats[0])
selectedFile = StringVar()
selectedFile.set(audiofiles[0])

# dropdown and label to select input file
inputFileLabelText = StringVar()
inputFileLabelText.set("Select input file")
inputFileLabel = Label(root, textvariable = inputFileLabelText)
inputFileLabel.grid(row=1, column=1)
inputFileDropdown = OptionMenu(root, selectedFile, *audiofiles)
inputFileDropdown.grid(row=1, column = 2)

# dropdown and label for file format selection
desiredFormatLabelText = StringVar()
desiredFormatLabelText.set("Select desired audio format for export")
desiredFormatLabel = Label(root, textvariable = desiredFormatLabelText)
desiredFormatLabel.grid(row=9, column=1)
desiredFormatDropdown = OptionMenu(root, selectedFormat, *formats)
desiredFormatDropdown.grid(row=9, column=2)

# build in the amplitude plot, not working yet
amplitudePlotLabelText = StringVar()
amplitudePlotLabelText.set("Amplitude Plot")
amplitudePlotLabel = Label(root, textvariable = amplitudePlotLabelText)
amplitudePlotLabel.grid(row=4, column=1)
amplitudePlotFrame = Frame(padding=4)
amplitudePlot = plt.figure()
amplitudePlot.subplots_adjust(bottom=0.10, right = 0.96, left = 0.08, top= 0.95, wspace = 0.10)
amplitudePlot.add_subplot(111, facecolor=('xkcd:light grey'))
amplitudeCanvas = FigureCanvasTkAgg(amplitudePlot, amplitudePlotFrame)
toolbar = NavigationToolbar2Tk(amplitudeCanvas, amplitudePlotFrame)
toolbar.update()
amplitudeCanvas._tkcanvas.pack(fill=BOTH, expand=1)
amplitudePlotFrame.grid(row=5, column = 1)


def updateAmplitudePlot(*args):
    print("this should update the amplitude graph but that doesnt work yet")
    pass

selectedFile.trace("w", updateAmplitudePlot)

specgramCanvas = FigureCanvasTkAgg()

def exportCallback():
    #create new text file, first line is file name, second line is desired format
    if messagebox.askokcancel("Export Dialogue", "Do you want to export '%s' as %s? The original file will remain intact" % (selectedFile.get(), selectedFormat.get())):
        print("you have pressed the export button. this will do something eventually")


def showHideAmplitudeGraph():
    if(amplitudePlotFrame.winfo_ismapped()):
        amplitudePlotFrame.grid_forget()
        amplitudePlotLabel.grid_forget()
    else:
        amplitudePlotLabel.grid(row=4, column=1)
        amplitudePlotFrame.grid(row=5, column = 1)

exportButton = Button(root, text="Export", command = exportCallback)
exportButton.grid(row = 9, column = 3)

specgramButton = Button(root, text="Display Spectrogram", command = showSpecGram)
specgramButton.grid(row = 3, column = 2)
amplitudeGraphButton = Button(root, text = "Display Amplitude Graph", command = showHideAmplitudeGraph)
amplitudeGraphButton.grid(row = 3, column = 1)

CreateToolTip(inputFileDropdown, text = "To add files to this list, add them to the root folder this script is in")
CreateToolTip(exportButton, text="This will export the given audio file in the selected format, leaving the original file intact.")
CreateToolTip(specgramButton, text="This will open the spectrogram view in a new window")

print(audiofiles)

def onClose():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        exit()

root.protocol("WM_DELETE_WINDOW", onClose)
root.mainloop()
