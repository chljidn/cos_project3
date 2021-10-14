## cos_project3

recos - 화장품 추천 서비스<br>
django, mariadb, nginx, uwsgi, aws, celery, redis<br>
<br>
api : 화장품 리스트, 화장품 추천 리스트(이미지 업로드 api에서 자동 호출)<br>
      회원 리스트, 마이 페이지<br>
      Q&A 리스트, Q&A 작성, Q&A 수정<br>
      스크래핑(celery를 통한 스케줄링, db : redis, 메시지 브로커: redis)<br>
      

프로젝트 구성 - cos : 프로젝트 디렉토리(settings.py, celery.py)<br>  
                app : 화장품 데이터 스크래핑 및 업로드(scraping.cos_scraping.py), 화장품 성분 이미지 업로드(views.py), 화장품 추천(recommend.py)<br>  
                
                
                common : 회원가입(views.signup_views.py), Q&A(views.qa_views.py)<br>
                
스크래핑 
       
   > worker 실행
   > celery –A cos worker –l INFO –P eventlet
   
   > beat 실행(스케줄링을 위한 beat)
   > elery –A cos beat
