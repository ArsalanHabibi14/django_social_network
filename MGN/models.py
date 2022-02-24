from django.db import models
from users.models import Profile, Order
from posts.models import Posts
from django.shortcuts import redirect

class MessageOrder(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    total_message = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.owner.user_name


class Messages(models.Model):
    order = models.ForeignKey(MessageOrder, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message_text = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.user.user_name

class NotificationFollower(models.Model):
    SUBJECT_TYPE = (
        ('follow', 'Follow'),
        ('comment', 'Comment')
    )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user_following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Followuser', null=True, blank=True)
    # subject = models.CharField(max_length=120, choices=SUBJECT_TYPE)
    description = models.TextField()
    order_follower = models.ForeignKey(Order, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return self.user_following.user_name




class NotificationComment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    send_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='SendUser')
    post = models.ForeignKey(Posts, null=True,on_delete=models.SET_NULL)
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)    
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.send_user.user_name


class Activity(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, null=True, blank=True)
    activity_text = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return self.user.user_name