# -------- rest_framework 설치 ------------------------------------
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import generics

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# filter
from django_filters.rest_framework import DjangoFilterBackend
from app.filters import CosFilter

# serializers 설치
from app.serializers import CosSerializer

# 모델 설치
from app.models import ImageUpload, Cos

from app.views import recommend

from django.core.cache import cache

# -------- 이미지 업로드 페이지 --------------------------------------
# 이미지 파일은 'media/imageupload' 디렉터리 경로로 저장
class image_upload(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name='app/upload.html'

    # get이 꼭 필요한데, 다른 형태로 return 할 수 없는지 확인해 볼 것.
    def get(self, request):
        imagelist = ImageUpload.objects.all()
        return Response({'imgaelist':imagelist})

    def post(self, request):
        # 이미지 이름, url 저장
        image = ImageUpload()
        image.title = request.POST['title']
        image.pic = request.FILES['pic']
        image.save()

        # 코사인 유사도를 통한 화장품 추천
        _image = ImageUpload.objects.get(pic=image.pic)
        recommend_function = recommend(image.pic.url)
        result = recommend_function.cosine()
        return Response(result)



# -------- 화장품 리스트 페이지 -------------------------------------------------------------------------------
# filterset를 따로 지정
class cos_list(generics.ListAPIView):
    # 인증하지 않은 상태로는 접근할 수 없도록 지정
    # authentication의 방식은 Token 방식
    # permission은 정확히 뭔지 찾아볼 것
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = cache.get_or_set('coslist', Cos.objects.filter().values('brand', 'image','price','prdname','ingredient').distinct())
    serializer_class = CosSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CosFilter






































