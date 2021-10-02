from rest_framework import serializers
from app.models import ImageUpload, Cos

class ImageUploadSerializer(serializers.ModelSerializer):
    pic = serializers.ImageField(use_url=True)
    class Meta:
        model = ImageUpload
        fields = ('title','pic')

class CosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cos
       # fields = '__all__'
        fields = ('brand', 'price', 'prdname', 'ingredient')
