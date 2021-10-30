from django.urls import path, include
from app.views import views as app_views
from rest_framework.routers import DefaultRouter
app_name = 'app'

router = DefaultRouter()
router.register(r'cos_list', app_views.cos_list, basename='cos_list')
router.register(r'upload', app_views.image_upload, basename='upload')

urlpatterns = [
    path('', include(router.urls))
]