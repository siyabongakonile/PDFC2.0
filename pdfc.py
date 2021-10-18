from posixpath import basename
import tkinter.messagebox
import PyPDF2
import fitz
import os
import time

__author__ = "Siyabonga Konile"
__authorsEmail__ = "siyabongakonile@gmail.com"

class PDF:
    def __init__(self, filename = ""):
        """Open the given file or creates a new one.
        
        Depending on the given parameters, when the filename is given
        then the PDF file will be open and if it is not given then
        a new PDF document will be created in memory.

        Parameters
        ----------
        filename: str
            The filepath of a PDF file to opened.
        """
        if filename != "":
            if os.path.exists(filename):
                self.filename = os.path.abspath(filename)
                self.doc = fitz.open(filename)
            else:
                self.doc = fitz.open()
                self.doc.new_page()

    def getNumPage(self):
        """Get number of page in the document"""
        return self.doc.page_count

    def close(self):
        """Closes the document and removes the filename"""
        self.doc.close()
        self.filename = ""

    def combine(self, otherFile, outputDir, filename) -> bool:
        """Combines the given PDFs and output that PDF in the given Dir
        
        Creates a new file that will have the content of the two chosen
        files in a chosen directory with a user given name.

        Parameters
        ----------
        otherFile: str
            The second file that will be embed on the current file.
            
        outputDir: str
            The directory to the output file will be created in.

        filename: str
            The filename of the new file.

        Return
        ------
        Boolean:
            True the file was successfully created or False otherwise
        """
        if not filename.lower().endswith(".pdf"): 
            filename = filename + ".pdf"
        newFilePath = os.path.join(outputDir, filename)

        try:
            otherDoc = fitz.open(otherFile)
            self.doc.insert_pdf(otherDoc, 0, self.getNumPage() - 1)
            self.doc.save(newFilePath)
            otherDoc.close()
            return True
        except:
            return False

    def delPages(self, listOfPages) -> bool:
        """Delete a given number of pages
        
        Takes in a list of page numbers to delete then deletes them
        and create a new PDF document

        Parameters
        ----------
        listOfPages: List
            The list of pages to delete.

        Returns
        -------
        Boolean:
            True if everything went successfully and False otherwise.
        """
        docDir = os.path.dirname(self.filename)
        docFilename = os.path.basename(self.filename)

        # delete pages is zeros based but method is not
        listOfPages = [i - 1 for i in listOfPages]

        try:
            self.doc.delete_pages(listOfPages)
            newDoc = fitz.open()
            newDoc.insert_pdf(self.doc)
            newDoc.save(os.path.join(docDir, docFilename + "-new.pdf"))
            newDoc.close()
            return True
        except:
            return False

    def swapPages(self, page1, page2) -> bool:
        """Swaps two pages in a PDF file.
        
        Parameters
        ----------
        page1: int
            The page number of the first page to be swapped

        page2: int
            The page number of the second page to be swapped

        Returns
        -------
        Boolean: 
            True when the pages where successfully swapped and False otherwise
        """
        pass

    def reversePages(self) -> bool:
        """Reverses the whole documents
        
        Change the order of all the pages and the first becomes the
        last page all the way to having the last become the first page.
        This method creates a new PDF with reversed pages.

        Return
        ------
        Boolean:
            True if the PDF file with the reversed pages was created 
            successfully and False otherwise.
        """
        pass

    def separatePages(self) -> bool:
        """Separates the whole document to single PDF pages
        
        Returns
        -------
        Boolean: 
            True if all the pages were successfully separated and 
            False otherwise
        """
        docDir = os.path.dirname(self.filename)
        docName = os.path.basename(self.filename)

        try:
            for pageNum in range(0, self.getNumPage()):
                newPDFFile = fitz.open()
                newPDFFile.insert_pdf(self.doc, pageNum, pageNum)
                filePath = os.path.join(docDir, docName + "-page" + str(pageNum + 1) + ".pdf")
                newPDFFile.save(filePath)
                newPDFFile.close()
            return True
        except:
            return False

    def insertPDF(self, pageNum, filename, outputFilename) -> bool:
        """Inserts a PDF file between the pages of another PDF file

        Parameters
        ----------
        pageNum: int
            The page number that the file will be inserted after.

        filename: str
            The path of the file to insert to the current one.

        outputFilename: str
            The path or name of the output file.

        Return
        ------
        Boolean:
            True if the file was created without an error or False otherwise.
        """
        if not outputFilename.lower().endswith(".pdf"):
            outputFilename = outputFilename + ".pdf"
        
        doc2 = fitz.open(filename)
        self.doc.insert_pdf(doc2, 0, -1, pageNum)
        self.doc.save(outputFilename)
        self.doc.close()

    def pageToImage(self, pageNum, imageType, outputImageDir = "", outputImageName = "") -> bool:
        """Converts a page into an SVG/PNG image
        
        This method coverts any page in the PDF document to an SVG or PNG 
        depending on what the user wants.

        Parameters
        ----------
        pageNum: int
            The number of the page to convert.

        imageType: str
            The type of image to convert the page to. 
            This is either 'svg' or 'png'

        outputImageDir: str
            The directory to create the image in

        outputImageName: str
            Custom name of the image
        
        Returns
        -------
        Boolean:
            True if the page wass successfully converted or False otherwise
        """
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
                mat = fitz.Matrix(5, 5)
                page = self.doc[pageNum]
                newPNG = page.get_pixmap(matrix = mat)
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
        return True

    def pageToSVG(self, pageNum, outputImageDir = "", outputImageName = "") -> bool:
        """Converts a page into an SVG image
        
        Parameters
        ----------
        pageNum: int
            The page number to convert to an image.

        outputImageDir: str
            The directory to create the output file in.

        outputImageName: str
            The name of the output file.

        Return 
        ------
        Boolean:
            True if the image was selected without an error or False otherwise.
        """
        return self.pageToImage(pageNum, "svg", outputImageDir, outputImageName)

    def pageToPNG(self, pageNum, outputImageDir = "", outputImageName = "") -> bool:
        """Converts a page into a PNG image
        
        Parameters
        ----------
        pageNum: int
            The page number to convert to an image.

        outputImageDir: str
            The directory to create the output file in.

        outputImageName: str
            The name of the output file.

        Return 
        ------
        Boolean:
            True if the image was selected without an error or False otherwise.
        """
        return self.pageToImage(pageNum, "png", outputImageDir, outputImageName)

    def imageToPage(self, outputImageDir = "", outputImageName = "") -> bool:
        """Converts an image to a PDF page.
        
        Takes in an image and creates a PDF file with a single page that is 
        filled with that image from it.

        Parameters
        ----------
        outputImageDir: str
            The path to the directory to output the image to.

        outputImageName: str 
            The name of the PDF product file.

        Returns
        -------
        Boolean:
            True if the document was successfully created and False otherwise.
        """
        if outputImageDir == "":
            outputImageDir = os.path.dirname(self.filename)
        
        if outputImageName == "":
            outputImageName = os.path.basename(self.filename) + "-image.pdf"

        try:
            bytePDFImage = self.doc.convert_to_pdf()
            # Create a new pdf file
            newPDF = open(os.path.join(outputImageDir, outputImageName), "wb")
            newPDF.write(bytePDFImage)
            newPDF.close()
            return True
        except:
            return False


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
