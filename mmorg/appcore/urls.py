from django.urls import path, include
from .views import activation, PostsList, PostsDetail, PostCreate, PostUpdate, PostDelete, CommentCreate, CommentsList, CommentAccept, CommentDelete

urlpatterns = [
   path('activation/', activation, name='activation'),
   path('posts/', PostsList.as_view(), name= 'posts_list'),
   #path('posts/search/', PostsListSearch.as_view(), name= 'posts_search'),
   path('posts/<int:pk>/', PostsDetail.as_view(), name= 'posts_detail'),
   path('posts/create/', PostCreate.as_view(), name='post_create'),
   path('posts/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('posts/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('comments/', CommentsList.as_view(), name= 'comments_list'),
   path('comments/create/', CommentCreate.as_view(), name='post_create'),
   path('comments/update/<int:pk>/', CommentAccept.as_view(), name='comment_accept'),
   path('comments/delete/<int:pk>/', CommentDelete.as_view(), name='comment_delete'),

]



