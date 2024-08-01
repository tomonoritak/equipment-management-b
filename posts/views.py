from django.shortcuts import render
from django.views.generic import ListView
from .models import Posts

class IndexView(ListView):
    model = Posts
    template_name = 'posts/index.html'
    context_object_name = 'posts'