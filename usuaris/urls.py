from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from usuaris import views

app_name='usuaris'

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^crear/', views.crear_usuari,name="crear_usuari"),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^biblioteca/$', views.biblioteca, name='biblioteca'),
    url(r'^(?P<usuari_id>\d+)/follow/$', views.follow, name='follow')
]