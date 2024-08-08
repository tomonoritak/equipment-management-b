from django.urls import path
from .views import IndexView, itemCreateView, itemlistView, itemDetailView, itemeditView,orderhistoryView

app_name = 'Posts'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('itemlist/', itemlistView.as_view(), name='itemlist'),
    path('itemlist/orderhistory/', orderhistoryView.as_view(), name='orderhistory'),
    path('itemlist/create/', itemCreateView.as_view(), name='itemregistration'),    
    path('itemlist/<int:pk>/', itemDetailView.as_view(), name='itemdetail'),
    path('itemlist/<int:pk>/edit', itemeditView.as_view(), name='itemedit'),
]