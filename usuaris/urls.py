from django.conf.urls import url
from . import views

app_name='usuaris'

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^crear/', views.crear_usuari,name="crear_usuari"),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^(?P<usuari_id>\d+)/biblioteca/$', views.biblioteca, name='biblioteca')
]