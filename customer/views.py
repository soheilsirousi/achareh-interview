from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, \
    HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from customer.utils.messages import create_otp, send_message
from customer.models import ExtendedUser, Block
from customer.serializers import ExtendedUserSerializer
import datetime
from django.utils import timezone


class UserRetrieveAPI(APIView):

    def get(self, request, username, *args, **kwargs):
        print(request.META.get('REMOTE_ADDR'))
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
            data["data"] = {"registered": True, "phone_number": phone_number}
            return Response(data, status=HTTP_200_OK)

        otp = create_otp()
        request.session["otp"] = otp
        # send_message(phone_number, str(otp)) -> send otp code on message
        data["data"] = {"registered": False, "otp": otp}
        return Response(data, status=HTTP_200_OK)


class UserLoginAPI(APIView):

    def post(self, request, *args, **kwargs):
        session = request.session
        data = dict({'data': '', 'error': ''})

        try:
            phone_number = request.data["phone_number"]
            password = request.data["password"]
        except KeyError:
            data["error"] = "wrong field"
            return Response(data, status=HTTP_400_BAD_REQUEST)

        ip = request.META.get('REMOTE_ADDR')
        if Block.is_user_block(ip_address=ip, phone_number=phone_number):
            data["error"] = 'attempt too much, try again later'
            return Response(data, status=HTTP_403_FORBIDDEN)

        if session.get("attempt", 0) > 2:
            Block.block_user(phone_number, ip, timezone.now() + datetime.timedelta(hours=1))

        user = ExtendedUser.get_user_by_phone(phone_number)

        if user is not None:
            if ExtendedUser.login_user(request, user.user, password):
                session["attempt"] = 0
                data["data"] = 'login successfully'
                return Response(data, status=HTTP_200_OK)

        try:
            session["attempt"] += 1
        except KeyError:
            session["attempt"] = 1
            session.set_expiry(60)

        print(session["attempt"])
        data["error"] = 'incorrect username or password'
        return Response(data, status=HTTP_200_OK)


class UserRegisterAPI(APIView):

    def post(self, request, *args, **kwargs):
        session = request.session
        data = dict({'data': '', 'error': ''})

        try:
            phone_number = request.data["phone_number"]
            user_otp = request.data["otp"]
        except KeyError:
            data["error"] = "wrong field"
            return Response(data, status=HTTP_400_BAD_REQUEST)

        try:
            otp = request.session.get("otp")
        except KeyError:
            data["error"] = "invalid otp"
            return Response(data, status=HTTP_400_BAD_REQUEST)

        ip = request.META.get('REMOTE_ADDR')
        if Block.is_user_block(ip_address=ip, phone_number=phone_number):
            data["error"] = 'attempt too much, try again later'
            return Response(data, status=HTTP_403_FORBIDDEN)

        if session.get("attempt", 0) > 2:
            Block.block_user(phone_number, ip, timezone.now() + datetime.timedelta(hours=1))

        if ExtendedUser.objects.filter(phone_number=phone_number).exists():
            data["error"] = "user is already exist"
            return Response(data, status=HTTP_200_OK)

        if user_otp == otp:
            user = ExtendedUser.register_user(request, phone_number)
            serializer = ExtendedUserSerializer(user)
            data["data"] = serializer.data
            return Response(data, status=HTTP_201_CREATED)

        try:
            session["attempt"] += 1
        except KeyError:
            session["attempt"] = 1
            session.set_expiry(60)

        data["error"] = "invalid otp code"
        return Response(data, status=HTTP_200_OK)


class UserInfoAPI(APIView):

    def post(self, request, *args, **kwargs):
        data = dict({'data': '', 'error': ''})

        try:
            phone_number = request.data["phone_number"]
            first_name = request.data["first_name"]
            last_name = request.data["last_name"]
            email = request.data["email"]
            password = request.data["password"]
        except KeyError:
            data["error"] = "wrong field"
            return Response(data, status=HTTP_400_BAD_REQUEST)

        user = ExtendedUser.save_user_info(phone_number, email, first_name, last_name, password)
        if user is None:
            data["error"] = "user does not exist"
            return Response(data, status=HTTP_400_BAD_REQUEST)

        serializer = ExtendedUserSerializer(user)
        data["data"] = serializer.data
        return Response(data, status=HTTP_200_OK)
