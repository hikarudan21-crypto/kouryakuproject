from django.contrib import admin
from .models import Category, kouryaku
from .models import Contact

  # PhotoPost → Zyouhou に変更

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

class KouryakuAdmin(admin.ModelAdmin):  # PhotoPostAdmin → ZyouhouAdmin に変更
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

admin.site.register(Category, CategoryAdmin)
admin.site.register(kouryaku, KouryakuAdmin) 
admin.site.register(Contact)
