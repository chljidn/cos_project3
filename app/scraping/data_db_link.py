# redis에 저장된 화장품 세부 정보 데이터를 db에 연결하여 삽입하기 위한 api

# django에 연결된 캐시 서버 사용하기 위함
from django.core.cache import cache
# 세부 정보 데이터가 들어있는 캐시 서버 사용하기 위함
import redis
# 데이터 베이스 사용하기 위함
from app.models import Cos
# json으로 저장된 데이터들을 사용하기 위함
import json

cosmetic = cache.get_or_set('cosmetic', Cos.objects.value('prdname'))

redis4 = redis.StrictRedis(host='localhost', port=6379, db=4)
bulk_data = [] # bulk_insert 할 리스트
for i in range(redis4.dbsize()):
    cos_dict = redis4.get(str(i))
    if not cos_dict:
        continue

    cos_dict = dict(json.loads(cos_dict))
    if {'brand': cos_dict['name']} not in cosmetic: # 일단 이것만으로도 데이터 갯수만큼 순회.
       # 리스트에 모든 cos 객체 만들어서 한번에 insert 할 것.
        bulk_data.append(Cos(name=cos_dict['name'],
                             price = cos_dict['price'],
                             ingredient=cos_dict['ingredient'],
                             brand=cos_dict['brand']
                             ))                                            # 만약 데이터의 수가 많아지면 부담될 수 있음.
Cos.objects.bulk_creage(bulk_data)