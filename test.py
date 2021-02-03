from pprint import pprint
import PyPDF2 

pdfFileObj = open('VRF-info-ALL.pdf', 'rb') 

pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

pageObj = pdfReader.getPage(10) 

pagetxt = (pageObj.extractText()).split('\n')
vrfname = print(pagetxt[1])
getnets = False
for line in pagetxt:
    if(getnets):
        pprint(line)
    if(line == 'VRF Superblock network(s):'):
        getnets = True
    if(getnets and line == ''):
        getnets = False


pdfFileObj.close() 