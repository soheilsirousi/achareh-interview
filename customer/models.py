from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class ExtendedUser(models.Model):

    user = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE, verbose_name=_('user'))
    phone_number = models.PositiveBigIntegerField(null=True, blank=True, verbose_name=_('phone number'))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('created time'))
    modified_time = models.DateTimeField(auto_now=True, verbose_name=_('modified time'))

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = _('Extended User')
        verbose_name_plural = _('Extended Users')

    @classmethod
    def get_user_by_username(cls, username):
        user = cls.objects.select_related('user').filter(user__username=username)
        return user.first() if user.exists() else None

    @classmethod
    def get_user_by_phone(cls, phone_number):
        user = cls.objects.filter(phone_number=phone_number)
        return user.first() if user.exists() else None