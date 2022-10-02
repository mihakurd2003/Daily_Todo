from django.forms import ModelForm
from .models import Todo


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'body', 'is_important']