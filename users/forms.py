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
        help_text='最低8文字以上、数字、記号を含むパスワードを入力してください。'
    )
    password2 = forms.CharField(
        label='パスワード（確認用）',
        widget=forms.PasswordInput,
        help_text='パスワードを再度入力してください。'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # デフォルトのフィールドをカスタマイズ
        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].label = 'パスワード（確認用）'



