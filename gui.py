from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
import tkinter.messagebox
import os, traceback, shelve
import pdfc as pc
import time, threading
from threading import Thread
import platform

__author__ = "Siyabonga Konile"
__authorsEmail__ = "siyabongakonile@gmail.com"

# Thread class for the thread counter
class ThreadCounter(Thread):
    def __init__(self, callbackFunc):
        """Initialize The Thread Class"""
        Thread.__init__(self)
        self.func = callbackFunc
        self.go = True
        #this is used for breaking the loop of the
        #   callback function
        self.stopCheckingThreads = False

    def run(self):
        """Start the Thread"""
        while self.go:
            self.func()

    def stopThread(self):
        """This stop the Thread that checks other running threads"""
        print("Stoping the Thread")
        self.go = False
        self.stopCheckingThreads = True


class GUI:
    def __init__(self, theme = 1):
        """Get the theme number and display the theme
        
        Get GUI theme and Display the GUI

        Parameters
        ----------
        theme:
            The software has two different types of themes and
            this variable represents the theme number
        """
        theme = self.getTheme()
        self.themeDisp(theme)

    def themeDisp(self, theme):
        """Displays the chosen GUI theme
        
    
        """
        #create the main window the set it to
        self.window = Tk()
        self.window.title("PDFC")
        self.window.protocol('WM_DELETE_WINDOW', self.quitApp)
        # self.window.iconbitmap("i.ico")

        if theme == 1:
            self.window.geometry("700x400")
            self.window.resizable(0,0)
            #the side buttons
            leftSideBarFrame = Frame(self.window, bg = "white")
            leftSideBarFrame.pack(side = LEFT, fill = Y)

            #add the buttons
            btn1 = Button(leftSideBarFrame,
                          text = "Combine PDFs",
                          bg = "white",
                          cursor = "hand2",
                          relief = GROOVE,
                          command = self.combineGui)
            btn2 = Button(leftSideBarFrame,
                          text = "Insert PDF in another",
                          bg = "white",
                          cursor = "hand2",
                          relief = GROOVE,
                          command = self.insertGui)
            btn3 = Button(leftSideBarFrame,
                          text = "Delete Pages",
                          bg = "white",
                          cursor = "hand2",
                          relief = GROOVE,
                          command = self.delPageGui)
            btn4 = Button(leftSideBarFrame,
                          text = "Swap Pages",
                          bg = "white",
                          cursor = "hand2",
                          relief = GROOVE,
                          command = self.swapPagesGui)
            btn5 = Button(leftSideBarFrame,
                          text = "Reverse Pages",
                          bg = "white",
                          cursor = "hand2",
                          relief = GROOVE,
                          command = self.revPagesGui)
            btn6 = Button(leftSideBarFrame,
                          text = "Separate Pages",
                          bg = "white",
                          cursor = "hand2",
                          relief = GROOVE,
                          command = self.sepPagesGui)
            btn7 = Button(leftSideBarFrame,
                          text = "Change Theme",
                          bg = "white",
                          cursor = "hand2",
                          relief = GROOVE,
                          command = self.changeThemeGui)
            btn8 = Button(leftSideBarFrame,
                          text = "PDF page to Image",
                          bg = "white",
                          cursor = "hand2",
                          relief = GROOVE,
                          command = self.pageToImageGUI)
            btn9 = Button(leftSideBarFrame,
                          text = "Image To Page",
                          bg = "white",
                          cursor = "hand2",
                          relief = GROOVE,
                          command = self.imageToPageGUI)
            btn10 = Button(leftSideBarFrame,
                          text = "About PDFC",
                          bg = "white",
                          cursor = "hand2",
                          relief = GROOVE,
                          command = self.aboutGui)

            #display the buttons
            btn1.pack(side = TOP, fill = BOTH, expand = 1, ipadx = 30)
            btn2.pack(side = TOP, fill = BOTH, expand = 1, ipadx = 30)
            btn3.pack(side = TOP, fill = BOTH, expand = 1, ipadx = 30)
            btn4.pack(side = TOP, fill = BOTH, expand = 1, ipadx = 30)
            btn5.pack(side = TOP, fill = BOTH, expand = 1, ipadx = 30)
            btn6.pack(side = TOP, fill = BOTH, expand = 1, ipadx = 30)
            btn7.pack(side = TOP, fill = BOTH, expand = 1, ipadx = 30)
            btn8.pack(side = TOP, fill = BOTH, expand = 1, ipadx = 30)
            btn9.pack(side = TOP, fill = BOTH, expand = 1, ipadx = 30)
            btn10.pack(side = TOP, fill = BOTH, expand = 1, ipadx = 30)

            #the contents frame
            self.defaultOption()
        elif theme == 2:
            self.window.geometry("500x300")
            self.window.resizable(0,0)

            #add the top menu
            menubar = Menu(self.window, bg = "white")
            self.window.config(menu = menubar)

            # Combine Menu Item
            combineMenu = Menu(menubar, tearoff = 0)
            menubar.add_cascade(label = "Combine", 
                                menu = combineMenu)
            combineMenu.add_command(label = "Back to Back", 
                                    command = self.combineGui)
            combineMenu.add_command(label = "Insert in another", 
                                    command = self.insertGui)

            # Edit Menu Item
            editMenu = Menu(menubar, tearoff = 0)
            menubar.add_cascade(label  = "Edit", menu = editMenu)
            editMenu.add_command(label = "Delete Pages", 
                                command = self.delPageGui)
            editMenu.add_command(label = "Swap Pages", 
                                command = self.swapPagesGui)
            editMenu.add_command(label = "Reverse Pages", 
                                command = self.revPagesGui)
            editMenu.add_command(label = "Separate Pages", 
                                command = self.sepPagesGui)

            # Image Menu Item
            imageMenu = Menu(menubar, tearoff = 0)
            menubar.add_cascade(label = "Image", menu = imageMenu)
            imageMenu.add_command(label = "Page To Image", command = self.pageToImageGUI)
            imageMenu.add_command(label = "Image To Page", command = self.imageToPageGUI)

            # Theme Menu Item
            menubar.add_command(label = "Themes", 
                                command = self.changeThemeGui)

            # About Menu Item
            menubar.add_command(label = "About PDFC", 
                                command = self.aboutGui)

            #the contents frame
            self.defaultOption()
        self.theCounter = ThreadCounter(self.processCounter)
        self.theCounter.start()
        self.window.mainloop()

    def quitApp(self):
        """This function is called when you click the `X` button to Quit the Application"""
        #top the thread here
        print("Starting to Quit the Thread")
        self.theCounter.stopThread()
        while self.theCounter.is_alive():
            time.sleep(0.1)
        #quit the whole app
        self.window.destroy()

    def getTheme(self):
        """Get the theme value from a text file and return it.
            if the file is not created it will be created with theme 1"""
        if platform.system() == "Linux":
            if os.path.exists("pdfc\\theme.txt"):
                file = open("pdfc\\theme.txt", "r")
                themeNum = int(file.readline())
                file.close()
            else:
                if not os.path.exists("pdfc"):
                    os.mkdir("pdfc")
                file = open("pdfc\\theme.txt", "w")
                file.write("1")
                file.close()
                themeNum = 1
            return themeNum
        elif platform.system() == "Windows":
            # Get the theme number from a theme file
            if os.path.exists("c:/pdfc/theme.txt"):
                file = open("c:/pdfc/theme.txt", "r")
                themeNum = int(file.readline())
                file.close()
            else:
                #create the file with a default of theme
                # one if it does not exist
                if not os.path.exists("c:/pdfc"):
                    os.mkdir("c:/pdfc")
                file = open("C:/pdfc/theme.txt", "w")
                file.write("1")
                file.close()
                themeNum = 1
            return themeNum
        else:
            pass # For systems other than Linux and Windows

    def emptyFrame(self):
        """Deletes all the widgets in the work frame"""
        self.contFrame.pack_forget()
        self.contFrame = Frame(self.window, bg = "white")
        self.contFrame.pack(side = LEFT, fill = BOTH, expand = 1)

    def defaultOption(self):
        """This Displays text in the blank frame"""
        self.contFrame = Frame(self.window, bg = "white")
        self.contFrame.pack(side = LEFT, fill = BOTH, expand = 1)
        label = Label(self.contFrame, text = "PDFC", bg = "white", 
                        fg = "#2e2e2e", font = "Arial 40 italic")
        label.pack(side = LEFT, fill = BOTH, expand = 1)

    def combineGui(self):
        """Display the GUI for combining PDF files"""
        self.emptyFrame()
        frame1 = Frame(self.contFrame, bg = "white")
        frame1.pack(fill = X, padx = 10, pady = 5)
        label = Label(frame1, bg = "white", 
                    text = "Pick the PDFs you want to combine:", 
                    anchor = "w")
        label.pack(side = LEFT, fill = X, expand = 1)

        #create a second frame
        frame2 = Frame(self.contFrame, bg = "white")
        frame2.pack(fill = BOTH, expand = 1, padx = 10, pady = 5)
        self.file1 = StringVar()
        FileBox1 = Entry(frame2, textvariable=self.file1)
        FileBox1.pack(fill = BOTH, expand = 1, side = LEFT, padx = 5, 
                    ipady = 4, ipadx = 5)
        fileOneBrowseBtn = Button(frame2, text = "Browse", 
                                command=self.setFile1)
        fileOneBrowseBtn.pack(ipadx = 15)

        #create another frame
        frame3 = Frame(self.contFrame, bg = "white")
        frame3.pack(fill = BOTH, padx = 10, pady = 10)
        self.file2 = StringVar()
        FileBox2 = Entry(frame3, textvariable=self.file2)
        FileBox2.pack(fill = BOTH, expand = 1, side = LEFT, padx = 5, 
                    ipady = 4, ipadx = 5)
        fileOneBrowseBtn = Button(frame3, text = "Browse", 
                                command=self.setFile2)
        fileOneBrowseBtn.pack(ipadx = 15)

        #create another frame
        #the output directory
        frame4 = Frame(self.contFrame, bg = "white")
        frame4.pack(fill = BOTH, expand = 1, padx = 10, pady = 5)
        self.outputDir = StringVar()
        label2 = Label(frame4, text = "Choose output folder:", 
                    bg = "white", anchor = "w")
        label2.pack(fill = BOTH, expand = 1)
        FileBox3 = Entry(frame4, textvariable = self.outputDir)
        FileBox3.pack(fill = BOTH, expand = 1, side = LEFT, padx = 5)
        outBtn = Button(frame4, text = "Browse", command = self.outDir)
        outBtn.pack(ipadx = 15)

        #create a frame
        frame5 = Frame(self.contFrame, bg = "white")
        frame5.pack(fill = BOTH, expand = 1, padx = 10, pady = 5)
        labelFileName = Label(frame5, text = "The output name of you new file:", bg = "white", anchor = "w")
        labelFileName.pack(fill = BOTH)
        self.fileName = StringVar()
        fileName = Entry(frame5, textvariable = self.fileName)
        fileName.pack(fill = BOTH, expand = 1, side = LEFT, padx = 5, ipady = 4)

        #create a frame
        frame6 = Frame(self.contFrame, bg = "white")
        frame6.pack(fill = BOTH, expand = 1, padx = 10, pady = 10)
        combBtn = Button(frame6, text = "Combine", command = self.combine)
        combBtn.pack(side = RIGHT, ipadx = 15)

    def insertGui(self):
        """Display the GUI for insert a PDF in another"""
        self.emptyFrame()
        frame1 = Frame(self.contFrame, bg = "white")
        frame1.pack(fill = X, padx = 10, pady = 5)
        label = Label(frame1, text = "Pick the PDFs you want to insert to and the one to insert:", bg = "white", anchor = "w")
        label.pack(side = LEFT, fill = X, expand = 1)

        #create a second frame
        frame2 = Frame(self.contFrame, bg = "white")
        frame2.pack(fill = BOTH, expand = 1, padx = 10, pady = 5)
        self.file1 = StringVar()
        FileBox1 = Entry(frame2, textvariable=self.file1)
        FileBox1.pack(fill = BOTH, expand = 1, side = LEFT, padx = 5, ipady = 4, ipadx = 5)
        fileOneBrowseBtn = Button(frame2, text = "Browse", command=self.setFile1)
        fileOneBrowseBtn.pack(ipadx = 15)

        #create another frame
        frame3 = Frame(self.contFrame, bg = "white")
        frame3.pack(fill = BOTH, padx = 10, pady = 10)
        self.file2 = StringVar()
        FileBox2 = Entry(frame3, textvariable=self.file2)
        FileBox2.pack(fill = BOTH, expand = 1, side = LEFT, padx = 5, ipady = 4, ipadx = 5)
        fileOneBrowseBtn = Button(frame3, text = "Browse", command=self.setFile2)
        fileOneBrowseBtn.pack(ipadx = 15)

        #create another frame
        frame4 = Frame(self.contFrame, bg = "white")
        frame4.pack(fill = BOTH, expand = 1, padx = 10, pady = 5)
        self.insertAfter = StringVar()
        label2 = Label(frame4, text = "Choose the page number you want to insert after:", bg = "white", anchor = "w")
        label2.pack(fill = BOTH, expand = 1)
        FileBox3 = Entry(frame4, textvariable = self.insertAfter)
        FileBox3.pack(fill = BOTH, expand = 1, side = LEFT, padx = 5, ipady = 4)

        #create a frame
        frame5 = Frame(self.contFrame, bg = "white")
        frame5.pack(fill = BOTH, expand = 1, padx = 10, pady = 5)
        labelFileName = Label(frame5, text = "The output name of you new file:", bg = "white", anchor = "w")
        labelFileName.pack(fill = BOTH)
        self.fileName = StringVar()
        fileName = Entry(frame5, textvariable = self.fileName)
        fileName.pack(fill = BOTH, expand = 1, side = LEFT, padx = 5, ipady = 4)

        #create a frame
        frame6 = Frame(self.contFrame, bg = "white")
        frame6.pack(fill = BOTH, expand = 1, padx = 10, pady = 10)
        combBtn = Button(frame6, text = "Insert", command = self.insert)
        combBtn.pack(side = RIGHT, ipadx = 15)

    def delPageGui(self):
        """Displays the GUI for deleting a page"""
        self.emptyFrame()
        self.file1 = StringVar()
        frame = Frame(self.contFrame, bg = "white")
        frame.pack(side = TOP, fill = BOTH, expand = 1, padx = 10)

        heading    = Label(frame, text = "Delete Pages", bg = "white", fg = "#2e2e2e", font = "arial 18")
        heading.pack(side = TOP, fill = X, pady = 10)

        frameInner0 = Frame(frame, bg = "white")
        labelFile  = Label(frameInner0, text = "PDF file to delete page(s) in:", bg = "white")
        frameInner0.pack(side = TOP, fill = X)
        labelFile.pack(side  = LEFT, fill = X, padx = 10)

        frameInner = Frame(frame, bg = "white")
        fileEntry  = Entry(frameInner, textvariable = self.file1)
        fileBtn    = Button(frameInner, text = "Browse", command = self.setFile1)
        frameInner.pack(side = TOP, fill = X)
        fileEntry.pack(side  = LEFT, fill = X, expand = 1, ipady = 5, ipadx = 10, padx = 10)
        fileBtn.pack(side = LEFT, padx = 10, ipady = 3, ipadx = 15)

        dividerFrame = Frame(frame, bg = "white")
        dividerFrame.pack(side = TOP, fill = X, pady = 7)

        frameInner1 = Frame(frame, bg = "white")
        text = Label(frameInner1,
                     text = "Enter the pages you want to delete (if many separate them by a comma):",
                     bg = "white")
        frameInner1.pack(side = TOP, fill = X)
        text.pack(side = LEFT, fill = X, expand = 1)

        frameInner2     = Frame(frame, bg = "white")
        self.pagesToDel = StringVar()
        pageEntry       = Entry(frameInner2, textvariable = self.pagesToDel)
        frameInner2.pack(side = TOP, fill = X, ipadx = 20)
        pageEntry.pack(side = LEFT, fill = X, expand = 1, ipady = 5, padx = 10, pady = 2)

        frameInner3 = Frame(frame, bg = "white")
        delBtn = Button(frameInner3, text = "Delete Pages", command = self.delPages)
        frameInner3.pack(side = TOP, fill = X)
        delBtn.pack(side = RIGHT, ipadx = 15, ipady = 5, padx = 10, pady = 5)

    def swapPagesGui(self):
        """Displays the GUI for swaping pages"""
        self.emptyFrame()
        self.contFrame['pady'] = 20
        #get the PDF file
        frame1 = Frame(self.contFrame, bg = "white")
        self.file1 = StringVar()
        label1 = Label(frame1, text = "The PDF file:", 
                        bg = "white", anchor = "w")
        pdfEntry = Entry(frame1, textvariable = self.file1)
        getPdfBtn = Button(frame1, text = "Browse", 
                            command = self.setFile1)

        self.page1 = IntVar()
        self.page2 = IntVar()
        self.page1.set(1)
        self.page2.set(2)
        frame2 = Frame(self.contFrame, bg = "white")
        frame2inner1 = Frame(frame2, bg = "white")
        frame2inner2 = Frame(frame2, bg = "white")
        label2 = Label(frame2inner1, 
                text = "The Page you want to swap:", bg = "white")
        page1Entry = Entry(frame2inner1, textvariable = self.page1)
        label3 = Label(frame2inner2, 
                    text = "The page to swap with:", bg = "white")
        page2Entry = Entry(frame2inner2, textvariable = self.page2)

        frame3 = Frame(self.contFrame, bg = "white")
        swapBtn = Button(frame3, text = "Swap", 
                        command = self.swapPages)

        #Display the Widgets
        frame1.pack(side = TOP, fill = BOTH, padx = 20, ipady = 10)
        label1.pack(side = TOP, fill = BOTH, expand = 1, padx = 10)
        pdfEntry.pack(side = LEFT, fill = BOTH, expand = 1, padx = 10)
        getPdfBtn.pack(side = LEFT, padx = 10, ipadx = 15, ipady = 2)

        frame2.pack(side = TOP, fill = BOTH, padx = 20, pady = 10)
        frame2inner1.pack(side = LEFT, fill = BOTH)
        frame2inner2.pack(side = LEFT, fill = BOTH)
        label2.pack(side = TOP, fill = BOTH, pady = 5)
        label3.pack(side = TOP, fill = BOTH, pady = 5)
        page1Entry.pack(side = TOP, fill = BOTH, padx = 20)
        page2Entry.pack(side = TOP, fill = BOTH, padx = 20)

        frame3.pack(side = BOTTOM, fill = X, padx = 30, pady = 10)
        swapBtn.pack(side = RIGHT, ipady = 2, ipadx = 20)

    def swapPages(self):
        """Triggers the swap action and checks the results. 
        Gives a pop up of the results"""
        theSwapThread = Thread(target = pc.swapPages,
                                args = (self.file1.get(),
                                        self.page1.get(),
                                        self.page2.get()))
        theSwapThread.start()

    def revPagesGui(self):
        """Displays the GUI for reversing pages in a PDF file"""
        self.emptyFrame()
        self.file1 = StringVar()

        frame = Frame(self.contFrame, bg = "white")
        headerLabel = Label(frame, text = "Reverse Pages", bg = "white", fg = "#2e2e2e", font = "arial 20 italic")
        label1 = Label(frame, text = "Choose the PDF file you want to reverse:", bg = "white", fg = "#2e2e2e", anchor = "w")

        #frame that contains the text entry and the browse button
        frame1 = Frame(frame, bg = "white")
        entry = Entry(frame1, textvariable = self.file1)
        browseBtn = Button(frame1, text = "Browse", command = self.setFile1)

        #the bottom reverse button
        frame2 = Frame(self.contFrame, bg = "white")
        revBtn = Button(frame2, text = "Reverse", command = self.revPages)

        frame.pack(side = TOP, fill = BOTH, expand = 1)
        headerLabel.pack(side = TOP, fill = X, pady = 10)
        label1.pack(side = TOP, fill = X, padx = 10, pady = 10)
        frame1.pack(side = TOP, fill = X, padx = 0)
        entry.pack(side = LEFT, fill = X, expand = 1, padx = 10, ipady = 5)
        browseBtn.pack(side = LEFT, ipadx = 20, padx = 10, ipady = 2)
        frame2.pack(side = BOTTOM, fill = X, pady = 20)
        revBtn.pack(side = RIGHT, padx = 10, ipadx = 20, ipady = 2)

    def sepPagesGui(self):
        """Displays the GUI for replacing pages"""
        self.emptyFrame()
        self.file1 = StringVar()

        frame = Frame(self.contFrame, bg = "white")
        headerLabel = Label(frame, text = "Separate Pages", bg = "white", fg = "#2e2e2e", font = "arial 18")
        frame0 = Frame(frame, bg = "white")
        frame1 = Frame(frame, bg = "white")
        label1 = Label(frame0, bg = "white", text = "Select the PDF file to separate: ", font = "sans-serif 11")
        entry  = Entry(frame1, bg = "white", textvariable = self.file1)
        browseBtn = Button(frame1, text = "Browse", command = self.setFile1)
        frame2 = Frame(frame, bg = "white")
        sepBtn = Button(frame2, text = "Separate File", command = self.sepPages)
        
        frame.pack(side = TOP, fill = BOTH, expand = 1)
        headerLabel.pack(side = TOP, fill = X, pady = 10)
        frame0.pack(side = TOP, fill = X)
        label1.pack(side = LEFT, fill = X, padx = 16, pady = 2)
        frame1.pack(side = TOP, fill = BOTH, padx = 10)
        entry.pack(side = LEFT, fill = X, expand = 1, ipady = 5, ipadx = 10, padx = 5)
        browseBtn.pack(side = LEFT, ipady = 2, ipadx = 10, padx = 5)
        frame2.pack(side = TOP, fill = X)
        sepBtn.pack(side = RIGHT, padx = 15, pady = 15, ipadx = 15, ipady = 2)

    def changeThemeGui(self):
        """Displays the change theme window"""
        #get the theme number
        themeDir = "c:/pdfc/theme.txt" if platform.system() == "Windows" else "pdfc\\theme.txt"
        themeNum = open(themeDir, 'r')
        themeNum = int(themeNum.readline())
        self.themeNum = IntVar()
        self.themeNum.set(themeNum)

        self.themeWind = Toplevel(bg = "white")
        self.themeWind.title("Themes")
        self.themeWind.geometry("550x350")
        self.themeWind.resizable(0,0)
        # self.themeWind.iconbitmap("i.ico")

        #the label frame
        frame1 = Frame(self.themeWind, bg = "white")
        frame1.pack(side = TOP, pady = 10)
        headerLabel = Label(frame1, text = "Choose Theme",
                            font = "sans-serif 20 italic",
                            fg = "#2e2e2e", bg = "white")
        headerLabel.pack(side = TOP, fill = X, expand = 1)

        #the theme's frame
        frame2 = Frame(self.themeWind, bg = "white")
        frame2inner1 = Frame(frame2, width = 250, bg = "white")
        frame2inner2 = Frame(frame2, width = 250, bg = "white")
        frame2.pack(side = TOP, fill = BOTH, expand = 1)
        frame2inner1.pack(side = LEFT, fill = X, expand = 1)
        frame2inner2.pack(side = LEFT, fill = X, expand = 1)

        themeOneImg = PhotoImage(file = os.path.join("img", "theme1s.png"))
        themeTwoImg = PhotoImage(file = os.path.join("img", "theme2s.png"))

        radioBtnTheme1 = Radiobutton(frame2inner1, text = "Theme One",
                                     anchor = "w", variable = self.themeNum,
                                     value = 1, bg = "white")
        radioBtnTheme2 = Radiobutton(frame2inner2, text = "Theme Two",
                                     anchor = "w", variable = self.themeNum,
                                     value = 2, bg = "white")
        radioBtnTheme1.pack(side = TOP, fill = X, expand = 1)
        radioBtnTheme2.pack(side = TOP, fill = X, expand = 1)

        imgLabelOne = Label(frame2inner1, image = themeOneImg, bg = "white")
        imgLabelTwo = Label(frame2inner2, image = themeTwoImg, bg = "white")
        imgLabelOne.pack(side = TOP, fill = X, expand = 1)
        imgLabelTwo.pack(side = TOP, fill = X, expand = 1)

        #the theme colour
        frame4 = Frame(self.themeWind, bg = "white")
        frame4.pack(side = TOP, fill = BOTH, expand = 1, padx = 18, pady = 10)
        themeColor1 = Radiobutton(frame4, text = "Dark", bg = "white")
        themeColor2 = Radiobutton(self.themeWind, text = "Light", bg = "white")

        #bottom frame
        frame3 = Frame(self.themeWind, bg = "white")
        frame3.pack(side = LEFT, fill = BOTH, expand = 1, padx = 18, pady = 10)

        #the Save and Cancel Buttons
        cancelBtn = Button(frame3, text = "Cancel", command = self.themeWind.destroy)
        saveBtn   = Button(frame3, text = "save",   command = self.saveTheme)
        cancelBtn.pack(side = RIGHT, ipadx = 10, ipady = 3, padx = 5)
        saveBtn.pack(side = RIGHT, ipadx = 10, ipady = 3, padx = 5)

        self.themeWind.mainloop()

    def saveTheme(self):
        """Save the theme number in a file"""
        themeFile = "c:/pdfc/theme.txt" if platform.system() == "Windows" else "pdfc\\theme.txt"
        fh = open(themeFile, 'w')
        fh.write(str(self.themeNum.get()))
        fh.close()
        tkinter.messagebox.showinfo("Theme Changes",
                                    "The Changes are going to appear when you load the program again.")
        self.themeWind.destroy()

    def aboutGui(self):
        """Displays the about window"""
        aboutRoot = Toplevel()
        aboutRoot.title("About PDFC")
        aboutRoot.geometry("350x400")
        aboutRoot.resizable(0,0)
        # aboutRoot.iconbitmap("i.ico")

        #Add menu bar
        menubar = Menu(aboutRoot, tearoff = 0, bg = "white")
        aboutRoot.config(menu = menubar)

        #add wrapper frame
        wrapperFrame = Frame(aboutRoot, bg = "white")
        wrapperFrame.pack(side = TOP, fill = BOTH, expand = 1)

        topFrame = Frame(wrapperFrame, bg = "white")
        bottomFrame = Frame(wrapperFrame, bg = "white")
        aboutLabel  = Label(topFrame, 
                            text = "About PDFC", 
                            bg = "white", 
                            font = "sans-serif 20 italic")
        aboutText   = Text(topFrame, 
                            height = "10", 
                            bg = "#fff", 
                            fg = "#2e2e2e", 
                            relief = "flat")
        text = "PDFC is a free simple PDF page manipulator used for deleting, adding, swaping pages and combining PDF files.\n" 
        aboutText.insert(END, text, "desc")
        aboutText.insert(END, "\n")
        aboutText.insert(END, "Version: 2.0 \nCreator: Siyabonga Konile\nEmail: siyabongakonile@gmail.com\n", "details")
        aboutText.tag_config("desc", font = "sans-serif 12")
        aboutText.config(state="disabled");
        closeAboutBtn = Button(bottomFrame, text = "Close", fg = "#2e2e2e", font = "sans-serif 12", command = aboutRoot.destroy)

        topFrame.pack(side = TOP, fill = BOTH, expand = 1)
        bottomFrame.pack(side = TOP, fill = BOTH, expand = 1)
        aboutLabel.pack(side = TOP, fill = X, ipady = 10)
        aboutText.pack(side = TOP, fill = X, expand = 1, pady = 20, padx = 10)
        closeAboutBtn.pack(side = BOTTOM, pady = 15, ipadx = 20, ipady = 3)

        aboutRoot.mainloop()
        
    def updateGui(self):
        """Displays the update windows"""
        updateRoot = Toplevel()
        updateRoot.title("Updates")
        updateRoot.geometry("700x400")
        updateRoot.minsize(500, 400)

        #add wrapper frame
        wrapperFrame = Frame(updateRoot, bg = "white")
        wrapperFrame.pack(side = TOP, fill = BOTH, expand = 1)

        updateRoot.mainloop()

    def setFile1(self):
        """Opens a file dialog and saves the selected file path to `self.file1`"""
        self.file1.set(askopenfilename())

    def setFile2(self):
        """Opens a file dialog and saves the selected file path to `self.file2`"""
        self.file2.set(askopenfilename())

    def outDir(self):
        """Opens a select directory dialog 
        and saves the path of the selected directory to `self.outputDir`"""
        self.outputDir.set(askdirectory())

    def combine(self):
        """Calls  the pdf combiner function and checks if the operation was a success"""
        if self.checkPdfs():
            #check if the output directory is selected or not
            #   if not get the directory of the first file
            if self.outputDir.get() == '':
                file1Dirname = os.path.dirname(self.file1.get())
                self.outputDir.set(file1Dirname)

            theCombineThread = Thread(
                                    target = pc.combine,
                                    args = (
                                        [
                                            self.file1.get(), 
                                            self.file2.get()
                                        ],
                                        self.outputDir.get(),
                                        self.fileName.get()
                                    )
                                )
            theCombineThread.start()

    def insert(self):
        """Get the values of the fields in the insert GUI"""
        if self.checkPdfs(noDir = True):
            dirname = os.path.dirname(self.file1.get())
            if self.fileName.get() == ".pdf":
                filename = "new_" + os.path.basename(self.file1.get())
                self.fileName.set(os.path.join(dirname, filename))
            else:
                self.fileName.set(os.path.join(dirname, self.fileName.get()))

            #check if the page intered can be an integer
            try:
                self.insertAfter.set(int(self.insertAfter.get()))
            except:
                tkinter.messagebox.showerror("Page Error",
                                            "You did not enter an integer in the page box.")

            #start the thread
            theInsertThread = Thread(target = pc.insert, 
                                    args = (self.file1.get(), 
                                            self.file2.get(), 
                                            self.insertAfter.get(), 
                                            self.fileName.get()))
            theInsertThread.start()
            
    def checkPdfs(self, noDir = False):
        """check if the files exists and if they are PDFs"""

        if os.path.exists(self.file1.get()):
            #file 1
            if not self.file1.get().endswith(".pdf"):
                tkinter.messagebox.showerror("File Error", "PDF input one is not a PDF file.")
                return False
        else:
            tkinter.messagebox.showerror("Path Error",
                                         "The path for the first PDF is incorrect.")
            return False

        #file 2
        if os.path.exists(self.file2.get()) and self.file2.get().endswith(".pdf"):
            if not self.file2.get().endswith(".pdf"):
                tkinter.messagebox.showerror("File Error", "PDF input two is not a PDF file.")
                return False
        else:
            tkinter.messagebox.showerror("Path Error",
                                         "The path for the second PDF is incorrect.")
            return False

        if noDir == False:
            # Directory
            if not os.path.exists(self.outputDir.get()):
                tkinter.messagebox.showerror("Path Error",
                                             "The output Folder is not set right. We will use path of the selected files.")

        #filename
        #check if it does have an extention if not add it
        if not self.fileName.get().endswith(".pdf"):
            self.fileName.set(self.fileName.get() + ".pdf")
        
        if noDir == False:
            if os.path.exists(os.path.join(self.outputDir.get(), self.fileName.get())):
                if tkinter.messagebox.askyesno("File Exists", 
                                "The file already exists. Do you want to override the file?"):
                    return True
                else:
                    return False
        return True

    def revPages(self):
        """Trigers the reverse pages function in a Thread"""
        theRevThread = Thread(target = pc.reversePages, args = (self.file1.get(),))
        theRevThread.start() 

    def sepPages(self):
        """Trigers the function for separating a file in a Thread"""
        if self.file1.get() == "":
            tkinter.messagebox.showerror("File Error", "Select the PDF file to separate!")
            self.setFile1()
        else:
            #sepStatus = pc.sepPages(self.file1.get())
            theThread = Thread(target = pc.sepPages, args = (self.file1.get(),))
            theThread.start()

    def processCounter(self):
        """Counts the number of processes running in the background 
            and display the number of the processes in the title bar"""
            # The `self.theCounter.stopCheckingThreads` is changed to false when
            #   the `X`(close button) is clicked
        while not self.theCounter.stopCheckingThreads:
            try:
                processesRunning = threading.active_count()
                if platform.system() == 'Linux':
                    appThreads = 3
                else:
                    appThreads = 2
                    
                if processesRunning > appThreads:
                    self.window.title("PDFC " + str(processesRunning - appThreads ) + " Process(es) Running")
                else:
                    self.window.title("PDFC")
                time.sleep(1)
            except:
                break

    def delPages(self):
        """Prepare the pages to given by the user and 
            call the deleting function."""
        filename = self.file1.get()
        if filename.endswith(".pdf"):
            if not filename == "":
                pagesToDel = self.pagesToDel.get()
                if not pagesToDel == "":
                    #fix the string
                    sepString = pagesToDel.split(",")

                    # remove all the values that can not be turned into an int
                    valuesToRemove = []
                    for pos, value in enumerate(sepString):
                        try:
                            sepString[pos] = int(value)
                        except ValueError:
                            valuesToRemove.append(pos)

                    # remove the value that are illigal
                    for pos in valuesToRemove:
                        print(pos)
                        sepString[pos] = ""
                    #remove empty spaces
                    for _ in range(sepString.count("")):
                        sepString.remove("")

                    #create a thread
                    theThread = Thread(target = pc.delPages, args = (filename, sepString))
                    theThread.start()
                else:
                    tkinter.messagebox.showerror("Pages Error",
                                                 "Please select the pages you want to delete.")
            else:
                tkinter.messagebox.showerror("File Error",
                                             "Please select the PDF file you want to delete pages from.")
                self.setFile1()
        else:
            tkinter.messagebox.showerror("Type Error",
                                         "You did not select a PDF file, Please select one.")
            self.setFile1()

    def pageToImageGUI(self):
        """Display the GUI for changing a PDF page to an image"""
        self.emptyFrame()
        self.file1 = StringVar()
        self.imageType = StringVar()
        self.imageType.set("svg")

        frame = Frame(self.contFrame, bg = "white")
        headerLabel = Label(frame, text = "PDF Page to Image", bg = "white", fg = "#2e2e2e", font = "arial 18")
        frame0 = Frame(frame, bg = "white")
        frame1 = Frame(frame, bg = "white")
        label1 = Label(frame0, bg = "white", text = "Select the PDF file to convert: ", font = "sans-serif 11")
        entry  = Entry(frame1, bg = "white", textvariable = self.file1)
        browseBtn = Button(frame1, text = "Browse", command = self.setFile1)
        frame2 = Frame(frame, bg = "white")
        sepBtn = Button(frame2, text = "Convert File", command = self.convertPage)

        frame3 = Frame(frame, bg = "white")
        imageTypeOne = Radiobutton(frame3, bg = "white", text = "SVG", variable = self.imageType, value = "svg")
        imageTypeTwo = Radiobutton(frame3, bg = "white", text = "PNG", variable = self.imageType, value = "png")
        
        frame.pack(side = TOP, fill = BOTH, expand = 1)
        headerLabel.pack(side = TOP, fill = X, pady = 10)
        frame0.pack(side = TOP, fill = X)
        label1.pack(side = LEFT, fill = X, padx = 16, pady = 2)
        frame1.pack(side = TOP, fill = BOTH, padx = 10)
        entry.pack(side = LEFT, fill = X, expand = 1, ipady = 5, ipadx = 10, padx = 5)
        browseBtn.pack(side = LEFT, ipady = 2, ipadx = 10, padx = 5)
        imageTypeOne.pack(side = LEFT, fill = X, expand = 1)
        imageTypeTwo.pack(side = LEFT, fill = X, expand = 1)
        frame3.pack(side = TOP, fill = X, ipady = 15)
        frame2.pack(side = TOP, fill = X)
        sepBtn.pack(side = RIGHT, padx = 15, pady = 10, ipadx = 15, ipady = 0)

    def convertPage(self):
        """Convert the page depending on the selected type"""
        if self.imageType.get() == "svg":
            self.pageToSVG()
        else:
            self.pageToPNG()

    def pageToSVG(self):
        """Convert a page to an SVG image"""
        doc = pc.PDF(self.file1.get())
        doc.pageToSVG()

    def pageToPNG(self):
        """Covert a page to a PNG image"""
        doc = pc.PDF(self.file1.get())
        doc.pageToPNG()

    def imageToPageGUI(self):
        """Display the GUI for converting an image to a PDF page"""
        self.emptyFrame()
        self.file1 = StringVar()
        self.imageType = StringVar()
        self.imageType.set("svg")

        frame = Frame(self.contFrame, bg = "white")
        headerLabel = Label(frame, text = "Image to PDF Document", bg = "white", fg = "#2e2e2e", font = "arial 18")
        frame0 = Frame(frame, bg = "white")
        frame1 = Frame(frame, bg = "white")
        label1 = Label(frame0, bg = "white", text = "Select the Image file to convert: ", font = "sans-serif 11")
        entry  = Entry(frame1, bg = "white", textvariable = self.file1)
        browseBtn = Button(frame1, text = "Browse", command = self.setFile1)
        frame2 = Frame(frame, bg = "white")
        sepBtn = Button(frame2, text = "Convert File", command = self.convertImage)
        
        frame.pack(side = TOP, fill = BOTH, expand = 1)
        headerLabel.pack(side = TOP, fill = X, pady = 10)
        frame0.pack(side = TOP, fill = X)
        label1.pack(side = LEFT, fill = X, padx = 16, pady = 2)
        frame1.pack(side = TOP, fill = BOTH, padx = 10)
        entry.pack(side = LEFT, fill = X, expand = 1, ipady = 5, ipadx = 10, padx = 5)
        browseBtn.pack(side = LEFT, ipady = 2, ipadx = 10, padx = 5)
        frame2.pack(side = TOP, fill = X)
        sepBtn.pack(side = RIGHT, padx = 15, pady = 10, ipadx = 15, ipady = 0)

    def convertImage(self):
        """Check if the image exist and convert it to a PDF Document"""
        print("convert Image to PDF")

GUI()