# import time
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import re
# from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from selenium import webdriver
import pymysql

makeDict = dict()
top_code_list = list()
tag_list = ''

SERVER = pymysql.connect(
    host='192.168.0.21',
    user='',
    password='',
    db='',
    charset='utf8'
)


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


def makeCodeName():  # 타이틀 한글코드 추출
    global top_code_list
    global tag_list
    if tag_list:
        fisrst_titles = tag_list.select('body > ul > li > div.list.selected > a')
        second_titles = tag_list.select('body > ul > li > ul > li > div.list > a')
        third_titles = tag_list.select('body > ul > li > ul > li > ul > li > div.list > a')
        fourth_titles = tag_list.select('body > ul > li > ul > li > ul > li > ul > li > div.list > a')
        datas = [fisrst_titles, second_titles, third_titles, fourth_titles]
        for data in datas:
            for title in data:
                top_code_list.append((title.parent.parent.attrs['id'], title.text))

        sql = """INSERT IGNORE INTO drug_kpic_code_titles(code_index, code_name_kor) VALUES (%s, %s)"""
        insertDataToServer(sql, top_code_list)
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


def makeCodeData():  # 데이터 한글 코드 추출
    global tag_list
    data_code_list = list()
    if tag_list:
        dep3_datas = tag_list.select('body > ul > li > ul > li > ul > li > ul > li > a')
        dep4_datas = tag_list.select('body > ul > li > ul > li > ul > li > ul > li > ul > li > a')

        datas = [dep3_datas, dep4_datas]
        for data in datas:
            for title in data:
                keyCode = title.parent.parent.attrs['id']
                if keyCode and title.text:
                    data_code_list.append((keyCode[2:], title.text))

        sql = """INSERT IGNORE INTO drug_kpic_code_data(code_index, data_name_kor) VALUES (%s, %s)"""
        insertDataToServer(sql, data_code_list)
    else:
        print('비었음 makeCodeData tag_list')


def insertDataToServer(sql, input_data):
    tempData = input_data
    if len(tempData) > 0:
        try:
            insert_sql = sql
            CURSOR = SERVER.cursor(pymysql.cursors.DictCursor)
            CURSOR.executemany(insert_sql, tempData)
            SERVER.commit()
        except InterruptedError:
            pass
        except SERVER.IntegrityError as err:
            SERVER.rollback()
            print("입력 실패, 중복 코드는 입력이 허용되지 않습니다.")
            print(err)
        finally:
            print("DB 접속을 종료 합니다")
            SERVER.close()
    else:
        print("원본 데이터가 비어 있습니다")


try:

    # local로 받아온 파일을 대상으로 처리
    page = open('D:\\PycharmProjects\\pythonProject\\yahyo.html', 'r', encoding='UTF8')
    soup = BeautifulSoup(page, 'html5lib')  # html5lib ,  lxml
    tag_list = soup.find('ul', class_='depth01')

    #makeCodeName()
    #makeCodeData()

    # makeCodeName()  # 코드네임표 만들기
    # charList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Z']
    # for charX in charList:  # 크롤링 시작
    #     makeBodyCollection(charX)
    #
    # print(makeDict)

finally:
    # print(top_code_list)
    print('END')
