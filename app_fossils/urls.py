from django.urls import path
from django.http import HttpResponse

from .views import *

urlpatterns = [
    path('', home, name='homepage'),
    path('species_add/', species_add, name='species-add'),
    path('fossil_add/', fossil_add, name='fossil-add'),
    path('specie/<int:pk>/', species, name='species-selected'),
    path('fossil/<int:pk>/', fossil, name='fossil-selected'),
]