from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='home'),
    path('register/', views.register_page, name='register'),
    path('profile/', views.profile_page, name='profile'),
    path('search/', views.search, name='search'),
    path('own_profile/followers/', views.profile_followers, name='profile_followers'),
    path('own_profile/following/', views.profile_following, name='profile_following'),
    path('view_profile/<user_id>/<user_name>/view/', views.view_profile, name='profile_view'),
    path('view_profile/<user_id>/<user_name>/view/followers', views.followers,
         name='profile_view_followers'),
    path('view_profile/<user_id>/<user_name>/view/following', views.following,
         name='profile_view_following'),
    path('logout/', views.logoutUser, name='logout'),
    path('update-profile/', views.updateProfile, name='update_user'),
    path('about/', views.about_page, name='about-user'),
    path('add_latest_search/<user_view_id>', views.add_latest_search, name='add_latest_search'),
    path('right/', views.right_bar, name='right_bar'),
    path('header/', views.header, name='header'),

]
