from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def library_helper_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.role not in [
            "library_helper",
            "head_librarian",
        ]:

            messages.error(
                request,
                "You do not have permission to perform this action."
            )

            return redirect("dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper


def head_librarian_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.role != "head_librarian":

            messages.error(
                request,
                "Only the Head Librarian can perform this action."
            )

            return redirect("dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper


# Backward compatibility
librarian_required = library_helper_required