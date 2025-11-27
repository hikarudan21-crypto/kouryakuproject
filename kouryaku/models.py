from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    title = models.CharField(
        verbose_name='カテゴリ',
        max_length=20
    )

    def __str__(self):
        return self.title

class kouryaku(models.Model):  # PhotoPost → Zyouhou に変更
    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリ',
        on_delete=models.PROTECT
    )
    title = models.CharField(
        verbose_name='タイトル',
        max_length=200
    )
    comment = models.TextField(
        verbose_name='コメント',
    )
    image1 = models.ImageField(
        verbose_name='イメージ1',
        upload_to='photos'
    )
    image2 = models.ImageField(
        verbose_name='イメージ2',
        upload_to='photos',
        blank=True,
        null=True
    )
    url = models.URLField(
    verbose_name='関連URL',
    blank=True,
    null=True
    )
    posted_at = models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True
    )

class Comment(models.Model):
    post = models.ForeignKey(
        kouryaku,
        verbose_name='投稿',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )
    text = models.TextField(verbose_name='コメント')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.text[:20]}'  
    

class Post(models.Model):
    title = models.CharField(max_length=200)
    comment = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title    




class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"