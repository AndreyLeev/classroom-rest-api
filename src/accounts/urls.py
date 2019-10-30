from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('accounts/', views.UserRegistrationAPIView.as_view(), name="registration"),
    path('accounts/login/', views.UserLoginAPIView.as_view(), name="login"),
     path('accounts/tokens/<key>/', views.UserTokenAPIView.as_view(), name="token"),
]