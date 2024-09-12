from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (CustomLoginView, SignUpView, CustomPasswordResetView, PasswordResetConfirmView, UserListView, UserEditView)

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('userlist/', UserListView.as_view(), name='userlist'),
    path('useredit/<int:pk>/', UserEditView.as_view(), name='useredit'),
]

