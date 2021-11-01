from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from common.serializers import MyTokenObtainPairSerializer

from common.models import User
from common import serializers

class signup(APIView):
    def post(self, request):
        password = make_password(request.POST['password']) # 패스워드를 해쉬함수를 통해서 암호화
        user = User.objects.create(username=request.POST['username'],
                           password=password,
                           sex=request.POST['sex'],
                           birth=request.POST['birth'],
                           email=request.POST['email'])
        user_get = User.objects.filter(password=password)
        user_get_serializer = serializers.UserSerializers(user_get, many=True)
        return Response(user_get_serializer.data)

# login
# simplejwt을 이용한 Token 발급
# access, refresh Token 발급
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# logout
# 형식은 refresh token을 받아서 blacklist에 추가시키는 것. refresh token은 content 부분에 담겨 보내진다.
# 코드 출처 : https://medium.com/django-rest/logout-django-rest-framework-eb1b53ac6d35
class logout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, reuqest):
        try:
            refresh_token = reuqest.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
