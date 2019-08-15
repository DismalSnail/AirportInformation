from bs4 import BeautifulSoup

from selenium import webdriver
#打开一个浏览器
browser = webdriver.PhantomJS(executable_path=r'C:\ProgramData\Anaconda3\chromedriver.exe')
#准备一个网址
urls = ['https://airportcode.51240.com/','https://phantomjs.org/download.html']

for url in urls:
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    print(soup.prettify())
    print("*********************************************************************************************************************")

browser.quit()

