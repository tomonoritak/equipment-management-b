from django import forms
from .models import Posts, Department  # Departmentモデルをインポート
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('承認待ち', '承認待ち'),
        ('承認', '承認'),
    ]  

    CATEGORY_CHOICES = [
        ('文房具', '文房具'),
        ('電子機器', '電子機器'),
        ('その他', 'その他'),
    ]

        # department追加
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        label='所属部署',
        widget=forms.Select(attrs={'placeholder': '所属部署を選択'})
    )

    # カテゴリをプルダウンメニューに変更
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        label='カテゴリ',
        widget=forms.Select(attrs={'placeholder': 'カテゴリを選択'})
    )

    catalog_number_or_link = forms.CharField(
        label='カタログ番号orリンク',
        widget=forms.TextInput(attrs={'placeholder': 'カタログ番号またはURL'}),
        required=False
    )
    price = forms.DecimalField(
        label='金額',
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': '価格を入力'})
    )

    #fieldsとlabelsにdepartmentを追加
    class Meta:
        model = Posts
        fields = ['name', 'category', 'location', 'catalog_number_or_link', 'price', 'image', 'stock_quantity', 'status', 'user', 'department']
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
            'department': '所属部署',
        }
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # デフォルト値を設定
        if self.instance and self.instance.pk is None:
            self.fields['status'].initial = '承認待ち'
            # ユーザー選択フィールドにデフォルト値を設定（例: 最初のユーザー）
            # self.fields['user'].initial = User.objects.first()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 部署を名前順に並べ替え
        self.fields['department'].queryset = Department.objects.order_by('name')

class StockQuantityForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.order_by('name'),  # 部署を名前順に並べ替え
        required=True,
        label='発注部署',
        widget=forms.Select(attrs={'placeholder': '部署を選択してください'})
    )

    class Meta:
        model = Posts
        fields = ['stock_quantity', 'department']
        widgets = {
            'stock_quantity': forms.NumberInput(attrs={'min': 0}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        labels = {
            'name': '新規追加部署',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 名前順に並べ替え
        self.fields['name'].queryset = Department.objects.order_by('name')