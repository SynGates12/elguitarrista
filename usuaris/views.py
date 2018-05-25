# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from .forms import LoginForm, NouUsuariForm
from django.core.urlresolvers import reverse
from django.forms import modelform_factory
from .models import Perfil
from posts.models import Post, Favorit
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import ( login as authLogin,
                                  authenticate,
                                  logout as authLogout )
from django.contrib import messages

#CREAR USUARI -------
def crear_usuari(request, perfil_id=None):
    
    if request.method == 'POST':
        form = NouUsuariForm(request.POST )
        
        if form.is_valid():
            email = form.cleaned_data['email']
            repetit = User.objects.filter( username = email )
            #mirem si està repetit i llencem missatge error
            if repetit:
                messages.error( request, "Aquest nom d'usuari ja existeix")
            else:
                password = form.cleaned_data['password']
                #creem el nou usuari
                nou_usuari = User.objects.create_user( username = email, email = email, password = password )
                
                messages.info(request,"Usuari creat correctament")
                return redirect('usuaris:login')
    else:
        form = NouUsuariForm()
    
    for f in form.fields:
       form.fields[f].widget.attrs['class'] = 'form-control'
       
    form.fields['email'].widget.attrs['placeholder']="Email"
    form.fields['password'].widget.attrs['placeholder']="Contrasenya"
    form.fields['email'].widget.attrs['required']="required"
    form.fields['password'].widget.attrs['required']="required"
    
    return render(request, 'crear_usuari.html', {'form': form} )
    

#biblioteca
def biblioteca(request):
    user = Perfil.objects.get(usuari = request.user)
    posts_propis = Post.objects.filter(usuari = user)
    posts_guardats = Favorit.objects.filter(usuari = user ) 
    ctx={"posts_propis" : posts_propis, "posts_guardats" : posts_guardats}
    return render (request, "biblioteca.html", ctx)
    
def usuari_informacio(request, usuari_id):
    usuari = get_object_or_404(Perfil, pk = usuari_id)
    ctx = {'usuari' : usuari}
    return render (request, "usuari_informacio.html", ctx)

def follow (request, usuari_id1, usuari_id2):
    usuari = Perfil.objects.get(id = usuari_id1)
    seguir = Perfil.objects.get(id = usuari_id2)
    usuari.usuaris_seguits.add(seguir)
    usuari.save()

#loguejar usuari    
def login(request):

    #si tot es POST:
    if request.method=='POST':
        form=LoginForm( request.POST )

        if form.is_valid():
            user=authenticate( username = form.cleaned_data['username'],
                               password = form.cleaned_data['password'])
               
            if user and user.is_active:
                #si tot és ok:
                authLogin( request, user )
                next = request.GET.get('next')
                messages.info(request,"Benvingut")
                return redirect('posts:mur')

            else:
                messages.error(request,"Usuari o password incorrecte o usuari no actiu")
                print "error"
           
    else:
        form=LoginForm()
   
    
    for f in form.fields:
       form.fields[f].widget.attrs['class'] = 'form-control'
    
    ctx={ 'form':form, }
    form.fields['username'].widget.attrs['placeholder']="Email"
    form.fields['password'].widget.attrs['placeholder']="Contrasenya"
    form.fields['username'].widget.attrs['required']="required"
    form.fields['password'].widget.attrs['required']="required"
    
    return render(request, 'login.html', ctx )
    
#DESLOGUEJAR-SE: me voy! ---    
def logout(request):
    authLogout( request )
    return redirect( 'usuaris:login')