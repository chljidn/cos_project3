from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
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
#-----------------------------------------------
class logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

# simplejwt을 이용한 Token 발급
# access, refresh Token 발급
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
