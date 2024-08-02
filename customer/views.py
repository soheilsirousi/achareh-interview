from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

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
            data["data"] = {"status": "ok"}
            return Response(data, status=HTTP_200_OK)
        data["data"] = {"status": "nok"}
        data["error"] = "user not found"
        return Response(data, status=HTTP_404_NOT_FOUND)
