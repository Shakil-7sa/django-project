from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')

def recipe(request):
    if request.method=='POST':
        recipe_name=request.POST.get('recipe_name')
        recipe_description=request.POST.get('recipe_description')
        recipe_image=request.FILES.get('recipe_image')
    
        recipes.objects.create(
            recipe_name=recipe_name,
            recipe_description=recipe_description,
            recipe_image=recipe_image
            )
        return redirect('/recipe/')
    queryset=recipes.objects.all()
    if request.GET.get('search'):
        queryset=queryset.filter(recipe_name__icontains=request.GET.get('search'))
    context={'recipe' : queryset}
    return render(request, 'recipe.html', context)

def delete(request, id):
    queryset=recipes.objects.get(id=id)
    queryset.delete()
    return redirect('/recipe/')

def update(request, id):
    queryset=recipes.objects.get(id=id)
    if request.method=='POST':
        recipe_name=request.POST.get('recipe_name')
        recipe_description=request.POST.get('recipe_description')
        recipe_image=request.FILES.get('recipe_image')
        
        queryset.recipe_name= recipe_name
        queryset.recipe_description=recipe_description
        if recipe_image:
            queryset.recipe_image=recipe_image
        queryset.save()
        return redirect('/recipe/')
    context={'recipe' : queryset}
    return render(request, 'update.html', context)

def login_page(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        
        user=authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/recipe/')
            
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

def register(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, 'Username already taken')
            return redirect('/register/')
                    
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
            )
        user.set_password(password)
        user.save()
        messages.info(request, 'Account created successfully')
        return redirect('/register/')
             
    return render(request, 'register.html')   