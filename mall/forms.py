from django import forms
from .models import Stuff
from .models import Comment

class StuffForm(forms.ModelForm):
    class Meta:
        model = Stuff
        fields = ['name', 'price', 'detail', 'stock', 'image']  # 재고 포함
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'image':forms.FileInput(attrs = {"id" : "image_field",'class':'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': '댓글을 작성하세요...'}),
        }