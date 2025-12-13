from django.urls import path
from .views import VerifyEmailView


urlpatterns = [
    path('verify-email/<uuid:token>/', VerifyEmailView.as_view()),
]
