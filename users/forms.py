from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

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




