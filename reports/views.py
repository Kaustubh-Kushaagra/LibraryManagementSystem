from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

from accounts.decorators import library_helper_required,head_librarian_required
from books.models import LibraryItem
from django.contrib.auth import get_user_model
from transactions.models import Transaction
from django.utils import timezone


@login_required
@library_helper_required
def export_books_excel(request):

    workbook = Workbook()

    worksheet = workbook.active
    worksheet.title = "Book Catalogue"

    worksheet.merge_cells("A1:O1")

    title = worksheet["A1"]
    title.value = "MVTC Library Management System"
    title.font = Font(
        bold=True,
        size=16,
    )
    title.alignment = Alignment(horizontal="center")

    headers = [
        "Accession Number",
        "Serial Number",
        "Title",
        "Author",
        "Publisher",
        "Category",
        "Publication Year",
        "Pages",
        "Rate in Rs.",
        "Volume Qty",
        "Source",
        "Location",
        "Remarks",
        "Date Added",
        "Status",
    ]

    for column, header in enumerate(headers, start=1):

        cell = worksheet.cell(
            row=3,
            column=column,
        )

        cell.value = header

        cell.font = Font(
            bold=True,
            color="FFFFFF",
        )

        cell.fill = PatternFill(
            fill_type="solid",
            fgColor="4472C4",
        )

        cell.alignment = Alignment(
            horizontal="center",
        )

    books = LibraryItem.objects.select_related(
        "author",
        "publisher",
        "category",
    ).order_by("accession_number")

    row = 4

    for book in books:

        worksheet.cell(row=row, column=1).value = book.accession_number
        worksheet.cell(row=row, column=2).value = book.serial_number
        worksheet.cell(row=row, column=3).value = book.title
        worksheet.cell(row=row, column=4).value = str(book.author)
        worksheet.cell(row=row, column=5).value = str(book.publisher)
        worksheet.cell(row=row, column=6).value = str(book.category)
        worksheet.cell(row=row, column=7).value = book.publication_year
        worksheet.cell(row=row, column=8).value = book.pages
        worksheet.cell(row=row, column=9).value = book.price
        worksheet.cell(row=row, column=10).value = book.volume_qty
        worksheet.cell(row=row, column=11).value = book.source
        worksheet.cell(row=row, column=12).value = book.location
        worksheet.cell(row=row, column=13).value = book.remarks
        worksheet.cell(row=row, column=14).value = (
            book.date_added.strftime("%d-%m-%Y")
            if book.date_added else ""
        )
        worksheet.cell(row=row, column=15).value = book.status

        row += 1

    for column_cells in worksheet.columns:

        # merged title cell causes this column to fail
        try:
            column = column_cells[0].column
        except AttributeError:
            column = column_cells[1].column

        length = max(
            len(str(cell.value)) if cell.value else 0
            for cell in column_cells
        )

        worksheet.column_dimensions[
            get_column_letter(column)
        ].width = length + 4

    worksheet.freeze_panes = "A4"

    worksheet.auto_filter.ref = f"A3:G{row-1}"

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="Book_Catalogue.xlsx"'
    )

    workbook.save(response)

    return response

@login_required
@library_helper_required
def export_members_excel(request):

    User = get_user_model()

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Members"

    worksheet.merge_cells("A1:F1")

    title = worksheet["A1"]
    title.value = "MVTC Library Management System - Members Report"
    title.font = Font(size=16, bold=True)
    title.alignment = Alignment(horizontal="center")

    headers = [
        "Employee ID",
        "Name",
        "Username",
        "Department",
        "Designation",
        "Email",
    ]

    for column, header in enumerate(headers, start=1):

        cell = worksheet.cell(row=3, column=column)

        cell.value = header
        cell.font = Font(bold=True, color="FFFFFF")

        cell.fill = PatternFill(
            fill_type="solid",
            fgColor="4472C4",
        )

        cell.alignment = Alignment(horizontal="center")

    members = User.objects.filter(
        role="member"
    ).order_by("employee_id")

    row = 4

    for member in members:

        worksheet.cell(row=row, column=1).value = member.employee_id
        worksheet.cell(row=row, column=2).value = (
            member.get_full_name() or member.username
        )
        worksheet.cell(row=row, column=3).value = member.username
        worksheet.cell(row=row, column=4).value = member.department
        worksheet.cell(row=row, column=5).value = member.designation
        worksheet.cell(row=row, column=6).value = member.email

        row += 1

    for column_cells in worksheet.columns:

        length = max(
            len(str(cell.value)) if cell.value else 0
            for cell in column_cells
        )

        worksheet.column_dimensions[
            get_column_letter(column_cells[0].column)
        ].width = length + 4

    worksheet.freeze_panes = "A4"
    worksheet.auto_filter.ref = f"A3:O{row-1}"

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="Members_Report.xlsx"'

    workbook.save(response)

    return response

