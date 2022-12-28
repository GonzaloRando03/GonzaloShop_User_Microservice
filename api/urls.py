from django.urls import path
from .views.UserView import UserView
from .views.LoginView import LoginView

urlpatterns=[
    path('users/', UserView.as_view(), name='usuarios_list'),
    path('login/', LoginView.as_view(), name='login'),
]