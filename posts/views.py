from django.shortcuts import render
from django.views.generic import ListView,CreateView,DetailView,UpdateView
from django.urls import reverse_lazy
from .models import Posts
from .forms import PostForm
from django.urls import reverse

class IndexView(ListView):
    model = Posts
    template_name = 'posts/index.html'
    context_object_name = 'posts'

class itemlistView(ListView):
    model = Posts
    template_name = 'posts/itemlist.html'
    context_object_name = 'itemlist'

class orderhistoryView(ListView):
    model = Posts
    template_name = 'posts/orderhistory.html'
    context_object_name = 'orderhistory'


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

class itemeditView(UpdateView):
    model = Posts
    form_class = PostForm
    template_name = 'posts/itemedit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Posts:itemdetail', kwargs={'pk': self.object.pk})
