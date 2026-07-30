from django import forms
from .models import BookRecommendation


class BookRecommendationForm(forms.ModelForm):

    class Meta:

        model = BookRecommendation

        fields = [
            "title",
            "author",
            "publisher",
            "isbn",
            "edition",
            "category",
            "language",
            "approximate_price",
            "reason",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Book Title",
                }
            ),

            "author": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Author Name",
                }
            ),

            "publisher": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Publisher (Optional)",
                }
            ),

            "isbn": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ISBN (Optional)",
                }
            ),

            "edition": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Edition (Optional)",
                }
            ),

            "category": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Category (Optional)",
                }
            ),

            "language": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Language (Optional)",
                }
            ),

            "approximate_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Approximate Price (Optional)",
                }
            ),

            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Reason for Recommendation (Optional)",
                }
            ),
        }