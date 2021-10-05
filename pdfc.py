from posixpath import basename
import tkinter.messagebox
import PyPDF2
import fitz
import os
import time

__author__ = "Siyabonga Konile"
__authorsEmail__ = "siyabongakonile@gmail.com"
__lastModified__ = "04 Oct 2021 21:48"

class PDF:
    def __init__(self, filename):
        """Open the given file"""
        if filename != "":
            if os.path.exists(filename):
                self.filename = os.path.abspath(filename)
                self.doc = fitz.open(filename)
            else:
                raise RuntimeError("Given file path does not exist.")

    def combine(self, otherFile, outputDir, filename):
        """This function combines the given PDFs 
        and output that PDF in the given Dir"""
        pass

    def delPages(self, listOfPages):
        pass

    def swapPages(self, page1, page2):
        pass

    def reversePages(self):
        pass

    def separatePages(self):
        pass

    def insertPDF(self, pageNum, filename, outputFilename):
        """Inserts a PDF file between the pages of another PDF file

        param pageNum   - THe page number that the file 
                            will be inserted after.
        param filename     - The path of the file to insert to the current one.
        param outputFilename     - The path or name of the output file."""
        if pageNum > self.doc.page_count():
            pageNum = self.doc.page_count()

        if os.path.exists(filename):
            raise RuntimeError("File path does not exist.")
        
        if self.filename == os.abspath(filename):
            doc2 = self.doc
        else:
            doc2 = fitz.open(filename)

    def pageToImage(self, pageNum, imageType, outputImageDir = "", outputImageName = ""):
        """Converts a page into an SVG/PNG image"""
        pageNum = pageNum - 1
        basename = os.path.basename(self.filename)

        if imageType == "svg":
            newImage = self.doc[pageNum].get_svg_image()
        
        if outputImageDir == "": 
            outputImageDir = os.path.dirname(self.filename)
        if outputImageName == "":
            if imageType == "svg":
                outputImageName = basename + "_page" + str(pageNum + 1) + ".svg"
            else:
                outputImageName = basename + "_page" + str(pageNum + 1) + ".png"
        else:
            if not outputImageName.lower().endswith(".svg") or not outputImageName.lower().endswith(".png"):
                if imageType == "svg":
                    outputImageName = outputImageName + ".svg"
                else:
                    outputImageName = outputImageName + ".png"

        try:
            if imageType == "svg":
                newSVG = open(os.path.join(outputImageDir, outputImageName), "w")
                newSVG.write(newImage)
                newSVG.close()
            else:
                newPNG = self.doc.get_page_pixmap(pageNum)
                newPNG.save(os.path.join(outputImageDir, outputImageName))
        except PermissionError:
            tkinter.messagebox.showerror("Permission Error", 
                "It seems like the program does not have access to write on this folder.")
        except OSError:
            tkinter.messagebox.showerror("Operating System Error", 
                "This might be because the disk is full.")
        except:
            tkinter.messagebox.showerror("Error", 
                "Something went wrong while trying to create a file.")

    def pageToSVG(self, pageNum = 1, outputImageDir = "", outputImageName = ""):
        """Converts a page into an SVG image"""
        self.pageToImage(pageNum, "svg", outputImageDir, outputImageName)

    def pageToPNG(self, pageNum = 1, outputImageDir = "", outputImageName = ""):
        """Converts a page into a PNG image"""
        self.pageToImage(pageNum, "png", outputImageDir, outputImageName)


