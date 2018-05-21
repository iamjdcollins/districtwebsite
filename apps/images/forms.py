from django import forms
from .models import InlineImage


class InlineImageForm(forms.ModelForm):
    class Meta:
        model = InlineImage
        fields = (
            'image_file',
        )

    def __init__(self, *args, **kwargs):
        super(InlineImageForm, self).__init__(*args, **kwargs)
        self.fields['image_file'].widget.attrs.update(
            {
              'class': 'box__file',
              'data-multiple-caption': '{count} files selected',
              'multiple': '',
            }
        )