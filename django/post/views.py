from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from post.models import Post, Stream
from django.template import loader
from django.http import HttpResponse

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
