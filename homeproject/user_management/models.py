from datetime import datetime
from django.db import models
from django.contrib import admin
# Create your models here.


class CustomUser(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.CharField(unique=True, db_index=True, max_length=255)
    phoneNumber = models.CharField(max_length=20, blank=True)
    isActive = models.BooleanField(default=True)
    profilePic = models.URLField()

    def __str__(self):
        return self.name
admin.site.register(CustomUser)


class UserPosts(models.Model):
    userId = models.CharField(max_length=255, blank=False)
    postTitle = models.TextField()
    postDescription = models.TextField()
    createdAt = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.userId

    def as_dict(self):
        post = dict()
        post["userId"] = self.userId
        post["postTitle"] = self.postTitle
        post["postDes"] = self.postDescription
        post["createdAt"] = self.createdAt
        return post

admin.site.register(UserPosts)