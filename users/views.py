from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic import ListView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('Posts:itemlist')  # ログイン成功後のリダイレクト先を指定


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')  # 登録成功後にログインページにリダイレクト
    template_name = 'users/userregistration.html' 

    def form_valid(self, form):
        # フォームの保存
        user = form.save(commit=False)
        user.is_staff = form.cleaned_data.get('is_staff')
        user.is_superuser = form.cleaned_data.get('is_superuser')
        user.save()
        
        return super().form_valid(form)
    
class UserListView(ListView):
    model = User
    template_name = 'users/userlist.html'
    context_object_name = 'users'

class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/useredit.html'
    fields = ['username', 'email', 'is_staff', 'is_superuser']  # 編集したいフィールドを指定
    success_url = reverse_lazy('users:userlist')  # 保存後にユーザー一覧にリダイレクト

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.kwargs['pk'])  # プライマリキーでユーザーを取得
