from django.shortcuts import render

# Create your views here.

def play(request):
    return render(request, 'play.html')

def main(request):
    return render(request, 'index.html')

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from bs4 import BeautifulSoup


def makeHtml():
    path = "/Users/kang/PycharmProjects/KB/prop.pdf"
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    f = open('./out.html', 'wb')
    device = HTMLConverter(rsrcmgr, f, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0  # is for all
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    f.close()
    return


def calLoan():
    totalAmt = 0
    with open('/Users/kang/PycharmProjects/KB/out.html') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        all_divs = soup.select("div > span")
        for amt in all_divs:
            if "채권최고액" in amt.text:
                atrAmtArray = amt.text.split(" ")
                loanStr = atrAmtArray[4].split("\n")[0]
                loanAmt = loanStr[1:-1]
                loanAmt = int(loanAmt.replace(',', ''))
                totalAmt += loanAmt
    return totalAmt

def ownerName():
    owner = ""
    ownerNumber = ""
    with open('/Users/kang/PycharmProjects/KB/out.html') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        all_divs = soup.select("div > span")
        for name in all_divs:
            if "소유자" in name.text:
                nameArray = name.text.split(" ")
                owner = nameArray[2]
                ownerNumber = nameArray[4].replace("\n",'')

    return (owner+" "+ownerNumber)