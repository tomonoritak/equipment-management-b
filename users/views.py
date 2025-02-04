from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.db.models import Q
from .forms import CustomUserCreationForm, UserEditForm, CustomPasswordResetForm

# Djangoの標準のユーザーモデルを取得
User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('Posts:itemlist')

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
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

        # パスワード変更処理
        if 'change_password' in request.POST:
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, "パスワードを変更しました")
                return redirect(self.success_url)
            else:
                return self.render_to_response(self.get_context_data(user_form=user_form, password_form=password_form))

        # ユーザー情報の更新処理
        elif 'update_user' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "ユーザー情報を更新しました")
                return redirect(self.success_url)
            else:
                return self.render_to_response(self.get_context_data(user_form=user_form, password_form=password_form))

        # ユーザー削除処理
        elif 'delete_user' in request.POST:
            self.object.delete()
            messages.success(request, "ユーザーが削除されました")
            return redirect(self.success_url)

        # その他の場合（エラーハンドリング）
        return self.render_to_response(self.get_context_data(user_form=user_form, password_form=password_form))

    def form_valid(self, form):
        if form.cleaned_data.get('delete_user'):
            self.object.delete()
            return redirect(self.success_url)
        return super().form_valid(form)

class CustomPasswordResetView(View):
    template_name = 'users/password_reset.html'

    def get(self, request, *args, **kwargs):
        form = CustomPasswordResetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            try:
                user = User.objects.get(username=username, email=email)

                # パスワードリセット用のリンクを生成
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = reverse('users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                full_reset_link = request.build_absolute_uri(reset_link)

                # パスワードリセットページにリダイレクト
                return redirect(full_reset_link)

            except User.DoesNotExist:
                form.add_error(None, "ユーザーIDとメールアドレスが一致しません。")

        return render(request, self.template_name, {'form': form})

class PasswordResetDoneView(View):
    template_name = 'users/password_reset_done.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class PasswordResetConfirmView(View):
    template_name = 'users/password_reset_confirm.html'

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user=user)
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, '無効なリセットリンクです。')
            return redirect('users:password_reset')

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('users:login')
            else:
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, '無効なリセットリンクです。')
            return redirect('users:password_reset')

class PasswordResetCompleteView(View):
    template_name = 'users/password_reset_complete.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

def user_list(request):
    # 検索クエリを取得
    query = request.GET.get('q', '').strip()  # クエリの前後の空白を除去
    print(f"Search query: {query}")  # デバッグ出力: 検索クエリ

    # 検索結果の初期化
    users = []

    # 管理者かどうかを確認
    if request.user.is_superuser:
        if query:
            # 管理者の場合、すべてのユーザーから検索
            users = User.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query)
            )
        else:
            users = User.objects.all()
    else:
        # 管理者でない場合、自分の情報だけを表示
        if query:
            # 自分のユーザー名またはメールアドレスが検索クエリに一致するか確認
            if query.lower() in request.user.username.lower() or query.lower() in request.user.email.lower():
                users = [request.user]
        else:
            users = [request.user]

    print(f"Filtered users: {users}")  # デバッグ出力: フィルタリング結果

    return render(request, 'users/userlist.html', {'users': users, 'query': query})
