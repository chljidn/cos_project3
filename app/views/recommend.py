# Cos 모델 설치
from app.models import Cos

# cache server
from django.core.cache import cache

# 성분추출함수에 쓰일 패키지 설치
from PIL import Image, ImageFont, ImageDraw
from pytesseract import *
import pandas as pd

# 코사인 유사도에 쓰일 패키지
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

class recommend:
    # 글자 추출 함수(코사인 유사도를 위해 공백과 ,등 제거)
    def cross(self, arg): # 사진 파일의 위치를 매개변수로 받음
        #pytesseract.tesseractc_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
        os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/4.00/tessdata/'
        image = Image.open(arg)

        x = int(1920 / image.size[0])
        y = int(1080 / image.size[1])

        if x != 0:
            if y != 0:
                if x > y:
                    image = image.resize((image.size[0] * y, image.size[1] * y))
                else:
                    image = image.resize((image.size[0] * x, image.size[1] * x))

        text = image_to_string(image, lang="kor")

        add = ""
        for i in range(len(text.split("\n"))):  # 추출한 글자들에서 \n을 기준으로 나누기. 즉, 한 줄 단위로 나누기.
            add = add + (text.split("\n")[i])  # 줄 단위로 끊어졌기 때문에 한 단어이지만 나누어진게 있을수 있으므로 다시 줄단위로 끊은 것들을 합치기.
        add2 = []
        for i in range(len(add.split(","))):  # 단어들을 다시 , 단위로 나누기
            add2.append(add.split(",")[i])  # 리스트인 add2에 , 기준으로 나눈 단어들을 넣기. 리스트이 하나의 엘리먼트는 하나의 단어가 됨.
        for i in range(len(add2)):
            add2[i] = add2[i].strip()  # 리스트의 각 단어(엘리먼트)들의 앞, 뒤쪽의 공백 없애기

        fflist = ""  # 문자변수 fflist 생성
        add3 = ""  # 문자변수 add3 생성
        add3 = ''.join(add2)
        fflist = add3[0:len(add3) - 2]  # 글자 사이에 공백이나 기호 없도록 fflist 변수에 합하기.

        return fflist


    def cosine(self, fflist):
        data = pd.read_csv("static/cos5.txt", header=None)

        def jaccard_similarity(self, doc1, doc2):
            doc1 = set(doc1)
            doc2 = set(doc2)
            return len(doc1 & doc2) / len(doc1 | doc2)

        listtt = []
        for i in range(len(fflist.split(" "))):
            for j in range(len(fflist.split(" ")[i].split(","))):
                listtt.append(fflist.split(" ")[i].split(",")[j])
        listtt = [v for v in listtt if v]

        list2 = []
        for i in range(len(listtt)):
            list = []
            for j in range(len(data[0])):
                test = jaccard_similarity(data[0][j], listtt[i])
                if test > 0.3:
                    list.append((test, data[0][j]))
            list.sort(reverse=True)
            if len(list) != 0:
                list2.append(list[0][1])

        # 화장품 전체 데이터가 cache 서버에 있는지 확인하고 없는 경우 넣어주고, 있을 경우 cache 서버에서 가져오기
        cos_cache = cache.get_or_set('cos_cache', Cos.objects.values())
        cos = pd.DataFrame(cos_cache)

        list2 = ', '.join(list2)
        ffflist = []
        for i in range(len(cos)):
            sent = (cos['주요성분'][i], fflist)
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(sent)  # 문장 벡터화 진행
            idf = tfidf_vectorizer.idf_

            cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])  # 첫번째와 두번째 문장 비교
            ffflist.append((float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])))

        recommend = cos[["prdname", "brand", "price", "category", "link", "pagelink"]]

        indexlist = []

        for i in range(6):
            del ffflist[ffflist.index(max(ffflist))]
            indexlist.append(int(ffflist.index(max(ffflist))))

        recommend = recommend.iloc[indexlist]
        recommend = recommend.reset_index()
        print('recommend:', recommend)

        column = ['link{}', 'pagelink{}', 'prdname{}', 'brand{}', 'category{}', 'price{}']
        data_column = ['link', 'pagelink', 'prdname', 'brand', 'category', 'price']

        for i in range(6):
            for j in range(6):
                globals()[(column[j]).format(i)] = cos[(data_column[j])][i]
                #print(globals()[(column[j]).format(i)])




