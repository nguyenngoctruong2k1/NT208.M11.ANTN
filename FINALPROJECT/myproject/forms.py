from django import forms
from myproject.models import CommentMH

class CommentMHForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.MSSV = kwargs.pop('MSSV',None)
        self.MaMH = kwargs.pop('MaMH',None)
        super().__init__(*args, **kwargs)
    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.MSSV = self.MSSV
        comment.MaMH = self.MaMH
        comment.save()
    class Meta:
        model = CommentMH 
        fields = ["NoiDung"]
