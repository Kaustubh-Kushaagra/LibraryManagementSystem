from django import forms
from django.contrib.auth import get_user_model

from .models import Transaction
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class IssueBookForm(forms.ModelForm):

    member = forms.ModelChoiceField(
        queryset=User.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    due_date = forms.DateField(
        label="Return Due Date",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "style": "cursor: pointer;",
                "autocomplete": "off",
            }
        )
    )

    class Meta:
        model = Transaction
        fields = (
            "member",
            "due_date",
            "remarks",
        )

        widgets = {
            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["member"].queryset = User.objects.filter(role="member")

        self.fields["due_date"].initial = (
            timezone.now().date() + timedelta(days=14)
        )

        self.fields["remarks"].initial = "Standard 14-day issue."


class ApproveReturnForm(forms.Form):

    return_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "text",
                "class": "form-control flatpickr-date",
                "placeholder": "Return Date",
            }
        )
    )

    return_time = forms.TimeField(
        input_formats=[
            "%I:%M %p",
            "%H:%M",
        ],
        widget=forms.TimeInput(
            attrs={
                "type": "text",
                "class": "form-control flatpickr-time",
                "placeholder": "Return Time",
            }
        ),
    )

    librarian_message = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Optional message for the member...",
            }
        ),
    )