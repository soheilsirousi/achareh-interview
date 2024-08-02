from django.urls import path
from customer.views import UserRetrieveAPI, UserCheckAPI

urlpatterns = [
    path('<str:username>/', UserRetrieveAPI.as_view(), name='user-retrieve'),
    path('login/check/', UserCheckAPI.as_view(), name='user-check')
]
