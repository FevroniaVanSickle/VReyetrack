# moves and calibrates .mp4 video according to user specifications
# goal: eye tracking analysis
# author: Fevronia Van Sickle
# version: 9/13/23

import os
import shutil
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import subprocess
from . import class_process_video, process, compare_eye_anno



#Gui to analyse eye tracking 
class RollOutMethodInterface(tk.Tk):
    def __init__(self,newVideoPath=None, newDataPath=None, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #set window configurations
        self.geometry("700x550+430+200")
        self.title("Roll Out Method Gui")

        #create container for windows on top of the root
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (HomePage, CalibrationPage, CreateLabelsPage, TadaPage):
            frame = F(container, self, newVideoPath=newVideoPath, newDataPath=newDataPath)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

        # ask user if they want to exit the application
        self.protocol("WM_DELETE_WINDOW", self.onClosing)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

     # asks user if they actually want to exit the app
    def onClosing(self):
        if messagebox.askyesno(message="Continue to quit?"):
            self.destroy()

# first page
class HomePage(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Home Page")
        self.title_label.grid(row=0, column=0, pady=20, padx=10, sticky='w')

        welcomeLabel = tk.Label(self, text="Welcome to the Graphic User Interface for the Roll Out Method!", font=('Times New Roman', 27))
        welcomeLabel.grid(row=1, column=0, pady=20, padx=10, sticky='w')

        overviewLabel1 = tk.Label(self, text="This GUI interface will walk you through three steps needed to determine attentional hitting points on 360 video stimuli:", font=('Times New Roman', 15))
        overviewLabel1.grid(row=2, column=0, pady=20, padx=10, sticky='w')

        overviewLabel2 = tk.Label(self, text="1. Creating video stills from your 360 video\n2. Determining areas of interest (AOIs) on your video stills at determined intervals\n3. Determining if participants’ attention falls within AOIs at each video still interval", font=('Times New Roman', 15))
        overviewLabel2.grid(row=3, column=0, pady=20, padx=10, sticky='w')

        overviewLabel3 = tk.Label(self, text="In order to use this program, you will need the following saved on your desktop:", font=('Times New Roman', 15))
        overviewLabel3.grid(row=4, column=0, pady=20, padx=10, sticky='w')

        overviewLabel4 = tk.Label(self, text="1. An .mp4 file of your 360 video\n2. An .xml file of raw eye-tracking data* derived from a participant viewing this 360 video", font=('Times New Roman', 15))
        overviewLabel4.grid(row=5, column=0, pady=20, padx=10, sticky='w')

        overviewLabel5 = tk.Label(self, text="* our program is currently only compatible with output from Tobii Pro but soon to be compatible with Varjo", font=('Times New Roman', 15))
        overviewLabel5.grid(row=6, column=0, pady=20, padx=10, sticky='w')

        self.nextButton = tk.Button(self, text="Next", command=lambda: self.controller.show_frame(CalibrationPage))
        self.nextButton.grid(row=7, column=0, pady=20, padx=10, sticky='w')


# second page
class CalibrationPage(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):

        # welcome text and file instructions
        choicesLabel = tk.Label(self, text="Video Stills Creation", font=(
            'Times New Roman', 27))
        choicesLabel.pack(side='top', anchor='w', pady = 20, padx=10)

        instructionLabel1 = tk.Label(self, text="Select your mp4 video file and xml data file from the available directories.", font=(
            'Times New Roman', 15))
        # instructionLabel1.place(x=20, y=80)
        instructionLabel1.pack(side='top', anchor='w', padx=10)

        # SELECT file
        selectFileButton = tk.Button(
            self, text="Select .mp4 File", command=self.selectVideoFile)
        # selectFileButton.place(x=20, y=120)
        selectFileButton.pack(side='top', anchor='w', pady = 10, padx=10)

        # SELECT file
        selectFileButton = tk.Button(
            self, text="Select .xml File", command=self.selectXMLFile)
        # selectFileButton.place(x=20, y=120)
        selectFileButton.pack(side='top', anchor='w', pady = 0, padx=10)

        #choices
        instructionLabel2 = tk.Label(self, text="Would you like your images cropped or flipped?", font=(
            'Times New Roman', 15))
        instructionLabel2.pack(side='top', anchor='w', padx=10)

        #crop check box
        self.checkState1 = tk.IntVar()
        self.check1 = tk.Checkbutton(self, text="crop video", font=(
            'Times New Roman', 16), variable=self.checkState1)
        self.check1.pack(padx=10, pady=10)

        #flip check box 
        self.checkState2 = tk.IntVar()
        self.check2 = tk.Checkbutton(self, text="flip video", font=(
            'Times New Roman', 16), variable=self.checkState2)
        self.check2.pack(pady=10)

        #set interval
        instructionLabel3 = tk.Label(self, text="Please select the interval you would like to use.", font=(
            'Times New Roman', 15))
        instructionLabel3.pack(side='top', anchor='w', padx=10)
        self.interval = tk.DoubleVar()
        spinbox = tk.Spinbox(self, from_=0, to=3, increment=0.5, textvariable=self.interval)
        spinbox.pack(pady=10)

        nextLabel = tk.Label(self, text="After you have made your selections, press 'Process Video' to create video stills .", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        nextLabel.pack(side='top', anchor='w', pady = 5, padx=10)

        self.processVideoButton = tk.Button(self, text="Process Video", command=self.controlSettings)
        self.processVideoButton.pack()

        instructionLabel2 = tk.Label(self, text="Your video, data, and stills will appear inside the 'Eyetrack' folder on your desktop. \n Please allow time for the folder to populate.", font=(
            'Times New Roman', 15))
        instructionLabel2.pack(side='top', anchor='w', padx=10)

        #goes to next page
        self.nextButton = tk.Button(self, text="Next", command=lambda: self.controller.show_frame(CreateLabelsPage))
        self.nextButton.pack(side='top', anchor='w', pady = 20, padx=10)

    # select the directory holding the video file
    def selectVideoFile(self):

        filetypes = (
            ('video files', '*.mp4'),
            ('All files', '*.*')
        )

        # open file dialog to select videoFile
        filePath = filedialog.askopenfilename(
            title='Open a file', initialdir='/', filetypes=filetypes)

        # show what was selected
        messagebox.showinfo(
            title='Selected File',
            message=filePath
        )
        self.path = filePath

        self.count = 0
        # place videoFile into Eyetrack Folder
        self.newEyetrackFolder(self.count)

    # adds new folder to user desktop and places video inside
    def newEyetrackFolder(self, count):

        # creates new folder
        homeDir = os.path.expanduser('~')
        folder = "EyeTrack"

        # creates an Eyetrack folder in the desktop
        try:
            os.makedirs(os.path.join(homeDir, "Desktop", folder))
        except:
            # breaks from try/except
            folder = "Eyetrack" + str(count)
            count += 1
            self.newEyetrackFolder(count)


        # save path to videoFile
        oldVideoPath = self.path
        print(oldVideoPath)
        # get video file name from path
        videoFileName = os.path.basename(oldVideoPath)
        print(videoFileName)

        #define directory path 
        self.folderPath = os.path.join(homeDir, "Desktop", folder)

        newVideoPath = os.path.join(self.folderPath, videoFileName)

        print(newVideoPath)
        shutil.move(oldVideoPath, newVideoPath)

    # select the directory holding the video file
    def selectXMLFile(self):

        filetypes = (
            ('video files', '*.xml'),
            ('All files', '*.*')
        )

        # open file dialog to select videoFile
        filePath = filedialog.askopenfilename(
            title='Open a file', initialdir='/', filetypes=filetypes)

        # show what was selected
        messagebox.showinfo(
            title='Selected File',
            message=filePath
        )
        self.path = filePath

        # place dataFile into Eyetrack/data Folder
        self.newDataFolder()

    # adds new folder to Eyetrack folder and places dataFile inside
    def newDataFolder(self):

        # creates new folder
        homeDir = os.path.expanduser('~')
        dataFolder = "Data"
        participantFolder = "001"
        destinationFolder = "Eye_Data_001"

        # creates an eyetrack/data folder in the desktop
        try:
            os.makedirs(os.path.join(homeDir, "Desktop/Eyetrack", dataFolder, participantFolder, destinationFolder))
        except:
            # breaks from try/except
            passed = True

        # save path to videoFile
        oldDataPath = self.path
        print(oldDataPath)
        # get video file name from path
        dataFileName = os.path.basename(oldDataPath)
        print(dataFileName)

        newDataPath = os.path.join(homeDir, "Desktop/Eyetrack", dataFolder + "/" + participantFolder,  destinationFolder, dataFileName)
        print(newDataPath)
        shutil.move(oldDataPath, newDataPath)

    #control settings
    def controlSettings(self):

        #crop
        if self.checkState1.get() == 0:
            cropBool = 0
        else:
            cropBool = 1

        #flip
        if self.checkState2.get() == 0:
            flipBool = 0
        else:
            flipBool = 1

        #interval
        interval = self.interval.get()
        interval = float(interval)

        #process the video
        self.frames = class_process_video.processVideo(self.folderPath, self.interval)
        self.frames.setOutputPath()
        self.frames.captureAtInterval(interval)
        self.frames.cropFrames(cropBool)
        self.frames.flipFrames(flipBool)

# third page
class CreateLabelsPage(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):
        
        # welcome text and file instructions
        choicesLabel = tk.Label(self, text="Create AOIs", font=(
            'Times New Roman', 27))
        choicesLabel.pack(side='top', anchor='w', pady = 20, padx=10)

        instructionLabel2 = tk.Label(self, text="Annotate video frames to determine Areas of Interest.", font=(
            'Times New Roman', 15))
        # instructionLabel2.place(x=20, y=180)
        instructionLabel2.pack(side='top', anchor='w', pady = 20, padx=10)

        instructionLabel3 = tk.Label(self, text="Save annotated frames to the folder of the frames you want to analyze; choose either 'frames', 'crop', or 'flip'.", font=(
            'Times New Roman', 15))
        # instructionLabel2.place(x=20, y=180)
        instructionLabel3.pack(side='top', anchor='w', pady = 10, padx=10)

        instructionLabel4 = tk.Label(self, text="Return to this GUI once done annotating.", font=(
            'Times New Roman', 15))
        # instructionLabel2.place(x=20, y=180)
        instructionLabel4.pack(side='top', anchor='w', pady = 10, padx=10)

        instructionLabel5 = tk.Label(self, text="If you accidentally close the GUI, simply navigate back to this page and continue.", font=(
            'Times New Roman', 15))
        # instructionLabel2.place(x=20, y=180)
        instructionLabel5.pack(side='top', anchor='w', pady = 10, padx=10)

        instructionLabel6 = tk.Label(self, text="You do not need to re-annotate your slides.", font=(
            'Times New Roman', 15))
        # instructionLabel2.place(x=20, y=180)
        instructionLabel6.pack(side='top', anchor='w', pady = 10, padx=10)

        # start labelling button 
        self.labelMeButton = tk.Button(self, text="Annotate Frames", command=self.startLabelMe)
        self.labelMeButton.pack(side='top', anchor='w', pady = 20, padx=10)

        # go back button 
        self.home_button = tk.Button(self, text="Go back", command=lambda: self.controller.show_frame(CalibrationPage))
        self.home_button.pack(side='top', anchor='w', pady = 20, padx=10)

        #next button
        self.nextButton = tk.Button(self, text="Next", command=lambda: self.controller.show_frame(TadaPage))
        self.nextButton.pack(side='top', anchor='w', pady = 20, padx=10)

    def startLabelMe(self):
        subprocess.Popen(['labelme'])


# fourth page
class TadaPage(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):
        
        # welcome text and file instructions
        choicesLabel = tk.Label(self, text="Data Tables and Hitting Points", font=(
            'Times New Roman', 27))
        choicesLabel.pack(side='top', anchor='w', pady = 20, padx=10)

        instructionLabel1 = tk.Label(self, text="Select the 'data' directory from within Desktop/Eyetrack", font=(
            'Times New Roman', 15))
        # instructionLabel1.place(x=20, y=80)
        instructionLabel1.pack(side='top', anchor='w', padx=10)

        # SELECT data folder
        selectFileButton1 = tk.Button(
            self, text="Select data folder", command=self.selectDataFolder)
        # selectFileButton.place(x=20, y=120)
        selectFileButton1.pack(side='top', anchor='w', pady = 10, padx=10)

        # SELECT image directory
        instructionLabel2 = tk.Label(self, text="Select the frames directory containing the frames and annotated frames you want analyzed", font=(
            'Times New Roman', 15))
        # instructionLabel1.place(x=20, y=80)
        instructionLabel2.pack(side='top', anchor='w', padx=10)

        selectFileButton2 = tk.Button(
            self, text="Select frames folder", command=self.selectFrameFolder)
        # selectFileButton.place(x=20, y=120)
        selectFileButton2.pack(side='top', anchor='w', pady = 10, padx=10)

        # # SELECT end image directory
        # instructionLabel3 = tk.Label(self, text="Select folder to place analyzed photos in", font=(
        #     'Times New Roman', 15))
        # # instructionLabel1.place(x=20, y=80)
        # instructionLabel3.pack(side='top', anchor='w', padx=10)

        # selectFileButton3 = tk.Button(
        #     self, text="Select image results folder", command=self.selectEndImageFolder)
        # # selectFileButton.place(x=20, y=120)
        # selectFileButton3.pack(side='top', anchor='w', pady = 10, padx=10)

        # SELECT 2D hitting points csv table
        instructionLabel4 = tk.Label(self, text="Select the csv table containing 2D hitting points located within new participant xyz folder", font=(
            'Times New Roman', 15))
        # instructionLabel1.place(x=20, y=80)
        instructionLabel4.pack(side='top', anchor='w', padx=10)

        selectFileButton4 = tk.Button(
            self, text="Select 2D hitting points", command=self.selectCSVFile)
        # selectFileButton.place(x=20, y=120)
        selectFileButton4.pack(side='top', anchor='w', pady = 10, padx=10)

        #get interval
        instructionLabel5 = tk.Label(self, text="Which interval did you select for your frames?", font=(
            'Times New Roman', 15))
        instructionLabel5.pack(side='top', anchor='w', padx=10)
        self.interval = tk.DoubleVar()
        spinbox = tk.Spinbox(self, from_=0, to=3, increment=0.5, textvariable=self.interval)
        spinbox.pack(pady=10)


        self.showResultButton = tk.Button(self, text="Calculate results", command=self.giveResults)
        self.showResultButton.pack(side='top', anchor='w', pady = 20, padx=10)

        # go back button 
        self.home_button = tk.Button(self, text="Go back", command=lambda: self.controller.show_frame(CalibrationPage))
        self.home_button.pack(side='top', anchor='w', pady = 10, padx=10)

        #home button
        self.nextButton = tk.Button(self, text="Home", command=lambda: self.controller.show_frame(HomePage))
        self.nextButton.pack(side='top', anchor='w', pady = 20, padx=10)

    # get Data Folder
    def selectDataFolder(self):

        # open file dialog to select videoFile
        filepath = filedialog.askdirectory()

        # show what was selected
        messagebox.showinfo(
            title='Selected folder',
            message=filepath
        )
        self.dataFolderPath = filepath

        #make sure correct Data folder is chosen 
        if (self.dataFolderPath.__contains__("Data")):
            print("passing data folder to process.py at line 450")
            print (os.getcwd())
            subprocess.run(["python3", "RollOutGui/src/process.py", self.dataFolderPath])
        else:
            print("Please select the data folder ")
            # sys.exit(1)
        

    # get Frame Folder
    def selectFrameFolder(self):

        # open file dialog to select videoFile
        filepath = filedialog.askdirectory()

        # show what was selected
        messagebox.showinfo(
            title='Selected folder',
            message=filepath
        )

        self.framesPath = filepath
        print(self.framesPath)
    
    #get EndImage folder
    def selectEndImageFolder(self):

        # open file dialog to select videoFile
        filepath = filedialog.askdirectory()

        # show what was selected
        messagebox.showinfo(
            title='Selected folder',
            message=filepath
        )

        self.endImagePath = filepath
        print(self.endImagePath)

    # select the directory holding the video file
    def selectCSVFile(self):

        filetypes = (
            ('video files', '*.csv'),
            ('All files', '*.*')
        )

        # open file dialog to select videoFile
        filepath = filedialog.askopenfilename(
            title='Open a file', initialdir='/', filetypes=filetypes)

        # show what was selected
        messagebox.showinfo(
            title='Selected File',
            message=filepath
        )

        self.csvFilePath = filepath
        print(self.csvFilePath)
        

    def giveResults(self):
        print("this is giveResults")

        #interval
        interval = self.interval.get()
        interval *= 100000
        interval = str(interval)
        
        try:
        # if (self.csvFilePath.contains("main.py")):
        #     print("this is the loader hi")
        
        # elif (self.framesPath.contains("main.p")):
        #     print("this is the loader hi")
        
        # elif (self.endImagePath.contains("main.py")):
        #     print("this is the loader hi")
        # else:
            #calculate results
            subprocess.run(["python3", "RollOutGui/src/compare_eye_anno.py", interval, self.csvFilePath, self.framesPath])

        except:
            print("loading")

        finally:
            subprocess.run(["python3", "RollOutGui/src/compare_eye_anno.py", interval, self.csvFilePath, self.framesPath])

