from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import BookRecommendationForm
from notifications.helpers import create_notification
from django.contrib.auth import get_user_model
from accounts.decorators import library_helper_required, head_librarian_required
from .models import BookRecommendation
from django.utils import timezone

@login_required
def recommend_book(request):

    if request.method == "POST":

        form = BookRecommendationForm(request.POST)

        if form.is_valid():

            recommendation = form.save(commit=False)

            recommendation.member = request.user

            recommendation.save()

            User = get_user_model()

            librarians = User.objects.filter(
                role="librarian"
            )

            for librarian in librarians:

                create_notification(
                    user=librarian,
                    title="📚 New Book Recommendation",
                    message=(
                        f"{request.user.get_full_name() or request.user.username} "
                        f"recommended '{recommendation.title}'."
                    ),
                    link=reverse("recommendation_list"),
                )

            messages.success(
                request,
                "Your recommendation has been submitted successfully."
            )

            return redirect("recommend_book")

    else:

        form = BookRecommendationForm()

    return render(
        request,
        "recommendations/recommend_book.html",
        {
            "form": form,
        },
    )

@library_helper_required
def recommendation_list(request):

    recommendations = (
        BookRecommendation.objects
        .select_related("member")
        .order_by("-requested_at")
    )

    return render(
        request,
        "recommendations/recommendation_list.html",
        {
            "recommendations": recommendations,
        },
    )

@library_helper_required
def recommendation_detail(request, pk):

    recommendation = get_object_or_404(
        BookRecommendation,
        pk=pk,
    )

    return render(
        request,
        "recommendations/recommendation_detail.html",
        {
            "recommendation": recommendation,
        },
    )

@head_librarian_required
def approve_recommendation(request, pk):

    recommendation = get_object_or_404(
        BookRecommendation,
        pk=pk,
    )

    if recommendation.status != BookRecommendation.PENDING:

        messages.warning(
            request,
            "This recommendation has already been reviewed."
        )

        return redirect(
            "recommendation_detail",
            pk=pk,
        )

    recommendation.status = BookRecommendation.APPROVED

    recommendation.reviewed_at = timezone.now()

    recommendation.save()

    print("MY RECOMMENDATION URL =", reverse("my_recommendations"))

    url = reverse("my_recommendations")

    print("URL =", repr(url))

    create_notification(
        user=recommendation.member,
        title="✅ Recommendation Approved",
        message=(
            f"Your recommendation for '{recommendation.title}' "
            f"has been approved."
        ),
        link=url,
    )

    messages.success(
        request,
        "Recommendation approved successfully.",
    )

    return redirect("recommendation_list")

@head_librarian_required
def reject_recommendation(request, pk):

    recommendation = get_object_or_404(
        BookRecommendation,
        pk=pk,
    )

    if recommendation.status != BookRecommendation.PENDING:

        messages.warning(
            request,
            "This recommendation has already been reviewed."
        )

        return redirect(
            "recommendation_detail",
            pk=pk,
        )

    recommendation.status = BookRecommendation.REJECTED

    recommendation.reviewed_at = timezone.now()

    recommendation.save()

    create_notification(
        user=recommendation.member,
        title="❌ Recommendation Rejected",
        message=(
            f"Your recommendation for '{recommendation.title}' "
            f"was not approved."
        ),
        link=reverse("my_recommendations"),
    )

    messages.success(
        request,
        "Recommendation rejected.",
    )

    return redirect("recommendation_list")

@login_required
def my_recommendations(request):

    recommendations = (
        BookRecommendation.objects
        .filter(member=request.user)
        .order_by("-requested_at")
    )

    return render(
        request,
        "recommendations/my_recommendations.html",
        {
            "recommendations": recommendations,
        },
    )