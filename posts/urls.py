from django.urls import path
from .views import IndexView, itemCreateView, itemlistView, itemDetailView

app_name = 'Posts'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('itemlist/', itemlistView.as_view(), name='itemlist'),
    path('itemlist/create/', itemCreateView.as_view(), name='itemregistration'),    
    path('itemlist/<int:pk>/', itemDetailView.as_view(), name='itemdetail'),
]