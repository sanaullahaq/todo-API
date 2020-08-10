from django.forms import ModelForm
from .models import Todo

'''
Here the inner class defines what kind of models form we want and what what fields we want
'''


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']
