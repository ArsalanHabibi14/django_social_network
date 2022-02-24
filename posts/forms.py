from django import forms
from .models import Posts


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'user', 'post_text', 'file']
        widgets = {
            'user': forms.HiddenInput()
        }


class CommentForm(forms.Form):
    comment_text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'Leave Your Comment'})
    )
