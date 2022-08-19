from authemail import views as auth_views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "users"
urlpatterns = [
    path('signup/', views.RegisterUserAPIView.as_view(), name='authemail-signup'),
    path('signup/verify/', auth_views.SignupVerify.as_view(),
         name='authemail-signup-verify'),

    path('password/reset/', auth_views.PasswordReset.as_view(),
         name='authemail-password-reset'),
    path('password/reset/verify/', auth_views.PasswordResetVerify.as_view(),
         name='authemail-password-reset-verify'),
    path('password/reset/verified/', auth_views.PasswordResetVerified.as_view(),
         name='authemail-password-reset-verified'),

    path('email/change/', auth_views.EmailChange.as_view(),
         name='authemail-email-change'),
    path('email/change/verify/', auth_views.EmailChangeVerify.as_view(),
         name='authemail-email-change-verify'),

    path('password/change/', auth_views.PasswordChange.as_view(),
         name='authemail-password-change'),

    path('me/', views.RetrieveUpdateCurrentUserAPIView.as_view(), name='authemail-me'),
    path('token/', views.NewTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('pass/training/', views.UpdateUserActivityAPIView.as_view(), name='token_refresh'),
]
