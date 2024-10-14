from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import os
from django.contrib.auth.decorators import login_required


# Create your views here.
@csrf_exempt
@login_required
def home(request):
    items = item.objects.all()
    return render(request, "home.html", {'items':items})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate inputs
        if not email or not password:
            return JsonResponse({"error": "Email and password are required"}, status=400)

        # Authenticate user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)  # Logs the user in
            next_url = request.GET.get('next', 'home')  # Redirect to 'next' if available
            return redirect(next_url)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

    return render(request, 'login.html')


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        # Validate email and password
        if "crce" in email and password == cpassword:
            try:
                user = User.objects.create_user(
                    username=email,  # Use email as the username
                    email=email,
                    password=password  # Password will be hashed automatically
                )
                user.save()
                messages.success(request, "Sign up successful! You can now log in.")
                return redirect('login')

            except Exception as e:
                messages.error(request, f"Sign up failed. Please try again. Error: {e}")
        else:
            return JsonResponse({"message": "Please use a valid 'crce' email and ensure passwords match."})
    
    return render(request, 'signup.html')

@login_required
def upload(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        description = request.POST.get('description')
        contact = request.POST.get('contact')
        image = request.FILES.get('image')

        # Validate inputs
        if not (name and location and description and contact and image):
            return JsonResponse({"error": "All fields are required"}, status=400)

        try:
            new_item = item(
                name=name,
                location=location,
                description=description,
                image=image,
                contact=contact,
                user=request.user  # Set the user who uploaded the item
            )
            new_item.save()
            return redirect('home')

        except Exception as e:
            return JsonResponse({"error": f"Failed to upload item: {e}"}, status=500)

    return render(request, 'upload.html')

@login_required
def search(request):
    items = []  # Initialize an empty list for items
    if request.method == 'POST':
        search_query = request.POST.get('search')
        if search_query:  # Check if the search query is not empty
            items = item.objects.filter(name__icontains=search_query)
    
    return render(request, 'home.html', {'items': items}) 

@login_required
def logout_view(request):
    logout(request)  # Logs the user out
    return redirect('login')