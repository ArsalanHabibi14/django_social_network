from django.db import models
import uuid
import os
from django.contrib.auth.models import User


# Create your models here.


def get_file_path(filepath):
    basename = os.path.basename(filepath)
    name, ext = os.path.splitext(basename)
    return name, ext


def upload_file(instance, filename):
    name, ext = get_file_path(filename)
    final_name = f'users/{instance.id}-{instance.user_name}{ext}'
    return final_name


def upload_file_background(instance, filename):
    name, ext = get_file_path(filename)
    final_name = f'users/background/{instance.id}-{instance.user_name}{ext}'
    return final_name


class Profile(models.Model):
    GENDER_TYPE = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    STATUS_TYPE = (
        ('married', 'Married'),
        ('single', 'No Married'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=150)
    age = models.IntegerField(default=0)
    email = models.EmailField(max_length=200)
    about_me = models.TextField(null=True, blank=True)
    password = models.CharField(max_length=200)
    birth_day = models.DateTimeField(null=True, blank=True)
    join_date = models.DateField(auto_now_add=True, null=True, blank=True)
    gender = models.CharField(max_length=120, choices=GENDER_TYPE)
    image = models.ImageField(upload_to=upload_file, null=True, blank=True, default='user-default.png')
    background_image = models.ImageField(upload_to=upload_file_background, null=True, blank=True, default='default.jpg')
    location = models.CharField(max_length=2000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    website = models.URLField(max_length=4000, null=True, blank=True)
    PhoneNumber = models.CharField(max_length=2000, null=True, blank=True)
    birthPlace = models.CharField(max_length=400, null=True, blank=True)
    status = models.CharField(max_length=1400, choices=STATUS_TYPE, null=True, blank=True)
    facebookAccount = models.URLField(max_length=2000, null=True, blank=True)
    twitterAccount = models.URLField(max_length=2000, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user_name


class Order(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    total_follower = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.owner.user_name


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.user_name


class OrderFollowing(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    total_follower = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.owner.user_name


class OrderDetailFollowing(models.Model):
    order = models.ForeignKey(OrderFollowing, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.user_name


class Latest_Search(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='latestUser')

    def __str__(self):
        return self.owner.user_name
