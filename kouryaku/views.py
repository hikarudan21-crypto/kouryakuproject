from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView,ListView
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import KouryakuForm
from .forms import CommentForm
from .forms import ContactForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import kouryaku, Category,Contact
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.core.mail import send_mail
from django.conf import settings




class IndexView(ListView):
    template_name = 'index.html'
    queryset = kouryaku.objects.order_by('-posted_at')
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.all()
        return context



@method_decorator(login_required, name='dispatch')
class CreateKouryakuView(CreateView):
    form_class = KouryakuForm
    template_name = 'post_kouryaku.html'
    success_url = reverse_lazy('kouryaku:post_done')
    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        return super().form_valid(form)  
class PostSuccessView(TemplateView):
    template_name = 'post_success.html'       
    
class KouryakuDetailView(DetailView):
    model = kouryaku
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.all()
        return context


    
def kouryaku_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = kouryaku.objects.filter(category=category)  # ← Post → kouryaku に変更
    all_categories = Category.objects.all()
    return render(request, 'kouryaku_by_category.html', {
        'category': category,
        'posts': posts,
        'all_categories': all_categories,
    })
        
class KouryakuDeleteView(DeleteView):
    model=kouryaku
    template_name='kouryaku_delete.html'
    success_url=reverse_lazy('kouryaku:mypage')
    def delete(self,request,*args, **kwargs):
        return super().delete(request,*args, **kwargs)        

@login_required
def post_detail(request, pk):
    post = get_object_or_404(kouryaku, pk=pk)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('kouryaku:kouryaku_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'detail.html', {
        'object': post,
        'comments': comments,
        'form': form,
        'all_categories': Category.objects.all(),  # ←追加
    })


def category_list(request):
    all_categories = Category.objects.all()
    # 各カテゴリに属する投稿数を計算
    categories_with_count = []
    for cat in all_categories:
        count = kouryaku.objects.filter(category=cat).count()
        categories_with_count.append({
            'category': cat,
            'count': count,
        })
    return render(request, 'category_list.html', {
        'categories_with_count': categories_with_count,
    })

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = kouryaku.objects.filter(title__icontains=query) | kouryaku.objects.filter(comment__icontains=query)
    return render(request, 'search_results.html', {
        'query': query,
        'results': results,
        'all_categories': Category.objects.all(),  # サイドバー用
    })

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message_text = form.cleaned_data['message']

            subject = "お問い合わせが届きました"
            body = f"名前: {name}\nメール: {email}\n内容:\n{message_text}"

            # 管理者宛に送信
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,   # 送信元
                ['hikarudan21@gmail.com'],  # 送信先
            )

            return redirect("kouryaku:contact_success")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})


