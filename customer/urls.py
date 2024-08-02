from django.urls import path
from customer.views import UserRetrieveAPI, UserCheckAPI, UserLoginAPI, UserRegisterAPI

urlpatterns = [
    path('login/', UserLoginAPI.as_view(), name='user-login'),
    path('register/', UserRegisterAPI.as_view(), name='user-register'),
    path('login/check/', UserCheckAPI.as_view(), name='user-check'),
    path('<str:username>/', UserRetrieveAPI.as_view(), name='user-retrieve'),
]
