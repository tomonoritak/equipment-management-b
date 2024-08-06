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
