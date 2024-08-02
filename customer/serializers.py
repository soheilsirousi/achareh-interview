from rest_framework import serializers

from customer.models import ExtendedUser


class ExtendedUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(source='user.password', write_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = ExtendedUser
        fields = ('user', 'phone_number', 'password', 'first_name', 'last_name')
