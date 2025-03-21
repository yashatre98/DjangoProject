from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserDetails
from django.http import HttpResponse, JsonResponse



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

# Crud operations, Task-5
def get_all_users(request):
    users = list(UserDetails.objects.values())  # Convert QuerySet to list
    return JsonResponse(users, safe=False)

def get_user_by_email(request, email):
    try:
        user = UserDetails.objects.get(email=email)
        return JsonResponse({"username": user.username, "email": user.email})
    except UserDetails.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


@csrf_exempt
def update_user(request, email):
    if request.method == "PUT":
        try:
            user = UserDetails.objects.get(email=email)
            print("$$$$$", user.username, "$$$$$")
            data = json.loads(request.body)
            print("#####",data.get("username"),"#####", "#####")
            # user.username = data.get("username")
            user.password = data.get("password")

            user.save(update_fields=['password'])

            return JsonResponse({"message": "User updated successfully"})
        except UserDetails.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

@csrf_exempt
def delete_user(request, email):
    if request.method == "DELETE":
        try:
            user = UserDetails.objects.get(email=email)
            user.delete()
            return JsonResponse({"message": "User deleted successfully"})
        except UserDetails.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
