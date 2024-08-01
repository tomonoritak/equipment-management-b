from django.db import models

class Posts(models.Model):
  class Meta:
    db_table = 'posts'

  name = models.CharField(max_length=10)
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)