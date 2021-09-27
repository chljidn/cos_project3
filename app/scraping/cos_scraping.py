# html parser api
import urllib.request
import re
from requests_html import HTMLSession, AsyncHTMLSession
from bs4 import BeautifulSoup as bs
import redis

# 데이터 베이스와 캐시 연결(데이터베이스에서 화장품 데이터 가져오기 위함)
from django.core.cache import cache
from app.models import Cos

import asyncio
import logging


class scraping:
    cosmetic = cache.get_or_set('cosmetic', Cos.objects.values('prdname'))

    def __init__(self, idx):
        self.redis3 = redis.StrictRedis(host='127.0.0.1', port=6379, db=3)  # 상세 페이지 html 가져오기 위함
        self.redis4 = redis.StrictRedis(host='localhost', port=6379, db=4)  # 각 상품 딕셔너리 저장하기 위함
        self.idx = idx  # 입력 받은 idx부터 시작할 수 있도록 함
        lobs_html = self.lobs()
        self.preprocessing()

    # 페이지에서 href 링크 모두 뽑아내기
    def get_links(self, html):
        webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
        return webpage_regex.findall(html)

    # 페이지에서 전성분 모두 뽑아내기 - 전성분은 화장품의 성분들 의미
    def get_ingredient(self, html):
        webpage_regex = re.findall('전성분</dt>(.*?)</dd>{1}', html)  # </dd>가 한번 나올 때까지만 찾기
        return webpage_regex

    def detailed_page(self, url):
        # 새 이벤트 루프 생성
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)

        session = HTMLSession()
        # logging.basicConfig(filename='recos_scraper.log', level=logging.DEBUG)
        r = session.get(url)
        r.html.render(scrolldown=3, timeout=20)
        session.close()
        return r

    # async def detailed_page(self, url):
    #    new_loop = asyncio.new_event_loop()
    #    asyncio.set_event_loop(new_loop)

    #   asession = AsyncHTMLSession()

    # browser = await pyppeteer.launch({
    #    'ignoreHTTPSErrors': True,
    #    'headless': True,
    #    'handleSIGINT': False,
    #    'handleSIGTERM': False,
    #    'handleSIGHUP': False
    # })
    # asession._browser = browser

    #    r = await asession.get(url)
    #    await r.html.arender(scrolldown=3, timeout=20)
    #    await asession.close()
    #    return r

    def lobs(self):

        # xhr로 넘어오는 상품들의 html을 가져온다.
        # html에서 get_links 함수를 통해서 href 링크들을 모두 가져온다(넘어온 xhr은 상품들에 관한 정보만 있으므로 링크들은 모두 상품들의 상세페이지 링크)
        total_link = []
        start_idx = self.idx  # 밑에서 enumerate 돌 때, key로 사용할 시작점으로 사용하기 위함.

        while True:
            url = f'https://www.lotteon.com/search/render/render.ecn?&u2={self.idx}&u3=60&u9=navigateProduct&render=nqapi&platform=pc&collection_id=401&login=Y&u4=lb10100005'
            main_html = urllib.request.urlopen(url).read().decode('utf-8')
            link_list = self.get_links(main_html)

            # 가져올 링크가 하나도 없으면 while문 break
            if link_list == []:
                break
            total_link.extend(link_list)

            self.idx += 60

        # 링크 뽑아내는 과정에서 같은 상세페이지가 두번씩 추가되므로, 중복 없애기 위해 set 사용
        for j, i in enumerate(set(total_link), start=start_idx):
            print(f'{j}번 째 상품 진행 중...')

            # 예외처리
            try:
                res = self.detailed_page(i)

                # loop = asyncio.get_event_loop()
                # asyncio.set_event_loop(loop)
                # res = loop.run_until_complete(self.detailed_page(i))
                # loop.close()
                # res = asyncio.run(self.detailed_page(i))
            except Exception as e:  # 예외 발생할 경우, 에러 이름 출력하고 다음 for문 부터 출력
                print(j, '번에서', e, '발생')
                continue

            # redis 서버에 html을 문자열로 바꾼 후 캐싱하기.
            # html 파일 객체로 담을 수는 없는지 찾아볼 것.
            self.redis3.set(str(j), str(res.html.html))  # 전체 html 캐싱

    def preprocessing(self):
        bulk_data = []
        for i in range(self.redis3.dbsize()):  # dbsize = redis의 해당 데이터베이스에 담긴 데이터 개수
            b = self.redis3.get(str(i))
            # 데이터가 담기지 않은 부분을 제외하기 위함
            # 예외가 발생하거나, 아예 html이 없는 경우 캐싱된 파일이 없을 수 있으므로 이 경우는 그냥 continue로 넘어간다.
            if not b: continue

            b = b.decode()  # 캐시에 저장될 때, 바이트로 타입으로 저장되므로 가져와서 다시 str로 인코딩
            c = self.get_ingredient(b)
            bb = bs(b, 'html.parser')  # beautifulsoup(name, price, brand 뽑아내기 위함)

            # 전성분이 없을 경우 continue
            if c == []: continue

            # 성분 : c[0].replace('<dd data-v-2902b98c="">', '').strip(" ")
            # 가격 : bb.find_all('span', class_='won')[0].text.strip()
            # 이름 : bb.find('div', class_='productName').text.strip()
            # 브랜드 : bb.find('strong').text.strip()
            cos_dict = {
                'name': bb.find('div', class_='productName').text.strip(),
                'price': bb.find_all('span', class_='won')[0].text.strip(),
                'ingredient': c[0].replace('<dd data-v-2902b98c="">', '').strip(" "),
                'brand': bb.find('strong').text.strip(),
                'image': bb.find_all('img', alt=bb.find('div', class_='productName').text.strip())[0]['src'],
            }

            # 같은 이름의 화장품이 데이터베이스 내에 있는지 확인
            # 없을 경우 bulk_data 리스트에 Cos모델 객체 추가
            if {'prdname': cos_dict['name']} not in scraping.cosmetic:
                bulk_data.append(Cos(prdname=cos_dict['name'],
                                     price=cos_dict['price'],
                                     ingredient=cos_dict['ingredient'],
                                     brand=cos_dict['brand'],
                                     image=cos_dict['image']
                                     ))
        Cos.objects.bulk_create(bulk_data)
