from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from post.models import Post, Stream, Tag
from django.template import loader
from django.http import HttpResponse
from post.forms import NewPostForm

#class base view
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
#===============================================================
# @login_required
# def index(request):
#     user = request.user
#     posts = Stream.objects.filter(user=user)
    
#     group_ids = []
#     for post in posts:
#         group_ids.append(post.post.id)
    
#     post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
#     tempale = loader.get_template('index.html')

#     context = {
#         'post_items': post_items
#     }
#     return HttpResponse(tempale.render(context, request))

#class baseview for index
class IndexView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    context_object_name = 'post_items'
    
    def get_queryset(self):
        
        self.posts = Stream.objects.filter(user=self.request.user)
    
        self.group_ids = []
        for post in self.posts:
            self.group_ids.append(post.post.id)
        
        return Post.objects.filter(id__in=self.group_ids).all().order_by('-posted')
    



#==============================================================
@login_required
def newPost(request):
    user = request.user.id
    tags_objs = []
    if request.method == "post":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get['picture']
            caption = form.cleaned_data.get['caption']
            tags_form = form.cleaned_data.get['tags']
            tags_list = list(tags_form.split(','))
            print(picture)
            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            p.tags.set(tags_objs)
            p.save()
            return redirect('index')
    else:
        form = NewPostForm()
    
    context = {
        'form': form
    }

    return render(request, 'newpost.html', context)

