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
    # path('species_update/<int:pk>/', species_update, name='species-update'),
    path('fossil_update/<int:pk>/', fossil_update, name='fossil-update'),
    # path('species_delete/<int:pk>/', species_delete, name='species-delete'),
    path('fossil_delete/<int:pk>/', fossil_delete, name='fossil-delete'),

    path('chart_simple/', chart_simple, name='chart-simple'),
    path('chart_multi/', chart_multi, name='chart-multi'),

    path('gatherings/', gatherings, name='gatherings'),
    path('gathering/<int:pk>/', gathering_selected, name='gathering-selected'),
    path('gathering_add/', gathering_add, name='gathering-add'),
    path('gathering_update/<int:pk>/', gathering_update, name='gathering-update'),

    path('events/', events, name='events'),
    path('event/<int:pk>/', event_selected, name='event-selected'),
    path('event_add/', event_add, name='event-add'),

    path('fossil_event_add/<int:pk>/', fossil_event_add, name='fossil-event-add'),
    path('fossil_event_return/<int:pk>/', fossil_event_return, name='fossil-event-return'),
    path('fossil_event_update/<int:pk>/', fossil_event_update, name='fossil-event-update'),

]