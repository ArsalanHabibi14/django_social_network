from django.forms import ModelForm
from django import forms
from .models import Messages


class CreateMessageForm(ModelForm):
    class Meta:
        model = Messages
        fields = ['order', 'user', 'message_text']
        widgets = {
            'user': forms.HiddenInput(),
            'order': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CreateMessageForm, self).__init__(*args, **kwargs)
        self.fields['message_text'].widget.attrs.update(
            {'placeholder': self.fields['message_text'].label, 'class': 'form-control'})
