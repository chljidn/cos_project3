# rest_framework 관련 설치
from rest_framework.views import APIView # 모든 함수를 클래스뷰로 하기 위해서 import
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer # html 렌더링 하기 위함

# 해쉬 암호화 모듈
from django.contrib.auth.hashers import make_password, check_password

# serializers.py 설치
from common import serializers

# models 설치
from common.models import User

class signup(APIView):
    def post(self, request):
        print(request.data.get('username'))
        print(request.POST['username'])
        print(request.POST.get('username', '0')) # 타입은 세개 모두 str
        password = make_password(request.POST['password']) # 패스워드를 해쉬함수를 통해서 암호화
        user = User.objects.create(username=request.POST['username'],
                           password=password,
                           sex=request.POST['sex'],
                           birth=request.POST['birth'],
                           email=request.POST['email'])
        user_get = User.objects.filter(password=password)
        user_get_serializer = serializers.UserSerializers(user_get, many=True)
        return Response(user_get_serializer.data)
