from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Post(models.Model):
    nom = models.CharField(max_length=50)
    partitura = models.TextField(null=True)
    video = models.FileField(upload_to='videos/', null=True, verbose_name="")
    usuari = models.ForeignKey('usuaris.Perfil', on_delete=models.SET_NULL, blank=True, null=True, related_name="post")
    votsPositius = models.IntegerField()
    votsNegatius = models.IntegerField()
    
class Favorit(models.Model):
    usuari = models.ForeignKey('usuaris.Perfil', on_delete=models.CASCADE)
    postFavorit = models.ForeignKey(Post, on_delete=models.CASCADE )
    apres = models.BooleanField(default=False)
    data = models.DateField( auto_now_add=True )
    