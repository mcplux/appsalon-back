from django import forms

class BulkAddForm(forms.Form):
    data = forms.CharField(
        widget=forms.Textarea,
        help_text="Enter multiple records, each on a new line in the format: name,price."
    )
