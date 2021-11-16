from django.urls import include, path
from common.views import qa_views, auth_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'common'

router = DefaultRouter()
router.register(r'qa', qa_views.qa, basename='qa')
router.register(r'useredit', auth_views.userEdit, basename='useredit')

urlpatterns = [
    path('mypage/', auth_views.myPage.as_view(), name='myPage'),
    path('auth/', auth_views.signup_login.as_view(), name='auth'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('', include(router.urls))
]

