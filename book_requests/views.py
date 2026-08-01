from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from books.models import LibraryItem
from .models import BookRequest
from accounts.decorators import library_helper_required
from .forms import ApproveRequestForm, RejectRequestForm
from django.utils import timezone
from datetime import timedelta
from transactions.models import Transaction
from audit.utils import log_action
from django.contrib.auth import get_user_model
from notifications.helpers import create_notification
from django.urls import reverse



@login_required
def request_book(request, accession_number):

    book = get_object_or_404(
        LibraryItem,
        accession_number=accession_number,
    )

    if book.status != LibraryItem.AVAILABLE:
        messages.error(
            request,
            "This book is currently unavailable.",
        )
        return redirect(
            "book_detail",
            accession_number=accession_number,
        )

    already_requested = BookRequest.objects.filter(
        member=request.user,
        book=book,
        status=BookRequest.PENDING,
    ).exists()

    if already_requested:
        messages.warning(
            request,
            "You have already requested this book.",
        )
        return redirect(
            "book_detail",
            accession_number=accession_number,
        )

    new_request = BookRequest.objects.create(
        member=request.user,
        book=book,
    )


    User = get_user_model()

    librarians = User.objects.filter(
        role__in=[
            "head_librarian",
            "library_helper",
        ]
    )

    for librarian in librarians:

        create_notification(
            user=librarian,
            title="📩 New Book Request",
            message=(
                f"{request.user.get_full_name() or request.user.username} "
                f"requested '{book.title}'."
            ),
            link=reverse("pending_requests"),
        )

    messages.success(
        request,
        "Your request has been sent to the librarian.",
    )

    return redirect(
        "book_detail",
        accession_number=accession_number,
    )


@login_required
@library_helper_required
def pending_requests(request):

    requests = (
        BookRequest.objects.filter(
            Q(status=BookRequest.PENDING) |
            Q(status=BookRequest.READY)
        )
        .select_related(
            "book",
            "member",
        )
        .order_by("-requested_at")
    )


    return render(
        request,
        "book_requests/pending_requests.html",
        {
            "requests": requests,
        },
    )

@login_required
@library_helper_required
def approve_request(request, request_id):

    book_request = get_object_or_404(
        BookRequest,
        id=request_id,
    )

    if request.method == "POST":

        form = ApproveRequestForm(request.POST)

        if form.is_valid():

            book_request.pickup_date = form.cleaned_data["pickup_date"]

            book_request.pickup_time = form.cleaned_data["pickup_time"]

            book_request.librarian_message = form.cleaned_data["librarian_message"]

            book_request.status = BookRequest.READY

            transaction = Transaction.objects.create(

                member=book_request.member,

                book=book_request.book,

                status=Transaction.PENDING_PICKUP,

            )
            book = book_request.book
            book.status = LibraryItem.PENDING_PICKUP
            book.save(update_fields=["status"])

            book_request.transaction = transaction

            book_request.save()

            create_notification(
                user=book_request.member,
                title="✅ Book Request Approved",
                message=(
                    f"Your request for '{book_request.book.title}' has been approved. "
                    f"Please collect it on {book_request.pickup_date} "
                    f"at {book_request.pickup_time.strftime('%I:%M %p')}."
                ),
                link=reverse("my_books") + "#my-book-requests",
            )

            return redirect("pending_requests")

        else:

            print(form.errors)

    else:

        form = ApproveRequestForm()

    return render(
        request,
        "book_requests/approve_request.html",
        {
            "book_request": book_request,
            "form": form,
        },
    )

@login_required
@library_helper_required
def confirm_collection(request, request_id):

    book_request = get_object_or_404(
        BookRequest,
        id=request_id,
        status=BookRequest.READY,
    )

    if request.method == "POST":

        transaction = book_request.transaction

        transaction.status = Transaction.ISSUED
        transaction.issued_at = timezone.now()
        transaction.due_date = timezone.now().date() + timedelta(days=14)
        transaction.save()

        book = transaction.book
        book.status = LibraryItem.ISSUED
        book.save(update_fields=["status"])

        create_notification(
            user=book_request.member,
            title="📚 Book Issued",
            message=(
                f"You have successfully collected "
                f"'{book.title}'. "
                f"Enjoy reading!"
            ),
            link=reverse("my_books") + "#my-book-requests",
        )

        log_action(
            request.user,
            "Confirm Collection",
            f"{book.title} collected by "
            f"{book_request.member.get_full_name() or book_request.member.username}",
        )

        messages.success(
            request,
            "Book handed over successfully.",
        )

        return redirect("pending_requests")

    return render(
        request,
        "book_requests/confirm_collection.html",
        {
            "book_request": book_request,
        },
    )

@login_required
@library_helper_required
def reject_request(request, pk):

    if request.user.role != "librarian":
        messages.error(request, "Permission denied.")
        return redirect("dashboard")

    book_request = get_object_or_404(
        BookRequest,
        pk=pk,
    )

    if request.method == "POST":

        form = RejectRequestForm(request.POST)

        if form.is_valid():

            book_request.status = BookRequest.REJECTED

            book_request.rejection_reason = form.cleaned_data[
                "rejection_reason"
            ]

            book_request.rejected_by = request.user

            book_request.rejected_at = timezone.now()

            book_request.save()

            create_notification(
                user=book_request.member,
                title="❌ Book Request Rejected",
                message=f"Your request for '{book_request.book.title}' was rejected.",
                link=reverse("my_books") + "#my-book-requests",
            )
            messages.success(
                request,
                "Book request rejected successfully."
            )

            return redirect("pending_requests")

    else:

        form = RejectRequestForm()

    return render(
        request,
        "book_requests/reject_request.html",
        {
            "book_request": book_request,
            "form": form,
        },
    )

@library_helper_required
def collect_book(request, request_id):

    book_request = get_object_or_404(
        BookRequest,
        id=request_id,
        status=BookRequest.READY,
    )

    transaction = book_request.transaction

    transaction.status = Transaction.ISSUED
    transaction.save()

    book = transaction.book

    book.status = LibraryItem.ISSUED
    book.save()

    book_request.status = BookRequest.COLLECTED
    book_request.save()

    create_notification(
        user=book_request.member,
        title="📚 Book Collected",
        message=(
            f"You have successfully collected "
            f"'{book.title}'."
        ),
        link=reverse("my_books"),
    )

    messages.success(
        request,
        f"'{book.title}' has been issued to "
        f"{book_request.member.get_full_name() or book_request.member.username}.",
    )

    return redirect("pending_requests")