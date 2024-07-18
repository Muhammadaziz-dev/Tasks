from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'completed']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError('Title is required.')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError('Description is required.')
        return description

    def clean_priority(self):
        priority = self.cleaned_data.get('priority')
        if priority is None:
            raise forms.ValidationError('Priority is required.')
        return priority
