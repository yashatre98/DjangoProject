from django.urls import path
from . import views

urlpatterns = [
    path('task-2/', views.hello_world, name='hello'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),

]
