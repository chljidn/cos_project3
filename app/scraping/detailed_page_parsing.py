# 제품 별 상세 페이지 parsing

# 데이터 전처리 api
import redis
from bs4 import BeautifulSoup as bs
import re

# redis에 딕셔너리를 json 타입으로 저장하기 위함
import json

# 페이지에서 전성분부터 </dd>까지 뽑기
# 성분 뽑아내기 위한 함수
def get_ingredient(html):
    webpage_regex = re.findall('전성분</dt>(.*?)</dd>{1}', html) # </dd>가 한번 나올 때까지만 찾기
    return webpage_regex

redis3 = redis.StrictRedis(host='localhost', port=6379, db=3) # 각 상품의 상세 페이지 html이 저장된 redis 3번 db 객체
redis4 = redis.StrictRedis(host='localhost', port=6379, db=4) # 각 상품의 name, price, brand, ingerdient 딕셔너리 저장할 redis 4번 db

for i in range(redis3.dbsize()): # dbsize = redis의 해당 데이터베이스에 담긴 데이터 개수
    b = redis.get(str(i))
    # key는 있으나 데이터가 담기지 않은 부분을 제외하기 위함
    if not b:
        continue

    b = b.decode() # 캐시에 저장될 때, 바이트로 타입으로 저장되므로 가져와서 다시 str로 인코딩
    c = get_ingredient(b)
    bb = bs(b, 'html.parser')  # beautifulsoup(name, price, brand 뽑아내기 위함)

    # 전성분이 없을 경우 continue
    if c == []: continue

    # 성분 : c[0].replace('<dd data-v-2902b98c="">', '').strip(" ")
    # 가격 : bb.find_all('span', class_='won')[0].text.strip() # 가격 부분은 beautifulsoup로 html parse 한 후에 태크로 뽑아냄
    # 이름 : bb.find('div', class_='productName').text.strip()
    # 브랜드 : bb.find('strong').text.strip()
    d = {'name': bb.find('div', class_='productName').text.strip(),
         'price':bb.find_all('span', class_='won')[0].text.strip(),
         'ingredient': c[0].replace('<dd data-v-2902b98c="">', '').strip(" "),
         'brand' : bb.find('strong').text.strip()
        }

    d = json.dumps(d, eusure_ascii=False).encode('utf-8')
    redis4.set(str(i), d)