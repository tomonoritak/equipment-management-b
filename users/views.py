from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, UserEditForm 
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404

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
    form_class = UserEditForm
    template_name = 'users/useredit.html'
    success_url = reverse_lazy('users:userlist')

    def get_object(self, queryset=None):
        # get_object_or_404 を使用してオブジェクトを取得
        return get_object_or_404(User, pk=self.kwargs['pk'])
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # ログイン中のユーザーをフォームに渡す
        return kwargs

    def form_valid(self, form):
        if form.cleaned_data.get('delete_user'):  # チェックボックスがオンならユーザーを削除
            self.get_object().delete()
            return redirect(self.success_url)  # 削除後はユーザー一覧にリダイレクト

        return super().form_valid(form)

   
