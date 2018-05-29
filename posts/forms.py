from django import forms
from django.conf import settings
from .models import Post, Favorit
from django.contrib.auth.models import User
from django.forms import ModelForm

class puja_partitura_form (forms.Form):
    nom = forms.CharField(max_length=120)
    partitura = forms.CharField(widget=forms.Textarea)
    
    
class puja_video_form (forms.Form):
    nom = forms.CharField(max_length=120)
    video = forms.FileField()
    
class ComentaForm(forms.Form):
    text=forms.CharField(label="Comenta...",widget=forms.Textarea)