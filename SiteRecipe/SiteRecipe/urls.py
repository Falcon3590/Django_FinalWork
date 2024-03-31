"""
URL configuration for SiteRecipe project.

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
from django.urls import path, include
from AppSiteRecipe import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
  path('user/<int:id_user>/new', views.new_recipe),
  path('user/<int:id_user>/update', views.new_update),
  path('user/<int:id_user>/update/<int:id_recipe>/', views.update_recipe),
  path('user/<int:id_user>/', views.main),
  path('admin/', admin.site.urls),
  path('', views.registration),
  path('login/', views.user_login),
  path('recipe', views.recipe),
  path('info/<int:id_recipe>/', views.info_recipe)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
