
from bs4 import BeautifulSoup

html='<td class="title">''<div class="tit3">''<a href="/movie/bi/mi/basic.nhn?code=171755" title="도어락">도어락</a>''</div></td>'

tags = bs.findAll('div', attrs={'class':'tit3'})
print(tags)

