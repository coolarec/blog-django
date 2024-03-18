# blog/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # 设置默认作者ID为1
    content = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', related_name='posts')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='posts')
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    summary = models.TextField(blank=True)
    authorname = models.CharField(max_length=100,default="")
    class Meta:
        ordering = ['-created_at']  # 根据创建时间降序排序
    def __str__(self):
        return self.title
    

class Tag(models.Model):
    name = models.CharField(max_length=50 ,blank=True,default='')
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50,blank=True,default='')
    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50, default="Anonymous")
    email = models.EmailField(blank=True,default='')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['created_at']  # 根据创建时间升序排序
    def __str__(self):
        return f'Comment by {self.author} ({self.email}) on {self.post.title}'
