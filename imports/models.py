from django.db import models


class ExcelImport(models.Model):

    excel_file = models.FileField(
        upload_to="imports/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    imported = models.BooleanField(
        default=False
    )

    def __str__(self):

        return self.excel_file.name