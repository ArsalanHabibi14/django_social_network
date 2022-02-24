from django.urls import path
from . import views

urlpatterns = [
    path('message/', views.message, name='message'),
    path('message/<message_id>/', views.message_detail, name='message_detail'),
    path('select_followers/', views.select_follower, name='select_follower'),
    path('create_message/<send_user_id>', views.create_message, name='create_message'),
    path('notifications/', views.Notifications, name='notification'),
]
