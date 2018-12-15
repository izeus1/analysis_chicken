
from bs4 import BeautifulSoup

html='<td class="title">''<div class="tit3">''<a href="/movie/bi/mi/basic.nhn?code=171755" title="도어락">도어락</a>''</div></td>'


def ex1():
    bs = BeautifulSoup(html, 'html.parser')
    print(bs)

    tag = bs.td
    print(tag)

if __name__ == '__mail__':
    ex1()

def ex2():
    bs = BeautifulSoup(html, 'html.parser')

    tag = bs.td


