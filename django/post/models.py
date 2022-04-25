from django.db import models
from django.contrib.auth.models import User
# Create your models here.,
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.urls import reverse

def user_directory_path(instance, filename):
    #this file will be uploaded to media root /user(id)/fiename
    return f'user_{instance.user.id}/{filename}'


class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tags", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        return super().save(*args, **kwargs)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=models.UUIDField4, editable=Fasle)
    picture = models.ImageField(upload_to=user_directory_path, null=False, verbose_name='Picture')
    caption = models.TextField(max_length=1500, verbose_name='Caption')
    posted = models.DateTimeFiels(auto_now_add=True)
    tags = models.ManyToManyField(Tags, related_name='tags')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField()
    

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.posted

    def get_absolute_url(self):
        return reverse("postdetails", args=[str(self.id)])


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    
class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField()


    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=psot, user=follower.follower, date=post.posted, following=user)
            stream.save()

    
