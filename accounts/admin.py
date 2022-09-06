from django.contrib import admin
from .models import Profile, Address, UserEmail, UserPhone

# Register your models here.
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(UserEmail)
admin.site.register(UserPhone)