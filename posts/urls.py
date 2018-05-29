from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from posts import views

app_name='posts'

urlpatterns = [
    url(r'^mur/(?P<usuari_id>\d+)/puja_partitura/', views.puja_partitura, name="puja_partitura"),
    url(r'^mur/(?P<usuari_id>\d+)/puja_video/', views.puja_video, name="puja_video"),
    url(r'^mur/', views.mur, name="mur"),
    url(r'^post_informacio/(?P<post_id>\d+)$', views.post_informacio, name="post_informacio"),
    url(r'^cerca/', views.cerca, name="cerca"),
    url(r'^(?P<post_id>\d+)/favorit/', views.favorit, name="favorit"),
    url(r'^(?P<post_id>\d+)/unfav/', views.unfav, name="unfav"),
    url(r'^(?P<id_backup>\d+)/fer_backups/$', views.fer_backups, name="fer_backups")
]