from django.urls import path
from .views import LoginView, ResetPwdView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('resetpwd', ResetPwdView.as_view()),
]
