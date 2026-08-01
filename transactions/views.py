from accounts.decorators import library_helper_required, head_librarian_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from audit.utils import log_action
from books.models import LibraryItem
from book_requests.models import BookRequest
from .forms import IssueBookForm, ApproveReturnForm
from .models import Transaction
from notifications.helpers import create_notification
from accounts.models import User
from django.urls import reverse



@login_required
@library_helper_required
def issue_book(request, accession_number):

    book = get_object_or_404(
        LibraryItem,
        accession_number=accession_number,
    )

    if book.status != "Available":
        messages.error(
            request,
            "This book is not available for issue.",
        )
        return redirect(
            "book_detail",
            accession_number=book.accession_number,
        )

    if request.method == "POST":

        form = IssueBookForm(request.POST)

        if form.is_valid():

            transaction = form.save(commit=False)

            transaction.book = book
            transaction.status = Transaction.ISSUED

            transaction.save()

            book.status = "Issued"
            book.save()

            log_action(
                request.user,
                "Issue Book",
                f"{book.title} issued to {transaction.member.get_full_name() or transaction.member.username}",
            )

            messages.success(
                request,
                "Book issued successfully.",
            )

            return redirect(
                "book_detail",
                accession_number=book.accession_number,
            )

    else:

        form = IssueBookForm()

    return render(
        request,
        "transactions/issue_book.html",
        {
            "form": form,
            "book": book,
        },
    )


@login_required
@library_helper_required
def return_book(request, transaction_id):

    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        status=Transaction.ISSUED,
    )

    transaction.status = Transaction.RETURNED
    transaction.returned_at = timezone.now()
    transaction.save()

    book = transaction.book
    book.status = "Available"
    book.save()

    log_action(
        request.user,
        "Return Book",
        f"{transaction.book.title} returned by {transaction.member.get_full_name() or transaction.member.username}",
    )

    messages.success(
        request,
        "Book returned successfully.",
    )

    return redirect(
        "book_detail",
        accession_number=book.accession_number,
    )

@login_required
def my_books(request):

    transactions = (
        Transaction.objects
        .filter(member=request.user)
        .select_related("book")
        .order_by("-issued_at")
    )

    today = timezone.now().date()

    my_requests = (
        BookRequest.objects
        .filter(member=request.user)
        .select_related("book")
        .order_by("-requested_at")
    )

    for transaction in transactions:

        if (
            transaction.status == Transaction.ISSUED
            and transaction.due_date < today
        ):
            transaction.overdue_days = (
                today - transaction.due_date
            ).days

        else:
            transaction.overdue_days = 0

    return render(
        request,
        "transactions/my_books.html",
        {
            "transactions": transactions,
            "my_requests": my_requests,
        },
    )



@library_helper_required
def manage_transactions(request):

    transactions = (
        Transaction.objects
        .select_related("book", "member")
        .order_by("-issued_at")
    )

    return render(
        request,
        "transactions/manage_transactions.html",
        {
            "transactions": transactions,
        },
    )

@login_required
def request_return(request, transaction_id):

    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        member=request.user,
        status=Transaction.ISSUED,
    )

    if transaction.return_status != Transaction.RETURN_NONE:

        messages.warning(
            request,
            "You have already requested the return of this book.",
        )

        return redirect("my_books")

    transaction.return_status = Transaction.RETURN_REQUESTED
    transaction.return_requested_at = timezone.now()
    transaction.save()

    librarians = User.objects.filter(role=User.LIBRARIAN)

    for librarian in librarians:

        create_notification(
            user=librarian,
            title="📦 New Return Request",
            message=(
                f"{request.user.get_full_name() or request.user.username} "
                f"requested to return '{transaction.book.title}'."
            ),
            link=reverse("pending_returns"),
        )

    messages.success(
        request,
        "Your return request has been sent to the librarian.",
    )

    return redirect("my_books")

@library_helper_required
def pending_returns(request):

    transactions = (
        Transaction.objects
        .filter(
            status=Transaction.ISSUED,
            return_status=Transaction.RETURN_REQUESTED,
        )
        .select_related(
            "member",
            "book",
        )
        .order_by("-return_requested_at")
    )

    return render(
        request,
        "transactions/pending_returns.html",
        {
            "transactions": transactions,
        },
    )

@library_helper_required
def approve_return(request, transaction_id):

    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        return_status=Transaction.RETURN_REQUESTED,
    )

    if request.method == "POST":

        form = ApproveReturnForm(request.POST)

        if form.is_valid():

            transaction.return_pickup_date = form.cleaned_data["return_date"]
            transaction.return_pickup_time = form.cleaned_data["return_time"]
            transaction.librarian_return_message = form.cleaned_data["librarian_message"]

            transaction.return_status = Transaction.RETURN_APPROVED
            transaction.save()

            create_notification(
                user=transaction.member,
                title="📦 Return Approved",
                message=(
                    f"Please return '{transaction.book.title}' on "
                    f"{transaction.return_pickup_date} "
                    f"at {transaction.return_pickup_time.strftime('%I:%M %p')}."
                ),
                link=reverse("my_books"),
            )

            messages.success(
                request,
                f"'{transaction.book.title}' return has been scheduled and the member has been notified."
            )

            return redirect("pending_returns")

    else:

        form = ApproveReturnForm()

    return render(
        request,
        "transactions/approve_return.html",
        {
            "transaction": transaction,
            "form": form,
        },
    )