def combine(pdfFiles, outputDir, filename):
    """This function combines the given PDFs 
        and output that PDF in the given Dir"""
    #open files and add them to a newFile
    newPdfFile = PyPDF2.PdfFileWriter()
    for ctr in range(len(pdfFiles)):
        try:
            openFile = open(pdfFiles[ctr], "rb")
            pdfFiles[ctr] = PyPDF2.PdfFileReader(openFile)
        except:
            tkinter.messagebox.showerror("File Error", 
                                "Could not open file" + str(ctr + 1))
            return False

    for fileIndex in range(len(pdfFiles)):
        for numPage in range(pdfFiles[fileIndex].numPages):
            page = pdfFiles[fileIndex].getPage(numPage)
            newPdfFile.addPage(page)

    newFileDir = os.path.join(outputDir, filename)
    try:
        newFile = open(newFileDir, "wb")
    except PermissionError:
        tkinter.messagebox.showinfo("File Permission",
                "Cannot access " + filename + \
                " because the file is being used by another program.")
        tkinter.messagebox.showerror("Unsuccessful Operation", 
                                    "A problem occured while trying to combine the PDFs. Try again")
    newPdfFile.write(newFile)
    tkinter.messagebox.showinfo("Successfully Combined",
                            "The PDFs where successfully combined.")

def delPages(pdfFilename, listOfPages):
    """This function deletes the given page from a PDF file"""
    print("Pges to Delete: ", listOfPages)
    try:
        pdfFile = open(pdfFilename, 'rb')
        PdfReader = PyPDF2.PdfFileReader(pdfFile)
        print("Number of pages: ", PdfReader.numPages)
    except:
        tkinter.messagebox.showerror("Openning Error",
                                    "Could not process the PDF file.")
    filename = os.path.basename(pdfFilename)
    dirname = os.path.dirname(pdfFilename)
    newWriter = PyPDF2.PdfFileWriter()

    #remove the given pages and create a new file
    for pageNum in range(1, PdfReader.numPages + 1):
        if pageNum in listOfPages:
            continue
        try:
            newWriter.addPage(PdfReader.getPage(pageNum - 1))
        except IndexError:
            continue
        
    newFile = open(os.path.join(dirname, "new_" + filename), 'wb')
    newWriter.write(newFile)
    newFile.close()
    pdfFile.close()
    tkinter.messagebox.showinfo("Done",
                            "The pages where successfully deleted.")
    
def swapPages(pdfFilename, page1, page2):
    """This function swap the given page numbers"""
    #return -1 if a problem occured while opening the PDF file
    #return -2 if a problem occured while processing the file
    #return -3 if a number of the page is less or greater than
    #   the number of pages of the PDF file
    #return 1  if the process was a success
    try:
        pdfFile = open(pdfFilename, 'rb')
    except:
        tkinter.messagebox.showerror("Error Openning File",
                    "Could not open the PDF file. Please try again")
        return
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    pdfNumPages = pdfReader.numPages

    #check the number if they are in range
    if (page1 < 1 or pdfNumPages < page1) or \
        (page2 < 1 or pdfNumPages < page2):
        tkinter.messagebox.showerror("Page Error", 
                            "It seems like there is a problem with the page count.")
        return

    p1 = pdfReader.getPage(int(page1) - 1)
    p2 = pdfReader.getPage(int(page2) - 1)

    #copy the pdf with the chnges in a new one
    newPdf = PyPDF2.PdfFileWriter()
    for pageNum in range(pdfNumPages):
        if (page1 - 1) == pageNum:
            newPdf.addPage(p2)
            continue
        elif (page2 - 1) == pageNum:
            newPdf.addPage(p1)
            continue
        newPdf.addPage(pdfReader.getPage(pageNum))

    currentDir = os.path.dirname(pdfFilename)
    filename = os.path.basename(pdfFilename)
    os.chdir(currentDir)
    nPdf = open(filename[:-4] + '_swaped.pdf', 'wb')
    newPdf.write(nPdf)
    nPdf.close()
    pdfFile.close()
    tkinter.messagebox.showinfo("Successfully Done",
                        "The PDF pages were successfully swaped.")

