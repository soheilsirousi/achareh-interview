from django.urls import path
from customer.views import UserRetrieveAPI, UserCheckAPI, UserLoginAPI, UserRegisterAPI, UserInfoAPI

urlpatterns = [
    path('login/', UserLoginAPI.as_view(), name='user-login'),
    path('register/', UserRegisterAPI.as_view(), name='user-register'),
    path('request/', UserCheckAPI.as_view(), name='user-check'),
    path('info/', UserInfoAPI.as_view(), name='user-info'),
    path('username/<str:username>/', UserRetrieveAPI.as_view(), name='user-retrieve'),
]
