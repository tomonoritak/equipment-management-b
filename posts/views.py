from django.shortcuts import render
from django.views.generic import ListView,CreateView,DetailView
from django.urls import reverse_lazy
from django.views.generic import ListView
from .models import Posts
from .forms import PostForm

class IndexView(ListView):
    model = Posts
    template_name = 'posts/index.html'
    context_object_name = 'posts'

class itemlistView(ListView):
    model = Posts
    template_name = 'posts/itemlist.html'
    context_object_name = 'itemlist'


#class itemeditView(ListView):
#    model = Posts
#    template_name = 'posts/itemedit.html'
#    context_object_name = 'itemedit'


class itemCreateView(CreateView):
    form_class = PostForm
    template_name = 'posts/itemregistration.html'
    success_url = reverse_lazy("Posts:itemlist")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return super().form_valid(form)

class itemDetailView(DetailView):
    model = Posts
    template_name = 'posts/itemdetail.html'
    context_object_name = 'post'


#class loginView(ListView):
#    model = Posts
#    template_name = 'posts/login.html'
#    context_object_name = 'login'
#class usereditView(ListView):
#    model = Posts
#    template_name = 'posts/useredit.html'
#    context_object_name = 'usereditView'
#class userlistView(ListView):
#    model = Posts
#    template_name = 'posts/userlist.html'
#    context_object_name = 'userlist'
#class userregistrationView(ListView):
#    model = Posts
#    template_name = 'posts/userregistration.html'
#    context_object_name = 'userregistration'


