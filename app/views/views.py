# -------- rest_framework 설치 ------------------------------------
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

# ------- serializers.py 설치 -----------------------------------------
from app.serializers import CosSerializer

# -------- 모델 설치 -----------------------------------------------
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
        # 이미지 저장.
        # 일단 여기까진 성공.
        # 유효성 검사 넣을 수 있는지 찾아볼 것.
        image = ImageUpload()
        image.title = request.POST['title']
        image.pic = request.FILES['pic']
        image.save()

        _image = ImageUpload.objects.get(pic=image.pic) # title이 중복될 수 있으므로 다른 매개변수로 찾을 수 있는지 파악.
        #serializer = UploadimageSerializer(a, many=True)

        recommend_function = recommend.recommend() # recommend class의 객체 생성
        # .pic은 ImageFileField이기 때문에 이미지가 저장된 url을 얻기 위해서는 .url을 해주어야 함.
        # 이미지 url이 /media/~~.jpg임. 하지만 media 폴더가 같은 디렉터리에 있으므로 맨 앞의 /를 지워야 경로 읽기 가능
        # 때문에 맨 앞의 /를 없애기 위해서 [1:] 로 슬라이싱.
        letter_extraction = recommend_function.cross(str(_image.pic.url)[1:])
        print(recommend_function.cosine(letter_extraction))
        #return Response(letter_extraction) # 현재는 이걸로 return 불가


# -------- 화장품 리스트 페이지 -------------------------------------------------------------------------------
class cos_list(APIView):
    def get(self, request):
        start = request.GET.get('start')
        end = request.GET.get('end')
        # 가격, 브랜드, 상품이름, 주요성분, 카테고리만 출력.
        coslist = cache.get_or_set('coslist', Cos.objects.filter(id__range=(start, end))
                                   .values('brand', 'price', 'prdname', 'ingredient'),timeout=None)
        cos_serializer = CosSerializer(coslist, many = True)
        return Response(cos_serializer.data)

































