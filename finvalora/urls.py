
from django.contrib import admin
from django.urls import path, include
from user import urls
from finance import urls
from analytics import urls
from drf_spectacular.renderers import OpenApiJsonRenderer
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [

    path('admin/', admin.site.urls),
    
    path('', include('user.urls')),
    path('finance/', include('finance.urls')),
    path('analytics/', include('analytics.urls')),
    # Serve openapi.json directly at root level
    path('openapi.json', SpectacularAPIView.as_view(renderer_classes=[OpenApiJsonRenderer]), name='schema'),

    # Optional: Serve interactive UIs that reference your schema
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
]
