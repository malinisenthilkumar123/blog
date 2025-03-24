from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='Comment',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
            }
        )
    )
    
    class Meta:
        model = Comment
        fields = ['content']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email 