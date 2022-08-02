from django.contrib import admin
from django.urls import path, include

# Add cutom apps urls, based on api versions
urlpatterns_v1 = [
    path("", include("planes.api.urls")),
]

# Main urlpatterns that bind everything together.
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include(urlpatterns_v1)),
]

# Add drf auth for browser api
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
