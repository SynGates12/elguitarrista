from django.shortcuts import render, get_object_or_404,redirect, render_to_response
from posts.models import Post, Favorit
from usuaris.models import Perfil, Comentari
from django.contrib import messages
from django.forms import modelform_factory
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import puja_partitura_form, puja_video_form, ComentaForm
from django.contrib.auth.decorators import login_required

@login_required (login_url='usuaris:login')
def favorit(request, post_id):
    usuari = Perfil.objects.get(usuari = request.user)
    postActual = Post.objects.get(id = post_id)
    preferit = Favorit.objects.create(usuari = usuari, postFavorit = postActual)
    return redirect('usuaris:biblioteca')
    
@login_required (login_url='usuaris:login')
def unfav(request, post_id):
    usuari = Perfil.objects.get(usuari = request.user)
    postActual = Post.objects.get(id = post_id)
    preferitborrar = Favorit.objects.get(usuari = usuari, postFavorit = postActual).delete()
    return redirect('usuaris:biblioteca')
    
@login_required (login_url='usuaris:login')
def mur(request):
    posts = Post.objects.all().order_by('?')[:30] 
    meuPerfil = request.user.perfil
    seguits = meuPerfil.usuaris_seguits
    tots =[]
    for perfil_seguidor in seguits.all():
        ultim_post = perfil_seguidor.post
        tots.append(ultim_post)
    ctx = {"posts_seguits":tots, "posts_tots":posts, "seguits":seguits}
    return render(request,"mur.html",ctx)
    
@login_required (login_url='usuaris:login')
def post_informacio(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    meuPerfil = Perfil.objects.get(usuari = request.user)
    es_fav = Favorit.objects.filter(postFavorit = post, usuari = meuPerfil).count()
    if es_fav == 1:
        es_fav = Favorit.objects.get(postFavorit = post, usuari = meuPerfil)
    
    if request.user:
        usuari = request.user
        
        if request.method == 'POST':
            form = ComentaForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data['text']
                Comentari.objects.create (text = text, post=post, usuari = usuari.perfil)
                messages.info(request, "Comentari afegit correctament")
                return redirect(request.META['HTTP_REFERER'])
        else:
            form = ComentaForm()
            
        for f in form.fields:
           form.fields[f].widget.attrs['class'] = 'form-control'
           form.fields['text'].widget.attrs['rows'] = '4'
           form.fields['text'].widget.attrs['placeholder']="Comenta..."
           
        comentari = post.comentari_set.all()
    
    ctx = {'post' : post, 'es_fav' : es_fav, 'form' : form, 'comentari' : comentari}
    
    return render (request, "post_informacio.html", ctx)


@login_required (login_url='usuaris:login')
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
        
@login_required (login_url='usuaris:login')
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
    print (results)
    return render( request, "cerca.html",
                                { "llista_posts": results,
                                   "query": query }
                               )
import sys
import datetime
from django.core.management import call_command
       
@login_required (login_url='usuaris:login')
def fer_backups(request, id_backup):
    if (request.user.usuari.admin):
        objectiu = ''
        if id_backup == '1':
            objectiu = 'posts'
        if id_backup == '2':
            objectiu = 'usuaris'
        sysout = sys.stdout
        nomFitxer = "backups/media/bdd-Backup" + str(datetime.datetime.now()).replace(" ","").replace(":","-")+".xml"
        sys.stdout = open (nomFitxer, 'w')
        call_command('dumpdata',objectiu,indent=2,format='xml')
        sys.stdout = sysout
        return HttpResponseRedirect(reverse('posts:mur'))
    else:
        return HttpResponseRedirect(reverse('posts:biblioteca'))
        
        
@login_required (login_url='usuaris:login')
def eliminar_post (request, post_id = None):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk = post_id)
        if (post_id):
            post.delete()
            return redirect('usuaris:biblioteca')
    else:
        return render(request, 'eliminar_post.html', {'Post' : Post.objects.get(pk=post_id)})
        

@login_required (login_url='usuaris:login')
def apres (request, favorit_id):
    favorit_actual = Favorit.objects.get(id = favorit_id)
    favorit_actual.apres = True
    favorit_actual.save()
    return redirect("usuaris:biblioteca")
