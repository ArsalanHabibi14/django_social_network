from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListView, name='posts'),
    path('add_post/', views.add_post, name='add_post'),
    path('post/<post_id>/<post_name>/', views.post_detail, name='post_detail'),
    path('delete_post/<post_id>', views.delete_post, name='post_delete'),
]
