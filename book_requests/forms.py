from django import forms


class ApproveRequestForm(forms.Form):

    pickup_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control flatpickr-date",
                "placeholder": "Select Pickup Date",
                "autocomplete": "off",
            }
        )
)

    pickup_time = forms.TimeField(
        input_formats=[
            "%I:%M %p",   # 02:30 PM
            "%H:%M",      # 14:30
        ],
        widget=forms.TimeInput(
            attrs={
                "class": "form-control flatpickr-time w-100",
                "style": "width:100%;",
                "placeholder": "Select Pickup Time",
                "autocomplete": "off",
            }
        ),
    )

    librarian_message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4}),
        required=False,
    )




class RejectRequestForm(forms.Form):

    rejection_reason = forms.CharField(
        label="Reason for rejection",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Explain why this request is being rejected..."
            }
        )
    )