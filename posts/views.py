from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, DetailView, UpdateView,DeleteView
from django.urls import reverse_lazy, reverse
from .models import Posts, StockHistory
from .forms import PostForm, StockQuantityForm ,DepartmentForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

class IndexView(ListView):
    model = Posts
    template_name = 'posts/index.html'
    context_object_name = 'posts'

class itemlistView(ListView):
    model = Posts
    template_name = 'posts/itemlist.html'
    context_object_name = 'itemlist'

class orderhistoryView(ListView):
    model = StockHistory
    template_name = 'posts/orderhistory.html'
    context_object_name = 'orderhistory'

    def get_queryset(self):
        return StockHistory.objects.all().order_by('-changed_at')

class itemCreateView(CreateView):
    form_class = PostForm
    template_name = 'posts/itemregistration.html'
    success_url = reverse_lazy("Posts:itemlist")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()

        # 新しい備品が作成された際に、StockHistory にもレコードを追加
        StockHistory.objects.create(
            post=post,
            stock_quantity=post.stock_quantity,
            user=self.request.user  # ★ユーザー情報を追加
        )

        return super().form_valid(form)

class itemDetailView(DetailView):
    model = Posts
    template_name = 'posts/itemdetail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['stock_histories'] = post.stockhistory_set.order_by('-changed_at')[:10]
        return context

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

class StockQuantityUpdateView(UpdateView):
    model = Posts
    form_class = StockQuantityForm
    template_name = 'posts/itemdetail.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        
        new_stock_quantity = form.cleaned_data['stock_quantity']
        StockHistory.objects.create(
            post=self.object,
            stock_quantity=new_stock_quantity,
            user=self.request.user  # ★ユーザー情報を追加
        )
        
        return response

    def get_success_url(self):
        return reverse_lazy('Posts:itemdetail', kwargs={'pk': self.object.pk})

def approve_item(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    
    if request.method == 'POST':
        post.status = '承認'  # または適切な承認ステータス
        post.save()
        return redirect('Posts:itemdetail', pk=post.pk)
    
    return redirect('Posts:itemdetail', pk=post.pk)

class DeleteView(DeleteView):
    model = Posts
    success_url = reverse_lazy("Posts:itemlist")

# 管理者だけがアクセスできるようにするデコレーター
@user_passes_test(lambda u: u.is_superuser)
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("Posts:itemlist")  # 成功後のリダイレクト先
    else:
        form = DepartmentForm()
    return render(request, 'posts/add_department.html', {'form': form})
