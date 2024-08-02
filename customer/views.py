from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
import random
from customer.models import ExtendedUser
from customer.serializers import ExtendedUserSerializer


class UserRetrieveAPI(APIView):

    def get(self, request, username, *args, **kwargs):
        data = dict({'data': '', 'error': ''})

        if user := ExtendedUser.get_user_by_username(username):
            serializer = ExtendedUserSerializer(user)
            data["data"] = serializer.data
            return Response(data, status=HTTP_200_OK)

        data["error"] = "user not found"
        return Response(data, status=HTTP_404_NOT_FOUND)


class UserCheckAPI(APIView):

    def post(self, request, *args, **kwargs):
        data = dict({'data': '', 'error': ''})

        try:
            phone_number = request.data["phone_number"]
        except KeyError:
            data["error"] = "wrong field"
            return Response(data, status=HTTP_400_BAD_REQUEST)

        if user := ExtendedUser.get_user_by_phone(phone_number):
            data["data"] = {"status": "ok", "phone_number": phone_number}
            return Response(data, status=HTTP_200_OK)

        data["data"] = {"status": "nok"}
        data["error"] = "user not found"
        return Response(data, status=HTTP_404_NOT_FOUND)


class UserLoginAPI(APIView):

    def post(self, request, *args, **kwargs):
        data = dict({'data': '', 'error': ''})

        try:
            phone_number = request.data["phone_number"]
            password = request.data["password"]
        except KeyError:
            data["error"] = "wrong field"
            return Response(data, status=HTTP_400_BAD_REQUEST)

        user = ExtendedUser.get_user_by_phone(phone_number)

        if user is None:
            data["error"] = 'user does not exist'
            return Response(data, status=HTTP_404_NOT_FOUND)

        if ExtendedUser.login_user(request, user.user, password):
            data["data"] = 'login successfully'
            return Response(data, status=HTTP_200_OK)

        data["error"] = 'incorrect password'
        return Response(data, status=HTTP_200_OK)


class UserRegisterAPI(APIView):

    def post(self, request, *args, **kwargs):
        data = dict({'data': '', 'error': ''})

        try:
            phone_number = request.data["phone_number"]
        except KeyError:
            data["error"] = "wrong field"
            return Response(data, status=HTTP_400_BAD_REQUEST)

