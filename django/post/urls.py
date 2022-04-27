from django.urls import path
# from post.views import index
from post.views import IndexView

urlpatterns = [
    # path('', index, name='index'),
    path('', IndexView.as_view(), name='index'),
    
]