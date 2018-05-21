from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from posts import views

app_name='posts'

urlpatterns = [
    url(r'^puja_partitura/', views.puja_partitura, name="puja_partitura"),
    url(r'^puja_video/', views.puja_video, name="puja_video"),
    url(r'^mur/', views.mur, name="mur"),
    url(r'^(?P<post_id>\d+)/favorit/', views.favorit, name="favorit")
]