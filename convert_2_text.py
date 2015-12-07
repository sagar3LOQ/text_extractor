import sys, os, time, re

# For PDF to text conversion:
import textract

# To identify file type:
import magic # Needs libmagic1 installed.

# For parsing CV using a grammar definition:
import pyparsing

# For doc, docx and odt to text conversions:
import docx2txt



class CVParser(object):
    # Some commonly used regex patterns:
    def __init__(self, cvfile, password=None):
        self.errorMsg = None
      #  print "trying 1"
        self.cvFile = cvfile # Input CV file - can be in any of the following formats: pdf, doc, docx, rtf, txt, odt.
        if not os.path.exists(self.cvFile) or not os.path.isfile(self.cvFile):
            self.errorMsg = "The input file '%s' doesn't exist\n"%self.cvFile
            return None
        self.cvFormat = None # Can be any of the following: pdf, doc, docx, rtf, txt, odt.
#        self.cvObject = CurriculumVitae() # This is the object that will be populated by the parser.
        self.cvFilePasswd = password # password for the input CV file (if one exists).
        self.scratchDir =  os.path.dirname(self.cvFile) + os.path.sep + "temp_files" # Directory where the intermediate output files will be created (like, while parsing a pdf file, we need to convert it to a text file first, and then parse the text file. This is the location where the text file will be created.
        if not os.path.exists(self.scratchDir):
            os.makedirs(self.scratchDir)
        self.cvTextFile = None
      #  print "trying 3"
        randomStr = 1
       # print randomStr
        self.userTempDir = self.scratchDir + os.path.sep + "tmp_" + randomStr.__str__()


    """
    Identify the format of the input file.
    """
    def _checkFormat(self):
        mime = magic.Magic(mime=True)
        filetype = mime.from_file(self.cvFile)
        fileparts = self.cvFile.split(".")
        ext = fileparts.pop()
        ext = ext.lower()
        primaryEnc, secondaryEnc = filetype.split("/")
        print primaryEnc
        print secondaryEnc
        if ext == 'pdf' or ext == 'doc' or ext == 'docx' or ext =='rtf':
            self.cvFormat = ext
            print ext
            print "test pass format"
            return(True)
        elif ext == 'text' :
            self.cvFormat = 'txt'
            print ext
            print "raw text"
            return(True)
            
        else:
#            self.errorMsg = "unknown file format - %s"%filetype
             return(True)
            

    """
    This method will identify the type of the input file and dispatch the file to the appropriate convertor method.
    """
    def preprocess(self):
        self._checkFormat()
        if self.errorMsg is not None:
            print self.errorMsg
            sys.exit(0)
        if self.cvFormat == 'pdf':
            self._convert_pdf_to_text()
        elif self.cvFormat == 'docx':
            self._convert_docx_to_text()
        elif self.cvFormat == 'doc':
            self._convert_doc_to_text()
        elif self.cvFormat == 'rtf':    
            self._convert_rtf_to_text()
        elif self.cvFormat == 'txt':
            print "Unrecognised format : pass decoding"
        else:
            print "Unrecognised format : pass decoding"
        return(self.cvTextFile)


    def _convert_pdf_to_text(self):
        print "processing pdfs"
        input_pdf = self.cvFile
        print self.cvFile
        outputPath = self.scratchDir
        inputPath = os.getcwd()
        if os.path.exists(input_pdf):
            inputPath = os.path.dirname(input_pdf)
        input_filename = os.path.basename(input_pdf)
        input_parts = input_filename.split(".")
        input_parts.pop()
        randomStr = int(time.time())
        output_filename = outputPath + os.path.sep + ".".join(input_parts)  + r".txt"
        self.cvTextFile = output_filename
        print "writing output to {0}".format(output_filename)
        output_filename = output_filename.replace (" ", "_")
        outfp = open(output_filename, 'w')

        text = textract.process(input_pdf)
 
        outfp.write(text)
        print "written sucessfully"
        outfp.close()
        return (0)

    def _convert_rtf_to_text(self):
        print "processing rtf"
        input_pdf = self.cvFile
        print self.cvFile
        outputPath = self.scratchDir
        inputPath = os.getcwd()
        if os.path.exists(input_pdf):
            inputPath = os.path.dirname(input_pdf)
        input_filename = os.path.basename(input_pdf)
        input_parts = input_filename.split(".")
        input_parts.pop()
        randomStr = int(time.time())
        output_filename = outputPath + os.path.sep + ".".join(input_parts)  + r".txt"
        self.cvTextFile = output_filename
        print "writing output to {0}".format(output_filename)
 #       output_filename = output_filename.replace (" ", "_")
        outfp = open(output_filename, 'w')

        text = textract.process(input_pdf)
 
        outfp.write(text)
        print "written sucessfully"
        outfp.close()
        return (0)
    
    def _convert_doc_to_text(self, password=None):
        print "decoding doc file"
        input_doc = self.cvFile
        outputPath = self.scratchDir
        inputPath = os.getcwd()
        if os.path.exists(input_doc):
            inputPath = os.path.dirname(input_doc)
        input_filename = os.path.basename(input_doc)
        input_parts = input_filename.split(".")
        input_parts.pop()
       
        output_filename = outputPath + os.path.sep + ".".join(input_parts)  + r".txt"
        output_filename = output_filename.replace (" ", "_")
        
        print "writing output to {0}".format(output_filename)
        self.cvTextFile = output_filename
        print "written sucessfully"
        cmd = "catdoc %s >%s"%(self.cvFile, self.cvTextFile) # Dangerous!!! Why not use 'subprocess'?
        os.system(cmd)
        return(0)



    def _convert_docx_to_text(self, password=None):
        print "Decoding docx file"
        input_docx = self.cvFile
        outputPath = self.scratchDir
        inputPath = os.getcwd()
        if os.path.exists(input_docx):
            inputPath = os.path.dirname(input_docx)
        input_filename = os.path.basename(input_docx)
        input_parts = input_filename.split(".")
        input_parts.pop()
        randomStr = int(time.time())
        output_filename = outputPath + os.path.sep + ".".join(input_parts)  + r".txt"
        output_filename = output_filename.replace (" ", "_")
        print "writing output to {0}".format(output_filename)

      #  self.cvTextFile = output_filename
        text = docx2txt.process(input_docx)
      #  print text
        fw = open(output_filename, "w")
        print "test"
        fw.write(text.encode('utf-8'))
        print "written sucessfully"
        fw.close()
        return(0)




if __name__ == '__main__':
#    cvfile = sys.argv[1]
    dir_name = "/home/viswanath/workspace/dataset/rejected_profiles"
    for root, dirs, files in os.walk(dir_name):
        for file in files:
            cvfile = os.path.join(root, file)
            print cvfile
            cvparser = CVParser(cvfile)
            if cvparser.errorMsg:
                print cvparser.errorMsg
                sys.exit(0)
            try:
                cvparser.preprocess()
            except:
                print "I am in trobule."
                sys.exit(1)


