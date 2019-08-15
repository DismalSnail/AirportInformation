import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver

airportInfoList = []

siteURL = "https://airportcode.51240.com"


def getAirportInfo(PageURL, page):  # 获取每个页面的机场列表
    try:
        browser = webdriver.PhantomJS(executable_path=r'C:\phantomjs\bin\phantomjs')
        response = requests.get(PageURL)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        tag_as = soup.table.table.find_all('a')
        length = str(len(tag_as))
        i = 1
        for tag_a in tag_as:
            airportDetailURL = siteURL + tag_a.attrs['href']
            print("第：" + str(page) + "/30 个页面的第：" + str(i) + "/" + length + "个机场")
            getAirportDetailInfo(airportDetailURL, browser)
            i = i + 1
        browser.quit()
    except:
        print("从 " + PageURL + "获取数据失败")
        browser.quit()
        return 0


def getAirportDetailInfo(airportDetailURL, browser):  # 从获取的机场列表中获取每个机场的详细信息
    try:
        time.sleep(3)
        browser.get(airportDetailURL)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        tag_trs = soup.table.table.find_all('tr')
        airportInfoDict = {}
        for tr in tag_trs:
            airportInfoDict[tr.td.string] = tr.td.next_sibling.next_sibling.span.string

        airportInfoList.append(airportInfoDict)
    except:
        print("从 " + airportDetailURL + "获取数据失败")
        return 0


def writeInfoToFile(infoFilepath):
    with open(infoFilepath, 'w+', encoding='utf-8') as infoFile:
        infoFile.write(json.dumps(airportInfoList, ensure_ascii=False))


def main():  # 读取机场URL文件，获取机场列表
    infoFilePath = "test.json"
    page = 1
    with open("test.txt", 'r') as AirportFile:
        for PageURL in AirportFile:
            print("第:" + str(page) + "/30 个页面")
            getAirportInfo(PageURL, page)
            page = page + 1

    writeInfoToFile(infoFilePath)


if __name__ == '__main__':
    main()
