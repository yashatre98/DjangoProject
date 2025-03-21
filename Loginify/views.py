from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserDetails
from django.http import HttpResponse

# Task-2 hello view
def hello_world(request):
    return HttpResponse("Hello, world!")


# Signup View
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('signup')

        user = UserDetails(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Signup successful! Please log in.")
        return redirect('login')

    return render(request, 'signup.html')


# Login View
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = UserDetails.objects.get(email=email)
            if user.password == password:
                messages.success(request, f"Welcome, {user.username}!")
                return render(request, 'success.html', {'username': user.username})
            else:
                messages.error(request, "Invalid credentials!")
                return redirect('login')
        except UserDetails.DoesNotExist:
            messages.error(request, "User does not exist!")
            return redirect('login')

    return render(request, 'login.html')
