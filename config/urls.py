"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.view.home import home_view 

# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from api import views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'perfis', views.PerfilViewSet, basename='perfil')
router.register(r'usuarios', views.UsuarioViewSet, basename='usuario')
router.register(r'etapas-escolares', views.EtapaEscolarViewSet, basename='etapaescolar')
router.register(r'disciplinas', views.DisciplinaViewSet, basename='disciplina')
router.register(r'status-envio', views.StatusEnvioViewSet, basename='statusenvio')
router.register(r'envios-material', views.EnvioMaterialViewSet, basename='enviomaterial')

# Define URL patterns
urlpatterns = [
    path('', home_view, name='home'),

    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include(router.urls)),
    
    # API Documentation endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Browsable API authentication (optional)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

