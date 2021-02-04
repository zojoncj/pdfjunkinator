from pprint import pprint
import PyPDF2
import ipaddress
import csv

cidrs = {}

def iptovrf(ip):
    retval = 'NotFound'
    for cidr in cidrs:
        if ipaddress.ip_address(ip) in ipaddress.ip_network(cidr):
            retval= cidrs[cidr]
    return retval

#the file below needs to be the same directory as this file.
pdfFileObj = open('VRF-info-ALL.pdf', 'rb')

pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

pages = pdfReader.getNumPages()
#to hold all of our cidrs

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
ccsvo = open('cidrs.csv','w', newline='\n')
for k in cidrs:
    ccsvo.write(k+','+cidrs[k]+"\n")
ccsvo.close()




#cause I'm lazy and don't want to find why we have a subnet that matches the empty string
cidrs.pop('', None)

csvo = open('outfile.csv','w', newline='\n')
csvout = csv.writer(csvo,delimiter=",",quotechar='"',quoting=csv.QUOTE_MINIMAL)

with open('ip_to_hostname.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    headers = next(csvreader)
    headers.append('VRF')
    csvout.writerow(headers)
    for row in csvreader:
        ip = row[1]
        row.append(iptovrf(ip))
        csvout.writerow(row)
