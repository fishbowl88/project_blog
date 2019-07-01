from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey('auth.User')
        # Connects a post to a user
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
            # Sets the date when the post is published

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
            # returns only the approved comments associated with this post

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})
            # After a post is created, go to a post detail page for the post
            # that was just created. Passes a dict with the pk

    def __str__(self):
        return self.title
            # sets the .name to the title of the post


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
        # Connects the comment to a blog post
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)
        # Dictates wether a comment has been approved or not. False at comment creation

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')
            # When a comment is approved, take us back to the main post list page

    def __str__(self):
        return self.text









