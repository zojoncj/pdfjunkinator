from pprint import pprint
import PyPDF2
from netaddr import IPNetwork, IPAddress
import csv



#the file below needs to be the same directory as this file.
pdfFileObj = open('VRF-info-ALL.pdf', 'rb')

pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

pages = pdfReader.getNumPages()
#to hold all of our cidrs
cidrs = {}

#cause you never not start at 0 for an incrementer
i = 0
#iterate over the PDF and create a "dictionary" mapping subnet to vrfname
for i in range(pages):
    pageObj = pdfReader.getPage(i)
    pagetxt = (pageObj.extractText()).split('\n')
    vrfname = pagetxt[1]
    getnets = False
    for line in pagetxt:
        if(getnets and line.startswith('Page')):
            getnets = False
        if(getnets and not line.startswith('-')):
            cidr = (line.split(' '))[2]
            cidrs[cidr] = vrfname
        if(line == 'Router SVIs Found:'):
            getnets = True


pdfFileObj.close()