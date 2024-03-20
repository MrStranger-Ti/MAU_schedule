from django import forms


class NoteForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(), label='Текст заметки')
