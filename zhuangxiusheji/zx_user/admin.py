from django.contrib import admin
from .models import Ordinary_User, Company_User


class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ['account_number','pk','examine']
    list_filter = ['examine']

admin.site.register(Ordinary_User)
admin.site.register(Company_User, CompanyUserAdmin)
# Register your models here.
