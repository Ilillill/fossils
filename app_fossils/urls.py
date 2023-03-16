from django.urls import path
from django.http import HttpResponse

from .views import *

urlpatterns = [
    path('', home, name='homepage'),
    path('search_get', search_result_get, name='search-get'),
    path('search_post', search_result_post, name='search-post'),

    path('profile', user_profile, name='profile'),
    # path('account_update', user_account_update, name='account-update'),
    # path('profile_create_update', user_profile_create_update, name='profile-create_update'),

    path('species_add/', species_add, name='species-add'),
    path('fossil_add/', fossil_add, name='fossil-add'),
    path('specie/<int:pk>/', species, name='species-selected'),
    path('fossil/<int:pk>/', fossil, name='fossil-selected'),
    
    path('fossil_update/<int:pk>/', fossil_update, name='fossil-update'),
    
    path('fossil_delete/<int:pk>/', fossil_delete, name='fossil-delete'),

    path('chart_simple/', chart_simple, name='chart-simple'),
    path('chart_multi/', chart_multi, name='chart-multi'),

    path('gatherings/', gatherings, name='gatherings'),
    path('gathering/<int:pk>/', gathering_selected, name='gathering-selected'),
    
    path('events/', events, name='events'),
    path('event/<int:pk>/', event_selected, name='event-selected'),
    
    path('fossil_event_return/<int:pk>/', fossil_event_return, name='fossil-event-return'),
    path('fossil_event_update/<int:pk>/', fossil_event_update, name='fossil-event-update'),

]