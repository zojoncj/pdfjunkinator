from pprint import pprint
import PyPDF2 

pdfFileObj = open('VRF-info-ALL.pdf', 'rb') 

pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 


pageObj = pdfReader.getPage(10) 

pprint(pageObj.extractText()) 

pdfFileObj.close() 
