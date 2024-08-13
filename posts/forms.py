from django import forms
from .models import Posts
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('承認待ち', '承認待ち'),
        ('承認', '承認'),
    ]   
    class Meta:
        model = Posts
        fields = ['name', 'category', 'location', 'description', 'image', 'stock_quantity', 'status', 'user']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter name'}),
            'category': forms.TextInput(attrs={'placeholder': 'Enter category'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter location'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description', 'rows': 5}),
            'image': forms.ClearableFileInput(attrs={'multiple': False}),
            'stock_quantity': forms.NumberInput(attrs={'placeholder': 'Enter stock quantity'}),
            'user': forms.Select()  # ドロップダウンリストとして表示
        }
        labels = {
            'name': 'Name',
            'category': 'Category',
            'location': 'Location',
            'description': 'Description',
            'image': 'Image',
            'stock_quantity': 'Stock Quantity',
            'status': 'Status',
            'user': 'User',
        }
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # デフォルト値を設定
        if self.instance and self.instance.pk is None:
            self.fields['status'].initial = '承認待ち'
            # ユーザー選択フィールドにデフォルト値を設定（例: 最初のユーザー）
            # self.fields['user'].initial = User.objects.first()

class StockQuantityForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['stock_quantity']
        widgets = {
            'stock_quantity': forms.NumberInput(attrs={'min': 0}),
        }