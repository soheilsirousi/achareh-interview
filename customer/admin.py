from django.contrib import admin
from django.contrib.admin import register

from customer.models import ExtendedUser, Block


@register(ExtendedUser)
class ExtendedUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')


@register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'ip_address', 'block_until')
