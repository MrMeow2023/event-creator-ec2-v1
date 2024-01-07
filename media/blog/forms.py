from django import forms
from django.forms import ModelForm
from .models import Post, Comment

class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['author']
        field_classes = {
            "created_on": model.created_on,
            "last_modified": model.last_modified,
        }
        labels = {
            "slug": "Subdirectory",
            "title": "Post Title"
        }

        error_messages = {
            "slug": {
                "invalid": "Enter a valid subdirectory consisting of letters, numbers, underscores or hyphens.",
                "required": "This field is required for URL subdirectory"
            }
        }

        widgets = { #set the widgets attribute of the ModelForm Meta class:
            'title':  forms.TextInput(attrs={'placeholder': 'Name'}), #Use Textinput class of forms
            'content':  forms.Textarea(attrs={'placeholder': 'Enter description here'}), 
        }

class PostComment(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['commenter', 'post']