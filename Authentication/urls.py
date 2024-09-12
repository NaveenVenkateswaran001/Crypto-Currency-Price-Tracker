from django.urls import path
from Authentication import views

urlpatterns = [
    
    path('', views.loginForm, name='loginForm'),
    path('signup/', views.signupForm, name='signupForm'),
    path('logout/',views.logoutForm,name='logout')
]
