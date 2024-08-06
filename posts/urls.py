from django.urls import path
from .views import IndexView,itemdetailsView,itemeditView,itemlistView,itemregistrationView

app_name = 'Posts'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('posts/itemdetails/', itemdetailsView.as_view(), name='itemdetails'),
    path('posts/itemedit/', itemeditView.as_view(), name='itemedit'),
    path('posts/itemlist/', itemlistView.as_view(), name='itemlist'),
    path('posts/itemregistration', itemregistrationView.as_view(), name='itemregistration'),
]