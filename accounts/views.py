from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import Count
from audit.models import AuditLog
from audit.utils import log_action
from books.models import LibraryItem
from transactions.models import Transaction
from book_requests.models import BookRequest
from .forms import UserRegisterForm, EditProfileForm
from recommendations.models import BookRecommendation
import secrets
import string
from django.contrib.auth.hashers import make_password


def generate_temp_password(length=10):

    characters = (
        string.ascii_letters
        + string.digits
        + "!@#$%&*?"
    )

    while True:

        password = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in "!@#$%&*?" for c in password)
        ):

            return password



def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = UserRegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            log_action(
                user,
                "Register",
                "New account created",
            )

            messages.success(
                request,
                "Account created successfully."
            )

            login(request, user)

            return redirect("dashboard")

    else:

        form = UserRegisterForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form,
        },
    )




@login_required
def dashboard(request):

    if request.user.role == "librarian":

        total_books = LibraryItem.objects.count()

        available_books = LibraryItem.objects.filter(
            status="Available"
        ).count()

        issued_books = LibraryItem.objects.filter(
            status="Issued"
        ).count()

        pending_pickups = Transaction.objects.filter(
            status=Transaction.PENDING_PICKUP
        ).count()

        pending_recommendations = BookRecommendation.objects.filter(
            status="Pending"
        ).count()

        pending_returns = Transaction.objects.filter(
            return_status=Transaction.RETURN_REQUESTED
        ).count()

        overdue_books = Transaction.objects.filter(
            status="Issued",
            due_date__lt=timezone.now().date(),
        ).count()

        total_members = get_user_model().objects.filter(
            role="member"
        ).count()

        recent_books = LibraryItem.objects.order_by(
            "-created_at"
        )[:5]

        recent_transactions = (
            Transaction.objects.select_related(
                "book",
                "member",
            )
            .order_by("-issued_at")[:5]
        )

        today = timezone.now()

        books_issued_this_month = Transaction.objects.filter(
            issued_at__year=today.year,
            issued_at__month=today.month,
        ).count()

        books_returned_this_month = Transaction.objects.filter(
            returned_at__year=today.year,
            returned_at__month=today.month,
        ).count()

        books_added_this_month = LibraryItem.objects.filter(
            created_at__year=today.year,
            created_at__month=today.month,
        ).count()

        top_books = (
            LibraryItem.objects
            .annotate(
                times_issued=Count("transactions")
            )
            .order_by("-times_issued", "title")[:5]
        )

        recent_activity = (
            AuditLog.objects.select_related(
                "user"
            )
            .order_by("-timestamp")[:8]
        )

        context = {

            "total_books": total_books,
            "available_books": available_books,
            "issued_books": issued_books,
            "overdue_books": overdue_books,
            "total_members": total_members,

            "recent_books": recent_books,
            "recent_transactions": recent_transactions,
            "recent_activity": recent_activity,
            "top_books": top_books,

            "books_issued_this_month": books_issued_this_month,
            "books_returned_this_month": books_returned_this_month,
            "books_added_this_month": books_added_this_month,

            "pending_pickups": pending_pickups,

            "pending_returns": pending_returns,

            "pending_recommendations": pending_recommendations,


        }

        return render(
            request,
            "dashboard/dashboard.html",
            context,
        )

    # -----------------------------
    # MEMBER DASHBOARD
    # -----------------------------

    active_transactions = Transaction.objects.exclude(
        status=Transaction.RETURNED
    ).filter(
        member=request.user,
    )

    issued_books = active_transactions.filter(
        status=Transaction.ISSUED
    )

    pending_pickups = active_transactions.filter(
        status=Transaction.PENDING_PICKUP
    )

    pending_requests = BookRequest.objects.filter(
        member=request.user,
        status=BookRequest.PENDING,
    )

    approved_requests = BookRequest.objects.filter(
        member=request.user,
        status=BookRequest.APPROVED,
    )

    rejected_requests = BookRequest.objects.filter(
        member=request.user,
        status=BookRequest.REJECTED,
    )

    recent_requests = BookRequest.objects.filter(
        member=request.user,
    ).select_related(
        "book"
    ).order_by(
        "-requested_at"
    )[:5]

    context = {

        "issued_books": issued_books,

        "issued_count": issued_books.count(),

        "pending_pickup_count": pending_pickups.count(),

        "pending_count": pending_requests.count(),

        "approved_count": approved_requests.count(),

        "rejected_count": rejected_requests.count(),

        "recent_requests": recent_requests,



    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )


