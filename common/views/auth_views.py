from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import QueryDict

from common.serializers import MyTokenObtainPairSerializer
from common.models import User

# signup/login
# simplejwt을 이용한 Token 발급
# signup의 경우 request에서 email이 not False일 때에 request 데이터를 저장하고 토큰 발급
# email field가 없는 경우 토큰만 발급
# set_cookie를 통해서 토큰을 response set-cookie header에 담아보낸다
# 참고 : https://stackoverflow.com/questions/66197928/django-rest-how-do-i-return-simplejwt-access-and-refresh-tokens-as-httponly-coo
class signup_login(TokenObtainPairView):
    #serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        if request.POST.get('email', False):
            password = make_password(request.POST['password'])  # 패스워드를 해쉬함수를 통해서 암호화
            user = User.objects.create(username=request.POST['username'],
                                       password=password,
                                       sex=request.POST['sex'],
                                       birth=request.POST['birth'],
                                       email=request.POST['email'])
            user_data = QueryDict(f'''username={request.POST['username']}&password={request.POST['password']}''')
        else:
            user_data = request.data

        serializer = MyTokenObtainPairSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        access = serializer.validated_data.get("access", None)
        refresh = serializer.validated_data.get("refresh", None)
        username = serializer.validated_data.get("username", None)

        if access is not None:
            response = Response({}, status=200)
            response.set_cookie('token', access, httponly=True)
            response.set_cookie('refresh', refresh, httponly=True)
            response.set_cookie('email', username, httponly=True)
            return response

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
