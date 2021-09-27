from rest_framework import serializers
from common.models import User, Qa

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = '__all__'

class QaSerializers(serializers.ModelSerializer):
    class Meta:
        model=Qa
        fields = '__all__'
