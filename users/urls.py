from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import UserListView, UserEditView

app_name = "users"

urlpatterns = [
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('userlist/', UserListView.as_view(), name='userlist'),
    path('useredit/<int:pk>/', UserEditView.as_view(), name='useredit'),
]

