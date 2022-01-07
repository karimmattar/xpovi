from django.urls import path

from .views import LoginView, RegisterView, CSRFToken

urlpatterns = [
    path('csrf', CSRFToken.as_view()),  # Get csrf token URL
    path('login/', LoginView.as_view()),    # Post login URL
    path('register/', RegisterView.as_view()),  # Post register URL
]
