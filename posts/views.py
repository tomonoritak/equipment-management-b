from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView,CreateView,DetailView,UpdateView
from django.urls import reverse_lazy
from .models import Posts
from .forms import PostForm,StockQuantityForm
from django.urls import reverse
from django.contrib import messages
from django.views.generic.edit import FormView


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
    
class StockQuantityUpdateView(FormView):
    form_class = StockQuantityForm
    template_name = 'posts/itemdetail.html'

    def form_valid(self, form):
        post = get_object_or_404(Posts, pk=self.kwargs['pk'])
        new_stock_quantity = form.cleaned_data['stock_quantity']
        post.stock_quantity = new_stock_quantity
        post.save()
        
        # Optionally, save stock change history here

        messages.success(self.request, "在庫数が更新されました。")
        return redirect('Posts:itemdetail', pk=post.pk)
    
    def form_invalid(self, form):
        messages.error(self.request, "フォームにエラーがあります。")
        return self.form_invalid(form)
