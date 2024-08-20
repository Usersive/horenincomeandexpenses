from .views import LoginView, LogoutView, RegistrationView, UsernameValidationView, EmailValidationView, VerificationView, RequestPasswordResetEmail, CompletePasswordReset
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .import views



urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', views.logout, name='logout'),
    path('validate-username',csrf_exempt( UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email',csrf_exempt( EmailValidationView.as_view()), name="validate-email"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name="activate"),
    
    path('reset-user-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name="reset-user-password"),
    path('reset_password', RequestPasswordResetEmail.as_view(), name='reset_password'),
    path('profile/', views.profile, name='profile'),
]
