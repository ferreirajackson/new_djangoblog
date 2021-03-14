from django import forms
from blogapp.models import Post, Newsletter, Contato
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import Textarea


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(required=True, max_length=100)

    class Meta:
        fields=('email','first_name', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'email Address'


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')

        widgets = {
            'test': Textarea(attrs={'cols': 80, 'rows': 10}),
        }

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ('email',)


class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ('NameContato','EmailContato','PhoneContato','MensagemContato')
