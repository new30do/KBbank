from django.shortcuts import render

# Create your views here.

def play(request):
    return render(request, 'play.html')

def main(request):
    return render(request, 'index.html')

from selenium import webdriver
from time import sleep
#자동화로 인터넷 등기소 검색
def search(request):
    driver = webdriver.Chrome('/Users/kang/PycharmProjects/kbBank/chromedriver2')
    #driver.get('http://www.iros.go.kr/frontservlet?cmd=RISUWelcomeViewC')
    driver.get('http://www.iros.go.kr/PMainJ.jsp')
    sleep(3.0)
    driver.find_element_by_xpath('//*[@id="cenS"]/div/ul/li[1]/div/ul/li[1]/a/strong').click()
    sleep(3.0)
    driver.find_element_by_name('txt_simple_address').send_keys('서울시 영등포구 당산로 20길 5-1')
    sleep(3.0)
    driver.find_element_by_xpath('//*[@id="btnSrchSojae"]').click()
    return

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from bs4 import BeautifulSoup


def makeHtml(): #html 파일생성
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


def calLoan(): # 채권채고액 합산
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

def ownerName(): #실소유주 확인
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