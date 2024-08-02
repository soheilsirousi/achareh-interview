from django.contrib import admin
from django.contrib.admin import register

from customer.models import ExtendedUser


@register(ExtendedUser)
class ExtendedUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
