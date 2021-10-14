# cos_project3(RECOS)

recos - 화장품 추천 서비스
django, mariadb, nginx, uwsgi, aws, celery, redis, vue.js

### API
화장품 리스트, 화장품 추천 리스트(이미지 업로드 api에서 자동 호출)
회원 리스트, 마이 페이지
Q&A 리스트, Q&A 작성, Q&A 수정
스크래핑(celery를 통한 스케줄링, db : redis, 메시지 브로커: redis)
      

### 프로젝트 구성
> cos : 프로젝트 디렉토리(settings.py, celery.py)   
> app : 화장품 데이터 스크래핑 및 업로드(scraping.cos_scraping.py),     
           화장품 성분 이미지업로드(views.py), 화장품 추천(recommend.py)   
> common : 인증(회원가입(views.signup_views.py) 및 로그인/로그아웃), Q&A(views.qa_views.py)
             
### 인증(회원가입 및 로그인/ 로그아웃) - jwt
1. 세션 방식(Session Authentication)
2. 토큰 방식(Token Authentication, Json Web Token Authentication)
* 토큰 방식 중 JsonWebTokenAuthentication(jwt)를 사용한다. rest_framework의 프레임 워크 중에 simplejwt를 이용
* 다만 TokenAuthentication을 사용할 경우, ObtainAuthToken을 상속받아 사용하면 view에서 사용이 가능하다. jwt의 경우 view가 url에서 바로 매칭되는 형식으로 나와있기 때문에 view에서 모듈을 설치하여 사용하는 방법을 알아볼 필요가 있음.


### 스크래핑 - requests_html, celery
   > worker 실행
   
    celery –A cos worker –l INFO –P eventlet     
   
   > beat 실행(스케줄링을 위한 beat)
   
    celery –A cos beat
    
* cos는 settings.py가 존재하는 cos 디렉토리를 의미한다.
* 현재로는 스크래핑의 스케줄링에 사용하지만, 추후 이미지를 업로드하고 화장품이 추려져 나오는 과정에서 비동기 작업 큐를 사용하여 추천 알고리즘이 진행되는 과정에서도 다른 작업을 할 수 있도록   추가할 예정
    
    
    
