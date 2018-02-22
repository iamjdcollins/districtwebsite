from django import forms

from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):

    class Meta:
        model = ContactMessage
        fields = ('your_name', 'your_email', 'message_subject', 'your_message', 'our_message', 'parent','primary_contact',)

    def __init__(self, *args, **kwargs):
        super(ContactMessageForm, self).__init__(*args, **kwargs)
        self.fields['your_message'].widget.attrs.update({'class' : 'materialize-textarea'})
        self.fields['our_message'].widget.attrs.update({'class' : 'materialize-textarea'})
        self.fields['parent'].widget = forms.HiddenInput()
        self.fields['primary_contact'].widget = forms.HiddenInput()