def reversePages(filename):
    """ Creates a file with the pages of the selected one reversed """
    # check if the file ends with '.pdf'
    if filename.endswith(".pdf"):
        #open the file
        try:
            fileHandler = open(filename, 'rb')
        except:
            tkinter.messagebox.showerror("Error Openning File", 
                                        "Something went wrong while trying to open the PDF file.")

        # read the file with PyPDF2
        try:
            reader = PyPDF2.PdfFileReader(fileHandler)
        except:
            tkinter.messagebox.showerror("Reading file error", 
                                        "An error has occured while trying to read the PDF file.")

        #get the number of pages
        fileNumPages = reader.numPages

        # reverse the pages and add them in a new PDF file
        try:
            #get the reversed pages
            newFile = PyPDF2.PdfFileWriter()
            #get the pages in reverse order
            for i in range(fileNumPages - 1, -1, -1):
                page = reader.getPage(i)
                newFile.addPage(page)

            
            oldDir = os.getcwd()
            currentDir = os.path.dirname(filename)
            os.chdir(currentDir)
            fileBasename = os.path.basename(filename)
            newPdf = open(fileBasename[:-4] + "-" + 
                        str(round(time.time())) + ".pdf", 'wb')
            newFile.write(newPdf)
            newPdf.close()
            fileHandler.close()
            os.chdir(oldDir)
        except:
            tkinter.messagebox.showerror("processing Error", 
                                        "An error has occured while processing the the document.")
        tkinter.messagebox.showinfo("success", 
                                "The PDF was successfully reversed.")
    else:
        tkinter.messagebox.showerror("Error", 
                            "Something went wrong. Please try again.")

def sepPages(filename):
    """Separate the given file into its pages."""
    if filename.endswith(".pdf"):
        # Try to open and read the PDF file
        try:
            pdfFile = open(filename, 'rb')
            reader  = PyPDF2.PdfFileReader(pdfFile)
        except:
            return 2
        # Start the separating process
        workingDir = os.path.dirname(filename)
        numPages = reader.numPages
        for page in range(numPages):
            pageNo = page + 1
            #print("PAGE: ", pageNo)
            newPage = open(os.path.join(workingDir, "page-" 
                +str(pageNo) + "-" + os.path.basename(filename)), 'wb')
            pageWriter = PyPDF2.PdfFileWriter()
            pageWriter.addPage(reader.getPage(page))
            pageWriter.write(newPage)
            newPage.close()
        pdfFile.close()
        #tell the user that the process was a success
        tkinter.messagebox.showinfo("Success",
                            "The Pages were separated successfully.")
    else:
        return 1

def insert(file1, file2, pageNum, outputFilename):
    """Inserts a PDF file between the pages of another PDF file

        param file1     - The file to insert the other 
                            PDF file will be inserted to.
        param file2     - The file to insert.
        param pageNum   - THe page number that the file 
                            will be inserted after.
        param outputFilename - The output file."""
    pageNum = int(pageNum)
    if file1 == file2:
        isSameFile = True
        pdfFile1 = open(file1, 'rb')
        pdfFile2 = pdfFile1
        reader1 = PyPDF2.PdfFileReader(pdfFile1)
        reader2 = reader1
    else:
        isSameFile = False
        pdfFile1 = open(file1, 'rb')
        pdfFile2 = open(file2, 'rb')
        reader1 = PyPDF2.PdfFileReader(pdfFile1)
        reader2 = PyPDF2.PdfFileReader(pdfFile2)

    dirname = os.path.dirname(file1)
    newFileWriter = PyPDF2.PdfFileWriter()

    #add the page to the new file
    for page in range(1, reader1.numPages + 1):
        # Insert the second pdf after reaching
        # the number of page to insert after
        if (page - 1) == pageNum:
            for page2 in range(reader2.numPages):
                newFileWriter.addPage(reader2.getPage(page2))
        newFileWriter.addPage(reader1.getPage(page - 1))

    newFile = open(outputFilename, 'wb')
    newFileWriter.write(newFile)
    newFile.close()

    # Close all the open files
    if isSameFile:
        pdfFile1.close()
    else:
        pdfFile1.close()
        pdfFile2.close()
    newFile.close()
    tkinter.messagebox.showinfo("Done",
        "The PDF file was successfully inserted.")
