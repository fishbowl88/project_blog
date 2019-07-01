from django.shortcuts import render
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView)
from blog.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import PostForm, CommentForm

# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self): #Adds more customization to generic views
        return Post.objects.filter(published_date__lte=timezone.now().order_by('-published_date'))
            # pretty much a sql query. Pulls all the post objects and filters them by
            # published date that is less than or equal (__lte) to now in the current
            # time zone. Then orders by publication date in decending order (-published_date)
            # Called a field lookup in django


class PostDetailView(DetailView):
    model = post

                    # Means you need to be logged in to see this view
class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
        # the form thats going to be used to creat a post
    model = Post