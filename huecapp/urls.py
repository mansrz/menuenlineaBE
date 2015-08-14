"""huecapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from web.views import *
from rest_framework import routers, serializers, viewsets
from web.viewsets import *
from django.conf import settings
from django.conf.urls.static import static


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'Restaurantes', RestaurantViewSet)
router.register(r'RestaurantPlato', RestaurantDishViewSet)
router.register(r'Categorias', CategoryViewSet)
router.register(r'CriterioCategoria', CategoryCriteriaViewSet)
router.register(r'CriterioEvaluacion', EvaluationCriteriaViewSet)
router.register(r'Evaluacion', EvaluationViewSet)
router.register(r'GCMDevice',GCMDeviceViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/', 'web.views.signup'),
    url(r'^top/', 'web.views.getTopFull'),
    url(r'^filter/', 'web.views.getByFilter'),
    url(r'^categories/', 'web.views.getCategories'),
    url(r'^dishes/', 'web.views.getDishes'),
    url(r'^restaurants/', 'web.views.getRestaurants'),
    url(r'^rank/', 'web.views.rank'),
    url(r'^lasthuecas/', 'web.views.lasthuecas'),
    url(r'^login/', 'web.views.login'),
    url(r'^logout/', 'web.views.logout'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^pushes/', 'web.views.push_notifications_view', name='push_notifications_view'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
