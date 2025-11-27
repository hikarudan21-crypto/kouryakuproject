from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin', admin.site.urls),         # 管理画面
    path('', include('kouryaku.urls')),   # 攻略アプリ
    path('', include('accounts.urls')),   # 認証アプリ
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)