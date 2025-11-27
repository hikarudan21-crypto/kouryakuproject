from django.forms import ModelForm
from .models import kouryaku  # PhotoPost → Zyouhou に変更
from django import forms
from .models import Comment



class KouryakuForm(ModelForm):  # PhotoPostForm → ZyouhouForm に変更（任意）
    class Meta:
        model = kouryaku  # PhotoPost → Zyouhou に変更
        fields = ['category', 'title', 'comment', 'image1', 'image2','url']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'コメントを入力してください'
            })
        }
        
class ContactForm(forms.Form):
    name = forms.CharField(label="お名前", max_length=100)
    email = forms.EmailField(label="メールアドレス")
    message = forms.CharField(label="お問い合わせ内容", widget=forms.Textarea)
        
        