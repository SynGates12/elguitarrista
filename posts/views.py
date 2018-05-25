from django.shortcuts import render, get_object_or_404,redirect, render_to_response
from posts.models import Post, Favorit
from usuaris.models import Perfil
from django.contrib import messages
from django.forms import modelform_factory
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import puja_partitura_form, puja_video_form


def favorit(request, usuari_id, post_id):
    usuari = Perfil.objects.get(id = usuari_id)
    postActual = Post.objects.get(id = post_id)
    preferit = Favorit.objects.create(usuari = usuari, postFavorit = postActual)
    return redirect('usuaris:biblioteca')
    
def mur(request):
    posts = Post.objects.all().order_by('?')[:30] 
    usuari = Perfil.objects.get(usuari = request.user)
    seguits = usuari.usuaris_seguits
    tots =[]
    for usuar in seguits.all():
        usuari_actual = Perfil.objects.get(usuari = usuar.user)
        ultim_post = Post.objects.latest(usuari = usuari_actual)
        tots.append(ultim_post)
    ctx = {"posts_seguits":tots, "posts_tots":posts}
    return render(request,"mur.html",ctx)
    
def post_informacio(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    ctx = {'post' : post}
    return render (request, "post_informacio.html", ctx)


def puja_partitura(request, usuari_id):
    
    usuari_partitura = Perfil.objects.get(id=usuari_id)
    
    if request.method == 'POST':
        form = puja_partitura_form(request.POST)
        
        if form.is_valid():
            nom = form.cleaned_data['nom']
            partitura = form.cleaned_data['partitura']
            
            Post.objects.create(nom = nom, partitura = partitura, usuari = usuari_partitura)
            messages.info(request, "Partitura pujada correctament")
            return redirect("usuaris:biblioteca")
            
    else:
        form = puja_partitura_form()
        
    for f in form.fields:
        form.fields[f].widget.attrs['class'] = 'form-control'
        form.fields['nom'].widget.attrs['placeholder'] = 'Titol partitura'
        form.fields['partitura'].widget.attrs['placeholder'] = 'Partitura'
        form.fields['nom'].widget.attrs['required']="required"
        form.fields['partitura'].widget.attrs['required']="required"
        
    return render (request, 'puja_partitura.html', {'form':form})
        
def puja_video(request, usuari_id):
    
    usuari_video = Perfil.objects.get(id=usuari_id)
    
    if request.method == 'POST':
        form = puja_video_form(request.POST, request.FILES)
        
        if form.is_valid():
            nom = form.cleaned_data['nom']
            video = form.cleaned_data['video']
            
            Post.objects.create(nom = nom, video = video, usuari = usuari_video)
            messages.info(request, "Video pujat correctament")
            return redirect("usuaris:biblioteca")
            
    else: 
        form = puja_video_form()
            
    for f in form.fields:
        form.fields[f].widget.attrs['class'] = 'form-control'
        form.fields['nom'].widget.attrs['placeholder'] = 'Titol video'
        form.fields['nom'].widget.attrs['required']="required"
        form.fields['video'].widget.attrs['required']="required"
            
    return render (request, 'puja_video.html', {'form':form})

def cerca(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(nom__icontains=query)
        )
        results = Post.objects.filter(qset).distinct()
    else:
        results = []
    return render( request, "posts/cerca.html",
                                { "llista_posts": results,
                                   "query": query }
                               )

       

    
    
    
    
    