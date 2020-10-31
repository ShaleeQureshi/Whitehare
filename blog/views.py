from abc import ABC

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post

# Query the posts from database
posts = Post.objects.all()


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'home.html', context)


# class based views look for template in <app>/<model>_<viewtype>.html
class PostListView(ListView):
    # Tell our list view what model to query in order to create list
    model = Post
    # class based views look for template in <app>/<model>_<viewtype>.html
    # changing the template it looks for
    template_name = 'home.html'
    # template will look for variable objectview by default to loop through, but we will change the variable to post
    context_object_name = 'posts'
    # order our posts from newest - oldest
    # change the order our query makes to the database
    ordering = ['-date_posted']
    paginate_by = 10

# class based views look for template in <app>/<model>_<viewtype>.html
class UserPostListView(ListView):
    # Tell our list view what model to query in order to create list
    model = Post
    # class based views look for template in <app>/<model>_<viewtype>.html
    # changing the template it looks for
    template_name = 'user_posts.html'
    # template will look for variable objectview by default to loop through, but we will change the variable to post
    context_object_name = 'posts'
    # order our posts from newest - oldest
    # change the order our query makes to the database
    ordering = ['-date_posted']
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user)

class PostDetailView(DetailView):
    model = Post


# LoginRequiredMixin only allows class to be used if user is logged in
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # Before submitting form, we need to override form valid method
    def form_valid(self, form):
        # set author to current logged in user
        form.instance.author = self.request.user
        # now validate the form after author is set
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Prevent from updating other people's posts
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView, ABC):
    model = Post
    success_url = '/'   # url destination when post deletion is successful

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def about(request):
    return render(request, 'about.html', {'title': 'About'})

def search(request):

    context = {
        'posts': posts
    }
    if (posts):
        messages.info(request, "Found")
        return render(request, 'user_posts.html', context)
    else:
        messages.info(request, "We couldn't find that user")
        return render(request, 'home.html', context)
        