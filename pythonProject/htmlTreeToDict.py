# import time
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# import re
# from selenium.webdriver.common.by import By

makeDict = dict()
top_code_list = dict()
tag_list = ''


def nodeMaker(key, value):  # 키 노드를 만든다

    global makeDict
    try:
        if str(key) not in makeDict:
            if len(key) == 1:
                makeDict[key] = dict()
            elif len(key) == 3:
                makeDict[key[:1]][key] = dict()
            elif len(key) == 4:
                makeDict[key[:1]][key[:3]][key] = dict()
            elif len(key) == 5:
                if type(makeDict[key[:1]][key[:3]][key[:4]]) is list:
                    makeDict[key[:1]][key[:3]][key[:4]].append({key: [value]})
                else:
                    makeDict[key[:1]][key[:3]][key[:4]][key] = dict()
                    # print(type(makeDict[key[:1]][key[:3]][key[:4]]), '/=>', key)
            elif len(key) == 6:
                print('number 6 ?')
    finally:
        print('')


def makeCodeName():  # 코드 한글 변환 콜렉션을 만든다.
    global top_code_list
    global tag_list
    if tag_list:
        fisrst_titles = tag_list.select('body > ul > li > div.list.selected > a')
        second_titles = tag_list.select('body > ul > li > ul > li > div.list > a')
        third_titles = tag_list.select('body > ul > li > ul > li > ul > li > div.list > a')
        fourth_titles = tag_list.select('body > ul > li > ul > li > ul > li > ul > li > div.list > a')

        if fisrst_titles:
            for title in fisrst_titles:
                top_code_list[title.parent.parent.attrs['id']] = title.text
        else:
            print('비었음 fisrst_titles')

        if second_titles:
            for title2 in second_titles:
                top_code_list[title2.parent.parent.attrs['id']] = title2.text
        else:
            print('비었음 second_titles')

        if third_titles:
            for title3 in third_titles:
                top_code_list[title3.parent.parent.attrs['id']] = title3.text
        else:
            print('비었음 third_titles')

        if fourth_titles:
            for title4 in fourth_titles:
                top_code_list[title4.parent.parent.attrs['id']] = title4.text
        else:
            print('비었음 fourth_titles')
    else:
        print('비었음 tag_list')


def makeBodyCollection(keyChar):  # 데이터 콜렉션을 만든다

    global tag_list
    second_titles = tag_list.select('li[id^="' + keyChar + '"]')

    if second_titles:
        for (index, title) in enumerate(second_titles):
            key = title.attrs['id']
            value = title.select_one('div.list > a').text
            nodeMaker(key, value)
            sub = title.select('ul[id^="ul' + key + '"] > li:not([id]) > a')

            if sub:
                for st in sub:
                    s_key = st.parent.parent.attrs['id'][2:]
                    s_value = st.text
                    if key == s_key:
                        if len(key) == 4:
                            if makeDict[key[:1]][key[:3]][s_key]:
                                makeDict[key[:1]][key[:3]][s_key].append(s_value)
                            else:
                                makeDict[key[:1]][key[:3]][s_key] = list()
                                makeDict[key[:1]][key[:3]][s_key].append(s_value)
                        elif len(key) == 5:
                            if type(makeDict[key[:1]][key[:3]][key[:4]]) is list:
                                for (i, test) in enumerate(makeDict[key[:1]][key[:3]][key[:4]]):
                                    if s_key in test:
                                        makeDict[key[:1]][key[:3]][key[:4]][i][s_key].append(s_value)
                            else:
                                if makeDict[key[:1]][key[:3]][key[:4]][s_key]:
                                    makeDict[key[:1]][key[:3]][key[:4]][s_key].append(s_value)
                                else:
                                    makeDict[key[:1]][key[:3]][key[:4]][s_key] = list()
                                    makeDict[key[:1]][key[:3]][key[:4]][s_key].append(s_value)
            else:
                print('비었음 2')
    else:
        print('비었음 1')


try:

    # local로 받아온 파일을 대상으로 처리
    page = open('D:\\PycharmProjects\\pythonProject\\yahyo.html', 'r', encoding='UTF8')
    soup = BeautifulSoup(page, 'html5lib')  # html5lib ,  lxml
    tag_list = soup.find('ul', class_='depth01')
    makeCodeName()  # 코드네임표 만들기

    charList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Z']
    for charX in charList:  # 크롤링 시작
        makeBodyCollection(charX)

    print(makeDict)

finally:
    # print(top_code_list)
    print('END')
