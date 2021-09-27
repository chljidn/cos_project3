# 상세 페이지들의 링크를 파싱하기 위한 api

import urllib.request
import re
from requests_html import HTMLSession
import redis
import logging


# 페이지에서 href 링크 모두 뽑아내기
def get_links(html):
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    return webpage_regex.findall(html)

# 페이지에서 전성분부터 </dd>까지 뽑기
def get_ingredient(html):
    webpage_regex = re.findall('전성분</dt>(.*)</dd>{1}', html) # </dd>가 한번 나올 때까지만 찾기
    return webpage_regex



def ingredient_confirm(bs_object):
    for i in bs_object.find_all('dt'):
        if '전성분' in i:
            return True
    return False


class scraping:
    def __init__(self, idx):
        self.idx = idx #입력 받은 idx부터 시작할 수 있도록 함
        self.lobs()

    def detailed_page(self, url):
        session = HTMLSession()
        #logging.basicConfig(filename='recos_scraper.log', level=logging.DEBUG)
        r = session.get(url)
        # timeout = 서버에서 데이터를 보낼 때까지 기다리는 시간.
        # timeout 안 걸면 에러
        # sleep = Integer, if provided, of how many seconds to sleep after initial render.
        # (sleep n초가 제공되면 렌더링은 반환되기 전에 n초를 기다린다)
        r.html.render(scrolldown=3, timeout=20)
        session.close()
        return r

    # 후에 idx 입력 받게 만들어서 멈춘 지점부터 시작할 수 있도록 할 것.
    def lobs(self):

        # redis
        rd = redis.StrictRedis(host='localhost', port=6379, db=3)

        # xhr로 넘어오는 상품들의 html을 가져온다.
        # html에서 get_links 함수를 통해서 href 링크들을 모두 가져온다(넘어온 xhr은 상품들에 관한 정보만 있으므로 링크들은 모두 상품들의 상세페이지 링크임)
        total_link = []
        start_idx = self.idx # 밑에서 enumerate 돌 때, key로 사용할 시작점으로 사용하기 위함.

        while True:
            url = f'https://www.lotteon.com/search/render/render.ecn?&u2={self.idx}&u3=60&u9=navigateProduct&render=nqapi&platform=pc&collection_id=401&login=Y&u4=lb10100005'
            main_html = urllib.request.urlopen(url).read().decode('utf-8')
            link_list = get_links(main_html)

            # 가져올 링크가 하나도 없으면 while문 break
            if link_list == []:
                break
            total_link.extend(link_list)

            self.idx += 60

        # 링크 뽑아내는 과정에서 같은 상세페이지가 두번씩 추가되므로, 중복 없애기 위해 set 사용
        for j, i in enumerate(set(total_link), start = start_idx):
            print(f'{j}번 째 상품 진행 중...')
            res = self.detailed_page(i)

            # redis 서버에 html을 문자열로 바꾼 후 캐싱하기.
            # html 파일 객체로 담을 수는 없는지 찾아볼 것.
            rd.set(str(j), str(res.html.html)) # 전체 html 캐싱

            #html_bs = bs(res.html.html)
            #if ingredient_confirm(html_bs) == True:
                #ab = get_in
            # gredient(res.html.html)
                #rd.set(str(j), str(ab))



# 예외처리 하여 자동으로 다시 시작할 수 있도록 수정 요망
d = scraping(1)
