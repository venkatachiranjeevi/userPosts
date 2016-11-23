from datetime import datetime
import json
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView, View
from oauth2client import client, crypt
from rest_framework.response import Response
from rest_framework.views import APIView
from homeproject.settings import GOOGLE_CLIENT_ID
from user_management.models import UserPosts, CustomUser
from user_management.utils import get_user_posts


class HomePageView(TemplateView):

    template_name = "home.html"

    def get(self, request, **kwargs):
        if 'userId' in request.session:
            userId = request.session.get("userId")
            return get_user_posts(request, "userPosts.html", userId)

        return render(request, self.template_name)


class UserPostsView(TemplateView):
    template_name = "userPosts.html"

    def dispatch(self, request, *args, **kwargs):
        return super(UserPostsView, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        if 'userId' not in request.session:
            return render(request, "home.html")
        id = request.session.get('userId')
        return get_user_posts(request, self.template_name, id)

    def get_user_post(self, request, id):
        user_posts = UserPosts.objects.filter(userId=id)
        return render(request, self.template_name, {'posts': user_posts})


class AddPostView(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AddPostView, self).dispatch(request, *args, **kwargs)

    model = UserPosts
    def post(self, request):
        if 'userId' not in request.session:
            raise Exception({"Error": "Invalid User"})
        id = request.session.get('userId')
        createdAt = datetime.now()
        UserPosts(userId = id,
                  postTitle =request.POST.get("postTitle"),
                  postDescription =request.POST.get("postDes"),
                  createdAt = createdAt).save()
        post = {'postTitle': request.POST.get("postTitle"), 'postDes': request.POST.get("postDes"), 'createdAt': createdAt}
        return Response(post, 200)


class GoogleLoginView(APIView):

    def dispatch(self, request, *args, **kwargs):
        return super(GoogleLoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request, format=None):
        data = json.loads(request.body)
        try:
            idinfo = client.verify_id_token(data.get('token'), GOOGLE_CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
            return self.get_user_post(request, idinfo)
        except crypt.AppIdentityError:
            pass


    def get_user_post(self, request, user_details):
        user, created = CustomUser.objects.get_or_create(name=user_details.get("name"), email=user_details.get("email"),
                                                         phoneNumber=user_details.get("mobile","none"),
                                                         profilePic=user_details.get("picture"))
        request.session['userId'] = user.id
        return Response({'userId': user.id}, 200)

