from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:article_id>/', views.detail , name='detail' ),
    path('<int:article_id>/<str:nickname>/add_comment/', views.add_comment , name='add_comment' ),
    path('profile<int:user_id>/', views.profile , name='profile' ),
    path('register/', views.register , name='register' ),
    path('search/', views.search , name='search' ),
    path('add_article_list/<int:article_id>', views.add_article_list , name='add_article_list' ),
    path('featured_article/<int:user_id>', views.featured_article , name='featured_article' ),
    
]