from pprint import pprint
import PyPDF2
import ipaddress
import csv
import re
import socket

#to hold all of our cidrs
cidrs = {}


#look up ip in cidrs to determine vrf
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

#regex to match on "good" lines
good = re.compile("^([a-zA-z0-9-])+:.*")

#file to write debug info to
debug = open('debug.txt','w',newline='\n')

#cause you never not start at 0 for an incrementer
i = 0

#some intial values for vars that we need to span iteterations of the below for loop
getnets = False
vrfname = ''
#iterate over the PDF and create a "dictionary" mapping subnet to vrfname
for i in range(pages):
    pageObj = pdfReader.getPage(i)
    pagetxt = (pageObj.extractText()).split('\n')
    if( not getnets):
        vrfname = pagetxt[1]

    for line in pagetxt:
        if( (line.startswith('--') or line.startswith("        CUSTOM") or line.startswith('Page') or line == '')):
            debug.write("Cont: %s\n" %line)
            continue
        elif(getnets and not good.match(line)):
            debug.write("False %s\n" %line)
            vrfname = pagetxt[1]
            getnets = False
        elif(getnets and good.match(line)):
            debug.write("Cidr: %s\n" %line)
            cidr = (line.split(' '))[2]
            cidrs[cidr] = vrfname
        elif(line == 'Router SVIs Found:'):
            debug.write("True %s\n" %line)
            getnets = True
        else:
            debug.write("Other %s\n" %line)

#close debug file
debug.close()

#close the pdf
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
    headers.append('Hostname')
    csvout.writerow(headers)
    for row in csvreader:
        ip = row[1]
        hostname = ''
        try:
            hostname = (socket.gethostbyaddr(ip))[0]
        except:
            hostname = 'NotFound'
        row.append(iptovrf(ip))
        row.append(hostname)
        csvout.writerow(row)
