from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status

from rest_framework.response import Response

# 로그인. 토큰 발급
# 추후 simplejwt로 수정 예상
class loginview(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serㅅializer_class(data=request.data,
                                           context={'request':request})
        serializer.is_valid(raise_exception=True)
        user= serializer.validated_data['user']
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            print(token)
            return Response({'token': token.key,
                            'id': user.username
                            })
            #return render(request, 'common/login1.html', {'token': token.key,
            #                'id': user.username
            #                })
        else:
            return Response({'message': '아이디를 다시 입력하세요'})
#-----------------------------------------------
class logoutview(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
