from django.urls import path
from django.conf.urls import url
from .views import RegisterView, UsernameCountView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    url(r'username/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', UsernameCountView.as_view()),
]