# rest_framework 관련 설치
from rest_framework.views import APIView # 모든 함수를 클래스뷰로 하기 위해서 import
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer # html 렌더링 하기 위함
# 해쉬 암호화 모듈
from django.contrib.auth.hashers import make_password, check_password
# serializers.py 설치
from common import serializers
# 모델 설치
from common.models import Qa
# cache
from django.core.cache import cache


class qa(APIView):
    #renderer_classes = [TemplateHTMLRenderer]
    #template_name = 'common/qa.html' #
    def get(self, request):
        qa_list = cache.get_or_set('qa_list', Qa.objects.all())
        qa_get = serializers.QaSerializers(qa_list, many = True)
        #return Response({'qa':qa_list}) #html에 렌더링 할 때에는 딕셔너리 형태로 넣어주기
        return Response(qa_get.data) # 렌더링 안하고 rest로 내보내기


class qa_write(APIView):
    def post(self, request):
        postname = request.POST['postname']
        #password = make_password(request.POST['password'])
        password = request.POST['password'] # 모델 설정할 때, 해쉬 생각 못하고 max_length를 너무 짧게 정함. 일단 이렇게...
        content = request.POST['content']


        new_qa = Qa.objects.create(postname=postname,
                               password=password,
                               content=content)

        qa_data = dict(postname=postname,
                       password=password,
                       content=content)
        print(type(qa_data))
        # serializer 해서 그 중 data를 내보내는 것과 dictionary의 차이는?
        # serializer.data 각 부분은 orderedict 인것으로 알고있긴한데...
        return Response(qa_data)

class qa_edit(APIView):
    def post(self, request, pk):
        posting = Qa.objects.filter(pk=pk)
        posting.update(contents=request.POST.get('contents'),
                       postname=request.POST.get('postname'),
                       password=request.POST.get('password'),
                       )
