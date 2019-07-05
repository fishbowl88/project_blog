from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from blog.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

# Post section


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self): #Adds more customization to the returned data
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            # pretty much a sql query. Pulls all the post objects and filters them by
            # published date that is less than or equal (__lte) to now in the current
            # time zone. Then orders by publication date in decending order (-published_date)
            # Called a field lookup in django


class PostDetailView(DetailView):
    model = Post

                    # Means you need to be logged in to see this view
class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
        # the form thats going to be used to creat a post
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'blog/host_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=post.pk)

# Comment section


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST': # if the form was submitted, then do the following
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:   #if the form has not been submitted, return the form
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve() # simply calling a function of the comment model
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk # this is done to save the post pk, cuz we need it in the
                                # redirect after the comment.delete
    comment.delete()
    return redirect('post_detail', pk=post_pk)



