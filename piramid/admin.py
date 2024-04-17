from django.contrib import admin
from .models import Products, User


admin.site.register(Products)


class UserLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'username', 'email', 'balance', 'reg_date')


admin.site.register(User, UserLevelAdmin)
