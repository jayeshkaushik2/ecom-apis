from django.contrib import admin
from .models import CompanyEmail, Homepage, Detail, Homepage_Images, Founder

# Register your models here.
admin.site.register(Homepage_Images)
admin.site.register(Founder)
admin.site.register(Detail)
admin.site.register(Homepage)
admin.site.register(CompanyEmail)
