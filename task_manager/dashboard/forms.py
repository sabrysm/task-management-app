from django import forms
from .models import Task, Category
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = False
        
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control rounded-md p-1 font-light text-[#9abad8] bg-[#0d1c2a] outline-none md:w-full',
                    'placeholder': 'Add a category..',
                }
            )
        }

class NewTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = False
        
    class Meta:
        model = Task
        fields = ['title']
        
        placeholder = {
            'title': 'Add a task..',
        }
        
        
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control rounded-md p-1 font-light text-[#9abad8] bg-[#0d1c2a] outline-none w-[93%] md:w-full',
                    'placeholder': 'Add a task..',
                    }
                )
        }