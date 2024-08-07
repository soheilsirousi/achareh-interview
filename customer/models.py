from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
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

    @classmethod
    def login_user(cls, request, user, password):
        if user := authenticate(request, username=user.username, password=password):
            login(request, user)
            return True
        return False

    @classmethod
    def register_user(cls, request, phone_number, password=None):
        if password is None:
            password = User.objects.make_random_password()
        user = User.objects.create_user(username=phone_number, password=password)
        user_detail = cls.objects.get(user=user)
        user_detail.phone_number = phone_number
        user_detail.save()
        cls.login_user(request, user, password)
        return user_detail

    @classmethod
    def save_user_info(cls, phone_number, email, first_name, last_name, password):
        user = User.objects.filter(username=phone_number)
        if not user.exists():
            return None
        user = user.first()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.set_password(password)
        user.save()
        return cls.objects.get(user=user)


class Block(models.Model):
    phone_number = models.PositiveBigIntegerField(null=True, verbose_name=_('phone number'))
    ip_address = models.GenericIPAddressField(null=True, verbose_name=_('ip address'))
    block_until = models.DateTimeField(blank=False, null=False, verbose_name=_('block until'))

    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name = _('block')
        verbose_name_plural = _('blocks')

    @classmethod
    def block_user(cls, phone_number, ip_address, time):
        return Block.objects.update_or_create(phone_number=phone_number, ip_address=ip_address, block_until=time)

    @classmethod
    def is_user_block(cls, ip_address, phone_number):
        user_block = cls.objects.filter(ip_address=ip_address, phone_number=phone_number)
        if not user_block.exists():
            return False
        block_time = user_block.first().block_until
        now = timezone.now()
        if block_time > now:
            return True
        return False
