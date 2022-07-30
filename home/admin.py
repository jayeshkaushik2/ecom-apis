from django.contrib import admin
from .models import Homepage, Detail, Homepage_Images, Founder

# Register your models here.
admin.site.register(Homepage_Images)
admin.site.register(Founder)
admin.site.register(Detail)
admin.site.register(Homepage)
