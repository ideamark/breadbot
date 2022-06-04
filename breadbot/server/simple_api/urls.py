from django.conf.urls import url
from .views import simpleAPI

urlpatterns = [
    url(r'^simple_api/?$', simpleAPI.as_view()),
]
