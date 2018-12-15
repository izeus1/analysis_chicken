import ssl
import time

import pandas as pd

from datetime import datetime
from itertools import count
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib3.util import url

RESULT_DIRECTORY = "__result__"

def crawling_kyochon():
    results = []

    for sido1 in range(1, 18):
        for sido2 in count(start=1):
            try:
                url = "http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=" % (sido1, sido2)
                req = Request(url)
                resp = urlopen(req)

                receive = resp.read() #바이트
                html = receive.decode('utf-8')

                # log
                print('%s : success for request [%s]' % (datetime.now(), url))
                bs = BeautifulSoup(html, 'html.parser')
                tag_ul = bs.find("ul", attrs={'class':'list'})

                for tag_span in tag_ul.findAll("span", attrs={'class':'store_item'}):
                    name = tag_span.find('strong').text
                    address = tag_span.find('em').get_text().strip().split('\r')[0]
                    sidogu = address.split()[:2]
                    # print(address)
                    # print(tag_span)

                    results.append((name, address) + tuple(sidogu))

                #print(html)
            except Exception as e:
                print('%s : %s ' % (datetime.now(), e))
                break

        print(len(results))
        print(results)

    #store
        table = pd.DataFrame(results, columns=['name', 'adress', 'sido', 'gungu'])
        table.to_csv(
            '{0}/kyochon_table.csv'.format(RESULT_DIRECTORY),
            encoding='utf-8',
            mode='w',
            index=True)


def crawling_pelicana():
    results =[]
    for page in count(start=1):
    # for page in range(1, 2):
        url = "https://pelicana.co.kr/store/stroe_search.html?page=%d" % page
        req = Request(url)
        resp = urlopen(req, context=ssl._create_unverified_context())

        receive = resp.read() #바이트
        # UnicodeDecodeError - > 'replace'
        html = receive.decode('utf-8', 'replace')
        #print(html)

        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class': 'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        #끝 검출
        if len(tags_tr) == 0:
            break

        #로그
        print('%s : success for request [%s]' % (datetime.now(), url))

        for tag_tr in tags_tr:
            #테이블 데이터는 아래와 같이 처리
            # print(tag_tr.strings)
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[3]
            sidogu = address.split()[:2]
            print(sidogu)

            results.append((name, address) + tuple(sidogu))

            #store(적재)
            table = pd.DataFrame(results, columns=['name', 'adress', 'sido', 'gungu'])
            table.to_csv(
                '{0}/pelicana_table.csv'.format(RESULT_DIRECTORY),
                encoding='utf-8',
                mode='w',
                index=True)


            # print(len(result))
            # print(result)

def crawling_nene():
    results =[]
    prepage_first_shopname=''
    for page in range(1, 3):
    # for page in count(start=1):
        url = "https://nenechicken.com/17_new/sub_shop01.asp?page=%d" % page
        req = Request(url)
        resp = urlopen(req, context=ssl._create_unverified_context())

        receive = resp.read() #바이트
        # UnicodeDecodeError - > 'replace'
        html = receive.decode('utf-8', 'replace')
        #print(html)

        bs = BeautifulSoup(html, 'html.parser')
        tags_table = bs.findAll('table', attrs={'class':'shopTable'})
        print(len(tags_table)) # 정상적인 길이값인지 확인!

        is_end = False

        for index, tag_table in enumerate(tags_table):
            name = tag_table.find('div', attrs={'class':'shopName'}).text
            address = tag_table.find('div', attrs={'class':'shopAdd'}).text
            sidogu = address.split()[:2]
            print(name, address)

        # 끝 검출
        if index == 0:
            if prepage_first_shopname == name:
                is_end = True
                break
            else:
                prepage_first_shopname = name
        results.append((name, address) + tuple(sidogu))

        if is_end is True:
            break

        #로그
        print('%s : success for request [%s]' % (datetime.now(), url))
    #store
        table = pd.DataFrame(results, columns=['name', 'adress', 'sido', 'gungu'])
        table.to_csv(
            '{0}/nene_table.csv'.format(RESULT_DIRECTORY),
            encoding='utf-8',
            mode='w',
            index=True)

def crawling_goobne():
    results = []
    url = "https://www.goobne.co.kr/store/search_store.jsp"

    # 첫 페이지 로딩
    wd = webdriver.Chrome('/JAVA_BIGDATA/chromedriver_win32/chromedriver.exe')
    wd.get(url)
    time.sleep(3)

    for page in count(start=1):
    # for page in range(102, 104):
        results = []
        # 자바 스크립트 실행
        script = "store.getList(%d)" % page
        wd.execute_script(script)
        #로그
        print('%s : success for script execute [%s]' % (datetime.now(), script))
        time.sleep(3)

        # 실행 결과 HTML(rendering된 HTML) 가져오기
        html = wd.page_source
        # print(html)

        #bs4를 사용해서 파싱
        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id':'store_list'})
        # print(tag_tbody)
        tags_tr = tag_tbody.findAll('tr')

        #마지막 검출
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            # print(strings): 확인용
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]

            results.append((name, address) + tuple(sidogu))

    # print(results)

    #로그
    print('%s : success for request [%s]' % (datetime.now(), url))
    #store
    table = pd.DataFrame(results, columns=['name', 'adress', 'sido', 'gungu'])
    table.to_csv(
        '{0}/gubne_table.csv'.format(RESULT_DIRECTORY),
        encoding='utf-8',
        mode='w',
        index=True)


def crawling_blade_soul():
    results = []

    # for page in count(start=1):
    for page in range(1, 2):
        try:
            # for line in count(start=1):
            # try:
            url = "http://bns.plaync.com/board/server/article?p=%d&cn=kkjs" % page
            req = Request(url)
            resp = urlopen(req)

            receive = resp.read() #바이트
            html = receive.decode('utf-8')

            # log
            print('%s : success for request [%s]' % (datetime.now(), url))
            bs = BeautifulSoup(html, 'html.parser')
            tags_strong = bs.findAll("strong", attrs={'class':'title'})

            for tag in tags_strong:
                summary = tag.a.text
                print(summary)
                results.append([summary])

            print(results)
        except Exception as e:
            print('%s : %s ' % (datetime.now(), e))
            break

    #store
        table = pd.DataFrame(results, columns=['summary'])
        table.to_csv(
            '{0}/blade_soul_table.csv'.format(RESULT_DIRECTORY),
            encoding='utf-8',
            mode='w',
            index=True)



if __name__=='__main__':
    #pelicana
    # crawling_pelicana()

    #nene
    # crawling_nene()

    #kyochon
    # crawling_kyochon()

    #goobne
    # crawling_goobne()

    #bhc

    #블레이드앤소울
    crawling_blade_soul()