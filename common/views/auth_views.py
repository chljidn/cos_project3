from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# 각 요청에 대한 허융/거부
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from common.serializers import MyTokenObtainPairSerializer

# rest_framework의 authtoken을 이용한 로그인. 토큰 발급
# 추후 simplejwt로 수정 예상
class login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request':request})
        serializer.is_valid(raise_exception=True)
        user= serializer.validated_data['user']
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key,
                            'id': user.username
                            })
        else:
            return Response({'message': '아이디를 다시 입력하세요'})

class logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

# -----------------------------------------------------------------

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
