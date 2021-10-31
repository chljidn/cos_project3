from common.models import User, Qa
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = '__all__'

class QaSerializers(serializers.ModelSerializer):
    class Meta:
        model=Qa
        fields = '__all__'

    def validate(self, attrs):
        data = super().validate(attrs)
        # 요청받은 패스워드를 암호화(해쉬)
        data['password'] = make_password(data['password'])
        return data

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username
        return data
