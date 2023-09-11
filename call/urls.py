from django.contrib import admin
from django.urls import path, include
from .views import *
from .consumer import offer


from django.conf.urls.static import static
from django.conf import settings
from asgiref.sync import async_to_sync
#async_offer_view=async_to_sync(offer)

urlpatterns = [
    
	path('register/',UserCreateAPIView.as_view(),name='user'),
	path("chat/<str:chat_box_name>/", chat_box, name="chat"),
    path('offer/',offer)

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)