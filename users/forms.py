from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

class CustomUserCreationForm(UserCreationForm):
    is_staff = forms.BooleanField(required=False, label='スタッフとして登録する')
    is_superuser = forms.BooleanField(required=False, label='管理者として登録する')

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email', 'username', 'is_staff', 'is_superuser')

    password1 = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput,
        help_text='最低8文字以上、数字、記号を含むパスワードを入力してください。',
        error_messages={
            'required': 'パスワードを入力してください。',
            'min_length': 'パスワードは8文字以上にしてください。',
        }
    )
    password2 = forms.CharField(
        label='パスワード（確認用）',
        widget=forms.PasswordInput,
        help_text='パスワードを再度入力してください。',
        error_messages={
            'required': '確認用パスワードを入力してください。',
            'password_mismatch': 'パスワードが一致しません。',
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'ユーザー名'
        self.fields['username'].error_messages = {
            'required': 'ユーザー名を入力してください。',
            'unique': 'このユーザー名は既に使用されています。',
        }
        self.fields['email'].label = 'メールアドレス'
        self.fields['email'].error_messages = {
            'required': 'メールアドレスを入力してください。',
            'invalid': '有効なメールアドレスを入力してください。',
        }
    

class UserEditForm(forms.ModelForm):
    delete_user = forms.BooleanField(required=False, label='ユーザーを削除')  # 削除用チェックボックスを追加

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'is_staff', 'is_superuser', 'delete_user')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 'user' 引数を取得して削除
        super().__init__(*args, **kwargs)
    
        self.fields['username'].label = 'ユーザー名'
        self.fields['username'].error_messages = {
            'required': 'ユーザー名を入力してください。',
            'unique': 'このユーザー名は既に使用されています。',
        }
        self.fields['email'].label = 'メールアドレス'
        self.fields['email'].error_messages = {
            'required': 'メールアドレスを入力してください。',
            'invalid': '有効なメールアドレスを入力してください。',
        }

        # ログイン中のユーザーが管理者でない場合、削除チェックボックスを表示しない
        if user and not user.is_superuser:
            self.fields.pop('delete_user')

class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = '現在のパスワード'
        self.fields['new_password1'].label = '新しいパスワード'
        self.fields['new_password1'].help_text = '最低8文字以上、数字、記号を含むパスワードを入力してください。'
        self.fields['new_password2'].label = '新しいパスワード（確認用）'
        self.fields['new_password2'].help_text = 'パスワードを再度入力してください。'

        # エラーメッセージのカスタマイズ
        self.fields['old_password'].error_messages = {
            'required': '現在のパスワードを入力してください。',
        }
        self.fields['new_password1'].error_messages = {
            'required': '新しいパスワードを入力してください。',
            'min_length': 'パスワードは8文字以上にしてください。',
        }
        self.fields['new_password2'].error_messages = {
            'required': '確認用パスワードを入力してください。',
            'password_mismatch': 'パスワードが一致しません。',
        }


