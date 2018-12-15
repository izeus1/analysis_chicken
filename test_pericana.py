from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

#1페이지부터 114페이지까지 요청
for  in range(1, 115):
    request = Request("https://pelicana.co.kr/store/stroe_search.html?page=1&branch_name=&gu=&si=")

response = urlopen(request)
receive = response.read()
html = response.decode('utf-8', 'replace')

#print(html)

bs = BeautifulSoup(html, 'html.parser')
#print(bs.prettify())

divs = bs.findAll('div', attrs={'class':'tit3'})
print(divs)

for index, div in enumerate(divs): #인덱스 추출을 위해 enumerate 사용
    print(index+1, div.a.text, div.a['href'], sep=':')














