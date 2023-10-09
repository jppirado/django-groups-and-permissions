from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from user.models import Post

class PostListView(PermissionRequiredMixin, ListView):
    permission_required = "blog.delete_post"
    template_name = "post.html"
    model = Post

from django.contrib.auth.decorators import permission_required

# @permission_required("blog.view_post")
def post_list_view(request):
    print(dir( request.user))
    print(  )

    context = {
        'user_permissions' : request.user.get_all_permissions() , 
    }

    return render( request , 'post.html' ,  context )