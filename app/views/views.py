# rest_framework 관련 모듈 설치
from rest_framework.response import Response
from rest_framework import viewsets
# filter
from django_filters.rest_framework import DjangoFilterBackend
from app.filters import CosFilter
# serializers 설치
from app.serializers import CosSerializer, RecommendSerializer

# 모델 설치
from app.models import ImageUpload, Cos
from app.views.recommend import recommend
from django.core.cache import cache

# 이미지 업로드 페이지
# 이미지 파일은 'media/imageupload' 디렉터리 경로로 저장
class image_upload(viewsets.ViewSet):
    serializer_class = RecommendSerializer

    def create(self, request):
        image = ImageUpload()
        image.title = request.POST['title']
        image.pic = request.FILES['pic']
        image.save()

        # recommend class의 객체 생성
        recommend_function = recommend(image.pic.url)
        # 추출된 성분 문자열로 코사인 유사도 수행.
        result = recommend_function.cosine()
        result_serializer = RecommendSerializer(result, many=True)
        return Response(result_serializer.data)


# 화장품 리스트 페이지
class cos_list(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]

    queryset = cache.get_or_set('coslist', Cos.objects.filter().values('brand', 'image','price','prdname','ingredient').distinct())
    serializer_class = CosSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CosFilter
