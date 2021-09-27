from django.urls import path
from app.views import views as app_views

app_name = 'app'

urlpatterns = [
    path('upload/', app_views.image_upload.as_view(), name='imageupload'),
    path('cos_list/', app_views.cos_list.as_view(), name='cos_list'),
]