from django.conf.urls import url
from .views import simpleAPI

urlpatterns = [
    url(r'^$', simpleAPI.as_view()),
]
