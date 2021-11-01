from django.urls import include, path
from django.conf.urls import url
from common.views import qa_views, auth_views
app_name = 'common'

urlpatterns = [
    path('signup_login/', auth_views.signup_login.as_view(), name='signup_login'),
    path('qa/', qa_views.qa.as_view(), name='qa'),
    path('qa/qa_write/', qa_views.qa_write.as_view(), name='qa_write'),
]