@login_required
def member_list(request):

    User = get_user_model()

    search = request.GET.get("search", "")

    members = User.objects.filter(
        role="member"
    )

    if search:

        members = members.filter(

            Q(employee_id__icontains=search)

            | Q(first_name__icontains=search)

            | Q(last_name__icontains=search)

            | Q(username__icontains=search)

        )

    return render(

        request,

        "accounts/member_list.html",

        {

            "members": members,

            "search": search,

        },

    )


@login_required
def member_detail(request, user_id):

    User = get_user_model()

    member = get_object_or_404(

        User,

        id=user_id,

    )

    current_books = Transaction.objects.filter(
        member=member,
    ).exclude(
        status=Transaction.RETURNED,
    )

    history = Transaction.objects.filter(

        member=member,

    ).order_by("-issued_at")

    recommendations = (
        BookRecommendation.objects.filter(
            member=member,
        ).order_by("-requested_at")
    )

    today = timezone.now().date()

    for transaction in history:

        if (

            transaction.status == "Issued"

            and transaction.due_date < today

        ):

            transaction.overdue_days = (

                today - transaction.due_date

            ).days

        else:

            transaction.overdue_days = 0

    return render(

        request,

        "accounts/member_detail.html",

        {

            "member": member,

            "current_books": current_books,

            "history": history,

            "recommendations": recommendations,
            
        },

    )

@login_required
def toggle_member_status(request, user_id):

    User = get_user_model()

    member = get_object_or_404(
        User,
        id=user_id,
        role="member",
    )

    if member == request.user:

        messages.error(
            request,
            "You cannot deactivate your own account."
        )

        return redirect("member_list")

    if member.is_active:

        active_transactions = Transaction.objects.filter(
            member=member,
            status=Transaction.ISSUED,
        )

        if active_transactions.exists():

            messages.error(
                request,
                "Cannot deactivate this member because they still have issued books.",
            )

            return redirect("member_list")

        member.is_active = False

        member.save()

        messages.success(
            request,
            "Member has been deactivated successfully.",
        )

    else:

        member.is_active = True

        member.save()

        messages.success(
            request,
            "Member has been reactivated successfully.",
        )

    return redirect("member_list")


@login_required
def reset_member_password(request, user_id):

    User = get_user_model()

    member = get_object_or_404(
        User,
        id=user_id,
        role="member",
    )

    if request.method == "POST":

        temporary_password = generate_temp_password()

        member.set_password(temporary_password)
        member.save()

        AuditLog.objects.create(

            user=request.user,

            action="Reset Password",

            details=f"Temporary password generated for {member.username}",

        )

        request.session["temp_password"] = temporary_password
        request.session["temp_member"] = member.id

        return redirect("password_reset_success")

    return render(

        request,

        "accounts/password_reset_confirm.html",

        {

            "member": member,

        },

    )

@login_required
def password_reset_success(request):

    temporary_password = request.session.get("temp_password")
    member_id = request.session.get("temp_member")

    if not temporary_password or not member_id:

        messages.warning(
            request,
            "No password reset information available.",
        )

        return redirect("member_list")

    User = get_user_model()

    member = get_object_or_404(
        User,
        id=member_id,
    )

    request.session.pop("temp_password", None)
    request.session.pop("temp_member", None)

    return render(

        request,

        "accounts/password_reset_success.html",

        {

            "member": member,
            "temporary_password": temporary_password,

        },

    )


@login_required
def profile(request):

    return render(
        request,
        "accounts/profile.html",
    )

@login_required
def edit_profile(request):

    if request.method == "POST":

        form = EditProfileForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")

    else:

        form = EditProfileForm(
            instance=request.user,
        )

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form,
        },
    )