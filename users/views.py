from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, UserEditForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

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
        return get_object_or_404(User, pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = PasswordChangeForm(user=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = UserEditForm(request.POST, instance=self.object)
        password_form = PasswordChangeForm(user=self.object, data=request.POST)

        if 'change_password' in request.POST:
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # パスワード変更後もログイン状態を維持
                messages.success(request, "パスワードを変更しました")  # メッセージを追加
                return redirect(self.success_url)
            else:
                return self.render_to_response(self.get_context_data(user_form=user_form, password_form=password_form))

        elif 'update_user' in request.POST:
            if user_form.is_valid():
                user_form.save()
                return redirect(self.success_url)
            else:
                return self.render_to_response(self.get_context_data(user_form=user_form, password_form=password_form))

        # フォームが無効な場合は、再度テンプレートに戻す
        return self.render_to_response(self.get_context_data(user_form=user_form, password_form=password_form))

    def form_valid(self, form):
        if form.cleaned_data.get('delete_user'):
            self.object.delete()
            return redirect(self.success_url)
        return super().form_valid(form)



   
