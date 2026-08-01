from django import forms
from .models import LibraryItem


class BookSearchForm(forms.Form):

    query = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "id": "search-box",
                "class": "form-control",
                "placeholder": "🔍 Search by Accession Number, Title, Author, Category or Publisher",
                "autocomplete": "off",
            }
        ),
    )

class BookForm(forms.ModelForm):

    class Meta:

        model = LibraryItem

        fields = [
            "accession_number",
            "serial_number",
            "title",
            "author",
            "publisher",
            "category",
            "publication_year",
            "pages",
            "price",
            "volume_qty",
            "source",
            "acquisition_type",
            "donor",
            "location",
            "remarks",
            "status",
        ]

        widgets = {
            "remarks": forms.Textarea(
                attrs={"rows": 3}
            ),

            "publication_year": forms.NumberInput(),
            "pages": forms.NumberInput(),
            "price": forms.NumberInput(),
        }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        # Status is automatic, librarian does not choose it
        self.fields["status"].required = False


    def save(self, commit=True):

        book = super().save(commit=False)

        if not book.status:
            book.status = "available"

        if commit:
            book.save()

        return book