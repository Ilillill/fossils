from django.urls import path
from django.http import HttpResponse

from app_fossils.views import *

urlpatterns = [
    path('', home, name='homepage'),
]