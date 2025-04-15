from django.urls import path
from personal_account.views import UserDetailApiView, UsersApiView
from personal_account.models.serializers import CustomObtainAuthToken

app_name = 'personal_account'

urlpatterns = [
    path('authtoken/', CustomObtainAuthToken.as_view()),
    path('users/', UsersApiView.as_view(), name='users'),
    path('profile/', UserDetailApiView.as_view(), name='profile'),
]
