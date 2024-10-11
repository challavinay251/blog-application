from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/new/', views.create_post, name='create_post'),
    path('like/<int:pk>/', views.like_post, name='like-post'),# Like URL
    path('post/<int:pk>/comment/', views.post_detail, name='add-comment'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('comment/<int:comment_id>/reply/', views.reply_comment, name='reply_comment'),

]
