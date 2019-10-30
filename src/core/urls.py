from django.contrib import admin
from django.urls import path, include

from .swagger_urls import swagger_urlpatterns

api_urls = [
    path('', include('accounts.urls')),
    path('', include(swagger_urlpatterns)),
    path('', include('classroom.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
]
