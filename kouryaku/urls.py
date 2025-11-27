from django.urls import path
from . import views
from django.views.generic import TemplateView


app_name='kouryaku'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/', views.CreateKouryakuView.as_view(), name='post'),
    path('post_done/', views.PostSuccessView.as_view(), name='post_done'),
    path('category/<int:category_id>/', views.kouryaku_by_category, name='kouryaku_cat'),
    path('categories/', views.category_list, name='category_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('kouryaku-detail/<int:pk>/', views.KouryakuDetailView.as_view(), name='kouryaku_detail'),
    path('kouryaku/<int:pk>/delete/', views.KouryakuDeleteView.as_view(), name='kouryaku_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('search/', views.search, name='search'),
    path("contact/", views.contact, name="contact"),
    path("contact/success/", TemplateView.as_view(template_name="contact_success.html"), name="contact_success"),

]
