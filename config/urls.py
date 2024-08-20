from django.conf import settings
from django.conf.urls.static import static
#from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', include('posts.urls', namespace='Posts')), 
    path('users/', include('users.urls',namespace='users')),
    path('logout/', LogoutView.as_view(next_page='Posts:index'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)