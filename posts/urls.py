from django.urls import path
from . import views  # viewsをインポート
from .views import IndexView, itemCreateView, itemlistView, itemDetailView, itemeditView,orderhistoryView,StockQuantityUpdateView, DeleteView

app_name = 'Posts'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('itemlist/', itemlistView.as_view(), name='itemlist'),
    path('itemlist/orderhistory/', orderhistoryView.as_view(), name='orderhistory'),
    path('itemlist/create/', itemCreateView.as_view(), name='itemregistration'),    
    path('itemlist/<int:pk>/', itemDetailView.as_view(), name='itemdetail'),
    path('itemlist/<int:pk>/edit', itemeditView.as_view(), name='itemedit'),
    path('item/<int:pk>/update_stock/', StockQuantityUpdateView.as_view(), name='stock_quantity_update'), 
    path('item/<int:pk>/approve/', views.approve_item, name='item_approve'),
    path('itemlist/<int:pk>/delete/', DeleteView.as_view(), name='delete'),  #DeleteViewを追加
    path('add_department/', views.add_department, name='department_add'),  # 所属部署追加用のURL
    ]