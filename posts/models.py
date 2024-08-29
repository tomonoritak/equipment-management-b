from django.db import models
from django.contrib.auth.models import User  # ユーザーIDを参照するためにインポート

class Posts(models.Model):
    class Meta:
        db_table = 'posts'  # db_tableを'posts'に変更

    id = models.AutoField(primary_key=True)  # IDカラム
    name = models.CharField(max_length=100)  # 名前カラム（適切な最大長に変更）
    category = models.CharField(max_length=50)  # カテゴリーカラム
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    location = models.CharField(max_length=100)  # 設置場所カラム
    description = models.TextField()  # 説明カラム
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # 画像カラム（任意）
    stock_quantity = models.PositiveIntegerField()  # 在庫数カラム
    status = models.CharField(max_length=20, default='未承諾')  # デフォルト値を設定
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # ユーザーID（usersテーブルから） 

    def __str__(self):
        return self.name
    

class StockHistory(models.Model):
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()
    changed_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # ★ユーザー情報を追加