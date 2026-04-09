from django import forms
from .models import CelebrityEndorsement


class CelebrityEndorsementForm(forms.ModelForm):
    class Meta:
        model = CelebrityEndorsement
        fields = [
            'name',
            'title',
            'image',
            'quote',
            'cause',
            'is_active',
            'display_order'
        ]