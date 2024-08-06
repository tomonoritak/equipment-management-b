from django.urls import path
from .views import IndexView,itemdetailsView,itemeditView,itemlistView,itemregistrationView,loginView,usereditView,userlistView,userregistrationView

app_name = 'Posts'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('posts/itemdetails/', itemdetailsView.as_view(), name='itemdetails'),
    path('posts/itemedit/', itemeditView.as_view(), name='itemedit'),
    path('posts/itemlist/', itemlistView.as_view(), name='itemlist'),
    path('posts/itemregistration/', itemregistrationView.as_view(), name='itemregistration'),

    path('users/login/', loginView.as_view(), name='login'),
    path('users/useredit/', usereditView.as_view(), name='useredit'),
    path('users/userlist/', userlistView.as_view(), name='userlist'),
    path('users/userregistration/', userregistrationView.as_view(), name='userregistration'),
]