@login_required
@library_helper_required
def export_issued_books_excel(request):

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Issued Books"

    worksheet.merge_cells("A1:G1")

    title = worksheet["A1"]
    title.value = "MVTC Library Management System - Issued Books Report"
    title.font = Font(size=16, bold=True)
    title.alignment = Alignment(horizontal="center")

    headers = [
        "Accession No.",
        "Book Title",
        "Member",
        "Employee ID",
        "Issued On",
        "Due Date",
        "Status",
    ]

    for column, header in enumerate(headers, start=1):

        cell = worksheet.cell(row=3, column=column)

        cell.value = header

        cell.font = Font(
            bold=True,
            color="FFFFFF",
        )

        cell.fill = PatternFill(
            fill_type="solid",
            fgColor="4472C4",
        )

        cell.alignment = Alignment(horizontal="center")

    transactions = Transaction.objects.select_related(
        "book",
        "member",
    ).filter(
        status=Transaction.ISSUED
    ).order_by("due_date")

    row = 4

    for transaction in transactions:

        worksheet.cell(row=row, column=1).value = transaction.book.accession_number
        worksheet.cell(row=row, column=2).value = transaction.book.title
        worksheet.cell(row=row, column=3).value = (
            transaction.member.get_full_name()
            or transaction.member.username
        )
        worksheet.cell(row=row, column=4).value = transaction.member.employee_id
        worksheet.cell(row=row, column=5).value = transaction.issued_at.strftime("%d-%m-%Y")
        worksheet.cell(row=row, column=6).value = transaction.due_date.strftime("%d-%m-%Y")
        worksheet.cell(row=row, column=7).value = transaction.status

        row += 1

    for column_cells in worksheet.columns:

        length = max(
            len(str(cell.value)) if cell.value else 0
            for cell in column_cells
        )

        worksheet.column_dimensions[
            get_column_letter(column_cells[0].column)
        ].width = length + 4

    worksheet.freeze_panes = "A4"
    worksheet.auto_filter.ref = f"A3:G{row-1}"

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="Issued_Books_Report.xlsx"'

    workbook.save(response)

    return response


@login_required
@library_helper_required
def export_overdue_books_excel(request):

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Overdue Books"

    worksheet.merge_cells("A1:H1")

    title = worksheet["A1"]
    title.value = "MVTC Library Management System - Overdue Books Report"
    title.font = Font(size=16, bold=True)
    title.alignment = Alignment(horizontal="center")

    headers = [
        "Accession No.",
        "Book Title",
        "Member",
        "Employee ID",
        "Issued On",
        "Due Date",
        "Days Overdue",
        "Status",
    ]

    for column, header in enumerate(headers, start=1):

        cell = worksheet.cell(row=3, column=column)

        cell.value = header

        cell.font = Font(
            bold=True,
            color="FFFFFF",
        )

        cell.fill = PatternFill(
            fill_type="solid",
            fgColor="C00000",
        )

        cell.alignment = Alignment(horizontal="center")

    today = timezone.now().date()

    transactions = Transaction.objects.select_related(
        "book",
        "member",
    ).filter(
        status=Transaction.ISSUED,
        due_date__lt=today,
    ).order_by("due_date")

    row = 4

    for transaction in transactions:

        overdue_days = (today - transaction.due_date).days

        worksheet.cell(row=row, column=1).value = transaction.book.accession_number
        worksheet.cell(row=row, column=2).value = transaction.book.title
        worksheet.cell(row=row, column=3).value = (
            transaction.member.get_full_name()
            or transaction.member.username
        )
        worksheet.cell(row=row, column=4).value = transaction.member.employee_id
        worksheet.cell(row=row, column=5).value = transaction.issued_at.strftime("%d-%m-%Y")
        worksheet.cell(row=row, column=6).value = transaction.due_date.strftime("%d-%m-%Y")
        worksheet.cell(row=row, column=7).value = overdue_days
        worksheet.cell(row=row, column=8).value = "Overdue"

        row += 1

    for column_cells in worksheet.columns:

        length = max(
            len(str(cell.value)) if cell.value else 0
            for cell in column_cells
        )

        worksheet.column_dimensions[
            get_column_letter(column_cells[0].column)
        ].width = length + 4

    worksheet.freeze_panes = "A4"
    worksheet.auto_filter.ref = f"A3:H{row-1}"

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="Overdue_Books_Report.xlsx"'

    workbook.save(response)

    return response

@login_required
@library_helper_required
def reports_home(request):

    return render(
        request,
        "reports/reports_home.html",
    )