from rest_framework import serializers
from app.models import ImageUpload, Cos

class ImageUploadSerializer(serializers.ModelSerializer):
    # 이게 뭔 의미임????
    # 모델에서 가져온 쿼리셋을 serializer할 때에 imagefield를 따로 처리해야 하기 땜누에
    # 이렇게 한건가? 바이너리???
    # 즉 이부분은 저장할 때 필요한게 아니라, 불러와서 이미지를 불러와서 serializer할 때에
    # 필요한 부분 같은데
    # 공식 페이지에서는 pillow 패키지가 필요하다고 나옴.
    pic = serializers.ImageField(use_url=True)
    class Meta:
        model = ImageUpload
        fields = ('title','pic')

class CosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cos
       # fields = '__all__'
        fields = ('brand', 'price', 'prdname', 'ingredient')
