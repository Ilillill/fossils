from django.urls import path
from django.http import HttpResponse

from .views import *

urlpatterns = [
    path('', home, name='homepage'),
    path('search_get', search_result_get, name='search-get'),
    path('search_post', search_result_post, name='search-post'),

    path('profile', user_profile, name='profile'),
    path('account_update', user_account_update, name='account-update'),
    path('profile_create_update', user_profile_create_update, name='profile-create_update'),

    path('species_add/', species_add, name='species-add'),
    path('fossil_add/', fossil_add, name='fossil-add'),
    path('specie/<int:pk>/', species, name='species-selected'),
    path('fossil/<int:pk>/', fossil, name='fossil-selected'),
    path('species_update/<int:pk>/', species_update, name='species-update'),
    path('fossil_update/<int:pk>/', fossil_update, name='fossil-update'),
    path('species_delete/<int:pk>/', species_delete, name='species-delete'),
    path('fossil_delete/<int:pk>/', fossil_delete, name='fossil-delete'),

    path('chart_simple/', chart_simple, name='chart-simple'),
    path('chart_multi/', chart_multi, name='chart-multi'),

]