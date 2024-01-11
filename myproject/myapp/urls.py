from django.urls import path, re_path
from . import views
from views import SendUserConfirmationTokenAPIView

urlpatterns = [
    path('create_user/', views.api_create_user),
    path('send-confirmation-email/', SendUserConfirmationTokenAPIView.as_view()),
    path('confirm-email/', views.confirm_email_view)
]
