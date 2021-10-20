# cos_project3(RECOS)

recos - 화장품 추천 서비스
django, mariadb, nginx, uwsgi, aws, celery, redis, vue.js

### API
화장품 리스트, 화장품 추천 리스트(이미지 업로드 api에서 자동 호출)   
회원 리스트, 마이 페이지   
Q&A 리스트, Q&A 작성, Q&A 수정,   
스크래핑(celery를 통한 스케줄링, db : redis, 메시지 브로커: redis)   
      
    
### 프로젝트 구성
> cos : 프로젝트 디렉토리(settings.py, celery.py)   
> app : 화장품 데이터 스크래핑 및 업로드(scraping.cos_scraping.py),     
           화장품 성분 이미지업로드(views.py), 화장품 추천(recommend.py)   
> common : 인증(회원가입(views.signup_views.py) 및 로그인/로그아웃), Q&A(views.qa_views.py)
         
          
### 인증(회원가입 및 로그인/ 로그아웃) - jwt
1. 세션 방식(Session Authentication)
2. 토큰 방식(Token Authentication, Json Web Token Authentication)
* 토큰 방식 중 JsonWebTokenAuthentication(jwt)를 사용한다. python과 Django에는 jwt에 대해서 python에는 PyJWT모듈이 있으며, Django의 rest_framework에는 simplejwt가 존재한다.
* rest_framework의 simplejwt를 이용

    > simplejwt 설치 및 settings.py 추가

        pip install djangorestframework-simplejwt

        # settings.py
        INSTALLED_APPS = [
            ...
            'rest_framework_simplejwt',
        ]
        
     > app/serializers.py

        # 기존 serializer 상속 후 수정. username이 response 값에 추가된다.
        class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
            def validate(self, attrs):
                data = super().validate(attrs)
                refresh = self.get_token(self.user)
                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)
                data['username'] = self.user.username
                return data
                
    > app/views/auth_views.py

        # return : {'access': 'accesstoken', 'refresh':'refreshtoken', 'username': 'username'}
        class MyTokenObtainPairView(TokenObtainPairView):
            serializer_class = MyTokenObtainPairSerializer


### 스크래핑 - requests_html, celery
   > worker 실행
   
    celery –A cos worker –l INFO –P eventlet     
   
   > beat 실행(스케줄링을 위한 beat)
   
    celery –A cos beat
    
* cos는 settings.py가 존재하는 cos 디렉토리를 의미한다.
* 현재로는 스크래핑의 스케줄링에 사용하지만, 추후 이미지를 업로드하고 화장품이 추려져 나오는 과정에서 비동기 작업 큐를 사용하여 추천 알고리즘이 진행되는 과정에서도 다른 작업을 할 수 있도록   추가할 예정
    
    
### 추천 알고리즘 - pytesseract, cv2, cosine similarity
* cosine similarity를 통해서 유사도가 제일 높은 10개를 순서대로 추출 후 반환
