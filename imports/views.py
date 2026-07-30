from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import librarian_required
from django.contrib import messages

from audit.models import AuditLog
import os
from .forms import ExcelUploadForm
from .models import ExcelImport
from .services import analyze_excel
from .import_books import import_books
from books.forms import BookForm
from books.models import LibraryItem




@login_required
@librarian_required
def upload_excel(request):

    if request.method == "POST":

        form = ExcelUploadForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            imported_file = ExcelImport.objects.create(
                excel_file=form.cleaned_data["excel_file"],
            )

            return redirect(
                "preview_import",
                imported_file.id,
            )

    else:

        form = ExcelUploadForm()

    return render(
        request,
        "imports/upload_excel.html",
        {
            "form": form,
        },
    )


@login_required
@librarian_required
def preview_import(request, import_id):

    imported_file = get_object_or_404(
        ExcelImport,
        id=import_id,
    )

    imported_file.excel_file.open("rb")

    preview = analyze_excel(
        imported_file.excel_file,
    )

    imported_file.excel_file.close()

    return render(
        request,
        "imports/upload_excel.html",
        {
            "form": ExcelUploadForm(),
            "preview": preview,
            "imported_file": imported_file,
        },
    )


@login_required
@librarian_required
def perform_import(request, import_id):

    imported_file = get_object_or_404(
        ExcelImport,
        id=import_id,
    )

    imported_file.excel_file.open("rb")

    result = import_books(
        imported_file.excel_file,
    )

    imported_file.excel_file.close()

    AuditLog.objects.create(
        user=request.user,
        action="Excel Import",
        details=(
            f"Imported: {result['imported']} | "
            f"Skipped: {result['skipped']} | "
            f"Duplicates: {result['duplicates']}"
        ),
    )

    file_path = imported_file.excel_file.path

    imported_file.delete()

    if os.path.exists(file_path):
        os.remove(file_path)

    messages.success(
        request,
        (
            "📥 Import Completed Successfully<br><br>"
            f"✅ Books Imported: <strong>{result['imported']}</strong><br>"
            f"⏭️ Books Skipped: <strong>{result['skipped']}</strong><br>"
            f"🔁 Duplicate Books: <strong>{result['duplicates']}</strong>"
        ),
    )

    return redirect("upload_excel")

@login_required
@librarian_required
def import_home(request):

    return render(
        request,
        "imports/index.html",
    )

@login_required
@librarian_required
def manual_book_add(request):

    if request.method == "POST":

        form = BookForm(request.POST)

        if form.is_valid():

            book = form.save()

            AuditLog.objects.create(
                user=request.user,
                action=f"Added book manually: {book.accession_number} - {book.title}",
            )

            messages.success(
                request,
                "Book added successfully.",
            )

            return redirect("catalog")

    else:

        form = BookForm()

    return render(
        request,
        "imports/manual_book.html",
        {
            "form": form,
        },
    )