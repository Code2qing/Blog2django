from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields=['nickname', 'email', 'url', 'text', 'is_reply', 'reply']
