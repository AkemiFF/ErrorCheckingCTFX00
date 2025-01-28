"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from accounts.views import MyTokenObtainPairView, MyTokenRefreshView
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('test/', test, name='test'),
    path('build_images/', build_images, name='build_images'),
    path('stop_test/', stop_test, name='stop_test'),
    path('<int:port>/<str:path>', proxy_to_docker, name='proxy_to_docker'),
    # path('challenge/<int:challenge_id>/start/', views.start_challenge, name='start_challenge'),

    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
]
