from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.core import exceptions 
import random
from .models import *

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self,validated_data):
    	User=super(UserSerializer,self).create(validated_data)
    	User.set_password(validated_data['password'])
    	User.save()
    	
    	return User