from posixpath import basename
import tkinter.messagebox
import fitz
import os

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
        docDir = os.path.dirname(self.filename)
        docName = os.path.basename(self.filename)
        newPDFFilename = os.path.join(docDir, docName + "-swapped.pdf")

        page1 = page1 - 1
        page2 = page2 - 1
        if not page1 > page2:
            page1, page2 = page2, page1
        try:
            self.doc.move_page(page2, page1)
            self.doc.move_page(page1, page2)
            self.doc.save(newPDFFilename)
            return True
        except:
            return False

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
        docDir = os.path.dirname(self.filename)
        docName = os.path.basename(self.filename) + "-reversed.pdf"

        try:
            newPDFFile = fitz.open()
            for pageNum in range(self.getNumPage(), 0, -1):
                page = pageNum - 1
                newPDFFile.insert_pdf(self.doc, page, page)
            newPDFFile.save(os.path.join(docDir, docName))
            newPDFFile.close()     
            return True 
        except:
            return False  

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
