from django.db import models
from users.models import Profile
import os


def get_file_path(filepath):
    basename = os.path.basename(filepath)
    name, ext = os.path.splitext(basename)
    print(ext)
    return name, ext


def upload_file(instance, filename):
    name, ext = get_file_path(filename)
    final_name = f'posts/{instance.id}-{instance.user.user_name}{ext}'
    return final_name


class Posts(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, null=True, blank=True)
    post_text = models.TextField()
    file = models.FileField(upload_to=upload_file, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def get_extension(self):
        basename = os.path.basename(str(self.file))
        name, ext = os.path.splitext(str(basename))
        return ext

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        if self.title is not None:
            return self.title
        else:
            return self.user.user_name


class Comments(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.user.user_name
