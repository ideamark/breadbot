from django.conf.urls import url
from .views import WeChat

urlpatterns = [
    url(r'^$', WeChat.as_view()),
]
