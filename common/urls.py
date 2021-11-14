from django.urls import include, path
from django.conf.urls import url
from common.views import qa_views, auth_views
from rest_framework.routers import DefaultRouter
app_name = 'common'

router = DefaultRouter()
router.register(r'qa', qa_views.qa, basename='qa')
router.register(r'userEdit', auth_views.userEdit, basename='userEdit')

urlpatterns = [
    path('mypage/', auth_views.myPage.as_view(), name='myPage'),
    path('auth/', auth_views.signup_login.as_view(), name='auth'),
    path('', include(router.urls))
]

