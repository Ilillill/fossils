from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

def restricted(request):
    return HttpResponse("Access to the admin area is restricted.")

urlpatterns = [
    path('admin/', restricted),
    path('secret_admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('captcha/', include('captcha.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path("", include("app_fossils.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)