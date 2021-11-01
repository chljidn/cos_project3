from django.urls import include, path
from django.conf.urls import url
from common.views import qa_views, signup_views, auth_views
app_name = 'common'

urlpatterns = [
    path('signup/', auth_views.signup.as_view(), name='signup'),
    path('qa/', qa_views.qa.as_view(), name='qa'),
    path('qa/qa_write/', qa_views.qa_write.as_view(), name='qa_write'),
    path('jwtlogin', auth_views.MyTokenObtainPairView.as_view(), name='jwtlogin')
]

