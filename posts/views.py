from django.shortcuts import render, get_object_or_404,redirect, render_to_response
from posts.models import Post, Favorit
from usuaris.models import Perfil
from django.contrib import messages
from django.forms import modelform_factory
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from .forms import puja_partitura_form, puja_video_form


def favorit(request, usuari_id, post_id):
    usuari = Perfil.objects.get(id = usuari_id)
    postActual = Post.objects.get(id = post_id)
    preferit = Favorit.objects.create(usuari = usuari, postFavorit = postActual)
    return redirect('usuaris:biblioteca')
    
def mur(request):
    posts = Post.objects.all().order_by('?')[:30]
    #usuaris_posts = Perfil
    #seguits = Perfil.usuaris_seguits
    ctx = {"posts_seguits":posts}
    return render(request,"mur.html",ctx)
    

def puja_partitura(request, usuari_id):
    
    usuari_partitura = Perfil.objects.get(id=usuari_id)
    
    if request.method == 'POST':
        form = puja_partitura_form(request.POST)
        
        if form.is_valid():
            nom = form.cleaned_data['nom']
            partitura = form.cleaned_data['partitura']
            
            Post.objects.create(nom = nom, partitura = partitura)
            messages.info(request, "Partitura pujada correctament")
            return redirect("usuaris:biblioteca")
            
        else:
            form = puja_partitura_form()
        
        for f in form.fields:
            form.fields[f].widget.attrs['class'] = 'form-control'
            
        return render (request, 'posts/puja_partitura.html', {'form':form})
        
def puja_video(request, usuari_id):
    
    usuari_video = Perfil.objects.get(id=usuari_id)
    
    if request.method == 'POST':
        form = puja_video_form(request.POST, request.FILES)
        
        if form.is_valid():
            nom = form.cleaned_data['nom']
            video = form.cleaned_data['video']
            
            Post.objects.create(nom = nom, video = video)
            messages.info(request, "Video pujat correctament")
            return redirect("usuaris:biblioteca")
            
        else: 
            form = puja_video_form()
            
        for f in form.fields:
            form.fields[f].widget.attrs['class'] = 'form-control'
            
        return render (request, 'posts/puja_video.html', {'form':form})
        

    
    
    
    
    