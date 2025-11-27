from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from kouryaku.models import kouryaku
from django.core.paginator import Paginator



class SignUpView(CreateView):
    form_class=CustomUserCreationForm
    template_name="signup.html"
    success_url=reverse_lazy('accounts:signup_success')
    def form_valid(self, form):
        user=form.save()
        self.object=user
        return super().form_valid(form)

class SignUpSuccessView(TemplateView):
    template_name="signup_success.html"
    
@login_required
def mypage(request):
    post_list = kouryaku.objects.filter(user=request.user).order_by('-posted_at')  # 新しい順
    paginator = Paginator(post_list, 5)  # 1ページに5件表示

    page_number = request.GET.get('page')  # URLの?page=2 などを取得
    posts = paginator.get_page(page_number)

    return render(request, 'mypage.html', {
        'user': request.user,
        'posts': posts,
    })



    