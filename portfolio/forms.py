from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Champ piège invisible : un humain le laisse vide, un robot le remplit.
    website = forms.CharField(required=False)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]

    def is_spam(self):
        return bool(self.cleaned_data.get("website"))
