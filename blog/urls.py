from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    # pk means primary key type int
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'), # template expected to be name of model_form.html
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), #will use same post_form template
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), # template used is post_confirm_delete.html
]

# class based views look for template in <app>/<model>_<viewtype>.html
