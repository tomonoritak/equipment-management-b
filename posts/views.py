from django.shortcuts import render
from django.views.generic import ListView
from .models import Posts

class IndexView(ListView):
    model = Posts
    template_name = 'posts/index.html'
    context_object_name = 'posts'

class itemdetailsView(ListView):
    model = Posts
    template_name = 'posts/itemdetails.html'
    context_object_name = 'itemdetails'


class itemeditView(ListView):
    model = Posts
    template_name = 'posts/itemedit.html'
    context_object_name = 'itemedit'

class itemlistView(ListView):
    model = Posts
    template_name = 'posts/itemlis.html'
    context_object_name = 'itemlis'

class itemregistrationView(ListView):
    model = Posts
    template_name = 'posts/itemregistration.html'
    context_object_name = 'itemregistration'


class loginView(ListView):
    model = Posts
    template_name = 'posts/login.html'
    context_object_name = 'login'
class usereditView(ListView):
    model = Posts
    template_name = 'posts/usereditView.html'
    context_object_name = 'usereditView'
class userlistView(ListView):
    model = Posts
    template_name = 'posts/userlist.html'
    context_object_name = 'userlist'
class userregistrationView(ListView):
    model = Posts
    template_name = 'posts/userregistration.html'
    context_object_name = 'userregistration'


