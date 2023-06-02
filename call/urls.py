from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    
	path('register/',UserCreateAPIView.as_view(),name='user'),
	path("chat/<str:chat_box_name>/", chat_box, name="chat")

]