from django.contrib import admin
# Register your models here.
from .models import User

class UserAdmin(admin.ModelAdmin):
	model=User
	def get_queryset(self, request):
		return User.admin.all()
		





admin.site.register(User,UserAdmin)
