from user_management.models import UserPosts, CustomUser
from django.shortcuts import render

__author__ = 'customfurnish'


def get_user_posts(request, template_name, id):
    user_posts = UserPosts.objects.filter(userId=id).order_by('createdAt')
    user = CustomUser.objects.get(id=id)
    return render(request, template_name, {'posts': user_posts, 'user':user, 'csrf': request.COOKIES.get('csrftoken')})