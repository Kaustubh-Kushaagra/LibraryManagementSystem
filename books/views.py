from django.db.models import Q
from django.shortcuts import get_object_or_404, render,redirect
from django.core.paginator import Paginator
from transactions.models import Transaction

from .forms import BookSearchForm
from .models import LibraryItem
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from accounts.decorators import librarian_required
from django.http import JsonResponse
from audit.models import AuditLog
from audit.utils import log_action
from .forms import BookForm
from django.template.loader import render_to_string


def filter_books(books, query):
    """
    Apply the catalog search filters.
    """

    if query:
        books = books.filter(
            Q(title__icontains=query)
            | Q(accession_number__icontains=query)
            | Q(author__name__icontains=query)
            | Q(publisher__name__icontains=query)
        )

    return books
def catalog(request):

    form = BookSearchForm(request.GET or None)

    books = LibraryItem.objects.select_related(
        "author",
        "publisher",
        "category",
    )

    # ------------------------
    # Search
    # ------------------------

    query = ""

    if form.is_valid():
        query = form.cleaned_data.get("query", "")

    books = filter_books(books, query)


    sort = request.GET.get("sort", "title")
    allowed_sizes = [10, 25, 50, 100]

    try:
        page_size = int(request.GET.get("page_size", 25))
    except ValueError:
        page_size = 25

    if page_size not in allowed_sizes:
        page_size = 25


    if sort == "accession":

        books = books.order_by("accession_number")

    elif sort == "author":

        books = books.order_by("author__name")

    elif sort == "publisher":

        books = books.order_by("publisher__name")

    elif sort == "newest":

        books = books.order_by("-created_at")

    elif sort == "oldest":

        books = books.order_by("created_at")

    else:

        books = books.order_by("title")

    # ------------------------
    # Pagination
    # ------------------------

    book_count = books.count()

    paginator = Paginator(
        books,
        page_size,
    )

    page_number = request.GET.get("page")

    books = paginator.get_page(page_number)

    context = {

        "books": books,

        "form": form,

        "current_sort": sort,

        "page_size": page_size,

        "book_count": book_count,

        "paginator": paginator,

    }

    return render(
        request,
        "books/catalog.html",
        context,
    )



def search_books(request):

    query = request.GET.get("q", "")

    books = LibraryItem.objects.select_related(
        "author",
        "publisher",
        "category",
    )

    books = filter_books(books, query)

    next_url = reverse("catalog")

    if query:
        next_url += f"?query={query}"

    html = render_to_string(
        "books/partials/book_rows.html",
        {
            "books": books,
            "request": request,
            "user": request.user,
            "next_url": next_url,
        },
    )

    return JsonResponse({
        "html": html
    })

def book_detail(request, accession_number):

    book = get_object_or_404(
        LibraryItem,
        accession_number=accession_number,
    )

    history = Transaction.objects.filter(
        book=book
    ).select_related(
        "member"
    ).order_by("-issued_at")

    today = timezone.now().date()

    for transaction in history:

        if (
            transaction.status == Transaction.ISSUED
            and transaction.due_date < today
        ):
            transaction.overdue_days = (
                today - transaction.due_date
            ).days
        else:
            transaction.overdue_days = 0

    active_transaction = Transaction.objects.filter(
        book=book,
        status="Issued",
    ).first()

    overdue_days = None

    if active_transaction:

        today = timezone.localdate()

        if active_transaction.due_date < today:

            overdue_days = (
                today - active_transaction.due_date
            ).days

    context = {

        "book": book,
        "active_transaction": active_transaction,
        "history": history,
        "overdue_days": overdue_days,
        "today": today,

    }

    return render(
        request,
        "books/book_detail.html",
        context,
    )

@login_required
@librarian_required
def edit_book(request, accession_number):

    book = get_object_or_404(
        LibraryItem,
        accession_number=accession_number,
    )

    if request.method == "POST":

        form = BookForm(
            request.POST,
            instance=book,
        )

        if form.is_valid():

            updated_book = form.save()

            log_action(
                request.user,
                "Edit Book",
                updated_book.title,
            )

            messages.success(
                request,
                f'"{book.title}" has been updated successfully.'
            )

            return redirect(
                "book_detail",
                accession_number=book.accession_number,
            )

    else:

        form = BookForm(
            instance=book,
        )

    return render(
        request,
        "books/edit_book.html",
        {
            "form": form,
            "book": book,
        },
    )

@login_required
@librarian_required
def delete_book(request, accession_number):

    book = get_object_or_404(
        LibraryItem,
        accession_number=accession_number,
    )

    issued = Transaction.objects.filter(
        book=book,
        status="Issued",
    ).exists()

    if issued:

        messages.error(
            request,
            "This book is currently issued and cannot be deleted."
        )

        return redirect("catalog")

    if request.method == "POST":

        title = book.title

        book.delete()

        log_action(
            request.user,
            "Delete Book",
            title,
        )

        messages.success(
            request,
            "Book deleted successfully."
        )

        return redirect("catalog")

    return render(
        request,
        "books/delete_book.html",
        {
            "book": book,
        },
    )