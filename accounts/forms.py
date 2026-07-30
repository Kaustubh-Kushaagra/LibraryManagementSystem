from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django.core.validators import RegexValidator


class CustomSetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({
                "class": "form-control",
            })


class CustomPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter your registered email",
        })

class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control form-control-lg",
            "placeholder": "Enter username",
        })

        self.fields["password"].widget.attrs.update({
            "class": "form-control form-control-lg",
            "placeholder": "Enter password",
        })

    def clean(self):

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        User = get_user_model()

        try:
            user = User.objects.get(username=username)

            if not user.is_active:
                raise ValidationError(
                    "Your account has been deactivated. Please contact the library administrator."
                )

        except User.DoesNotExist:
            pass

        self.user_cache = authenticate(
            self.request,
            username=username,
            password=password,
        )

        if self.user_cache is None:
            raise ValidationError(
                "Please enter a correct username and password."
            )

        self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserRegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    phone = forms.CharField(
        required=True,
        max_length=10,
        min_length=10,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="Phone number must contain exactly 10 digits."
            )
        ],
        widget=forms.TextInput(
            attrs={
                "placeholder": "9876543210",
                "maxlength": "10",
                "inputmode": "numeric",
                "oninput": "this.value=this.value.replace(/[^0-9]/g,'').slice(0,10)"
            }
        ),
    )

    employee_id = forms.CharField(required=False)

    designation = forms.CharField(required=False)

    department = forms.CharField(required=False)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "employee_id",
            "designation",
            "department",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Keep these optional
        self.fields["employee_id"].required = False
        self.fields["designation"].required = False
        self.fields["department"].required = False

        # Bootstrap styling
        for name, field in self.fields.items():

            css = "form-control"

            if self.errors.get(name):
                css += " is-invalid"

            field.widget.attrs["class"] = css

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get("employee_id")

        if not employee_id:
            return None

        return employee_id


class EditProfileForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "profile_picture",
            "first_name",
            "last_name",
            "email",
            "phone",
            "employee_id",
            "designation",
            "department",
            "address",
        ]

        widgets = {

            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),

            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "employee_id": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "designation": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "department": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "profile_picture": forms.FileInput(
                attrs={"class": "form-control"}
            ),

        }