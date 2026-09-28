from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import (
    Q,
)
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    CompanyForm,
    FollowUpForm,
    InterviewForm,
    JobApplicationForm,
)
from .models import (
    FollowUp,
    Interview,
    JobApplication,
)

# =========================================================
# REGISTRATION
# =========================================================

def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(
                request,
                user,
            )

            return redirect("dashboard")

    else:

        form = UserCreationForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form,
        },
    )


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    today = timezone.localdate()

    applications = JobApplication.objects.filter(
        user=request.user
    ).select_related(
        "company"
    )

    interviews = Interview.objects.filter(
        application__user=request.user
    ).select_related(
        "application",
        "application__company",
    )

    todays_interviews = interviews.filter(
        interview_date=today
    ).order_by(
        "interview_time"
    )

    upcoming_interviews = interviews.filter(
        interview_date__gt=today
    ).order_by(
        "interview_date",
        "interview_time"
    )[:5]

    pending_follow_ups = FollowUp.objects.filter(
        application__user=request.user,
        completed=False,
    )

    # -----------------------------------------------------
    # APPLICATIONS NEEDING ATTENTION
    # -----------------------------------------------------

    aging_cutoff = today - timedelta(days=7)

    aging_applications = applications.filter(
        application_date__lte=aging_cutoff,
        status__in=[
            JobApplication.Status.APPLIED,
            JobApplication.Status.SHORTLISTED,
            JobApplication.Status.ASSESSMENT,
            JobApplication.Status.INTERVIEW,
            JobApplication.Status.OFFER,
        ],
    ).order_by(
        "application_date"
    )[:5]

    overdue_follow_ups = pending_follow_ups.filter(
        follow_up_date__lt=today
    ).select_related(
        "application",
        "application__company",
    ).order_by(
        "follow_up_date"
    )[:5]

    todays_follow_ups = pending_follow_ups.filter(
        follow_up_date=today
    ).select_related(
        "application",
        "application__company",
    ).order_by(
        "follow_up_date"
    )[:5]

    attention_count = (
        aging_applications.count()
        + overdue_follow_ups.count()
        + todays_follow_ups.count()
        + todays_interviews.count()
    )

    # -----------------------------------------------------
    # PIPELINE
    # -----------------------------------------------------

    pipeline_counts = {

        "applied": applications.filter(
            status=JobApplication.Status.APPLIED
        ).count(),

        "shortlisted": applications.filter(
            status=JobApplication.Status.SHORTLISTED
        ).count(),

        "assessment": applications.filter(
            status=JobApplication.Status.ASSESSMENT
        ).count(),

        "interview": applications.filter(
            status=JobApplication.Status.INTERVIEW
        ).count(),

        "offer": applications.filter(
            status=JobApplication.Status.OFFER
        ).count(),

    }

    # -----------------------------------------------------
    # RECENT APPLICATIONS
    # -----------------------------------------------------

    recent_applications = applications[:5]

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {

        "total_applications":
            applications.count(),

        "interview_count":
            interviews.count(),

        "follow_up_count":
            pending_follow_ups.count(),

        "offer_count":
            applications.filter(
                status=JobApplication.Status.OFFER
            ).count(),

        "pipeline_counts":
            pipeline_counts,

        "todays_interviews":
            todays_interviews,

        "upcoming_interviews":
            upcoming_interviews,

        "recent_applications":
            recent_applications,

        # -------------------------------------------------
        # ATTENTION
        # -------------------------------------------------

        "aging_applications":
            aging_applications,

        "overdue_follow_ups":
            overdue_follow_ups,

        "todays_follow_ups":
            todays_follow_ups,

        "attention_count":
            attention_count,

    }

    return render(
        request,
        "dashboard.html",
        context,
    )


# =========================================================
# APPLICATION LIST
# SEARCH + FILTER + SORT
# =========================================================

@login_required
def application_list(request):

    applications = JobApplication.objects.filter(
        user=request.user
    ).select_related(
        "company"
    )

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    if search_query:

        applications = applications.filter(
            Q(
                company__name__icontains=search_query
            )
            |
            Q(
                job_title__icontains=search_query
            )
            |
            Q(
                location__icontains=search_query
            )
        )

    # -----------------------------------------------------
    # STATUS FILTER
    # -----------------------------------------------------

    selected_status = request.GET.get(
        "status",
        ""
    )

    valid_statuses = {
        choice[0]
        for choice in JobApplication.Status.choices
    }

    if selected_status in valid_statuses:

        applications = applications.filter(
            status=selected_status
        )

    else:

        selected_status = ""

    # -----------------------------------------------------
    # JOB TYPE FILTER
    # -----------------------------------------------------

    selected_job_type = request.GET.get(
        "job_type",
        ""
    )

    valid_job_types = {
        choice[0]
        for choice in JobApplication.JobType.choices
    }

    if selected_job_type in valid_job_types:

        applications = applications.filter(
            job_type=selected_job_type
        )

    else:

        selected_job_type = ""

    # -----------------------------------------------------
    # WORK MODE FILTER
    # -----------------------------------------------------

    selected_work_mode = request.GET.get(
        "work_mode",
        ""
    )

    valid_work_modes = {
        choice[0]
        for choice in JobApplication.WorkMode.choices
    }

    if selected_work_mode in valid_work_modes:

        applications = applications.filter(
            work_mode=selected_work_mode
        )

    else:

        selected_work_mode = ""

    # -----------------------------------------------------
    # SORTING
    # -----------------------------------------------------

    selected_sort = request.GET.get(
        "sort",
        "newest"
    )

    sort_options = {

        # Newest applications first
        "newest": [
            "-application_date",
            "-created_at",
        ],

        # Oldest applications first
        "oldest": [
            "application_date",
            "created_at",
        ],

        # Job title A-Z
        "title_az": [
            Lower("job_title"),
            "job_title",
        ],

        # Job title Z-A
        "title_za": [
            Lower("job_title").desc(),
            "job_title",
        ],

        # Backward-compatible option
        "job_title": [
            Lower("job_title"),
            "job_title",
        ],

        # Company A-Z
        "company": [
            Lower("company__name"),
            "job_title",
        ],

        # Status
        "status": [
            "status",
            "-application_date",
        ],

    }

    if selected_sort not in sort_options:

        selected_sort = "newest"

    applications = applications.order_by(
        *sort_options[selected_sort]
    )

    # -----------------------------------------------------
    # ALL USER APPLICATIONS
    # -----------------------------------------------------
    # These counts intentionally use all applications owned
    # by the logged-in user, not the currently filtered list.

    all_user_applications = JobApplication.objects.filter(
        user=request.user
    )

    total_applications = all_user_applications.count()

    active_opportunities = all_user_applications.filter(
        status__in=[
            JobApplication.Status.APPLIED,
            JobApplication.Status.SHORTLISTED,
            JobApplication.Status.ASSESSMENT,
            JobApplication.Status.INTERVIEW,
            JobApplication.Status.OFFER,
        ]
    ).count()

    interview_count = all_user_applications.filter(
        status=JobApplication.Status.INTERVIEW
    ).count()

    offer_count = all_user_applications.filter(
        status=JobApplication.Status.OFFER
    ).count()

    # -----------------------------------------------------
    # PIPELINE COUNTS
    # -----------------------------------------------------

    pipeline_counts = {

        "applied": all_user_applications.filter(
            status=JobApplication.Status.APPLIED
        ).count(),

        "shortlisted": all_user_applications.filter(
            status=JobApplication.Status.SHORTLISTED
        ).count(),

        "assessment": all_user_applications.filter(
            status=JobApplication.Status.ASSESSMENT
        ).count(),

        "interview": all_user_applications.filter(
            status=JobApplication.Status.INTERVIEW
        ).count(),

        "offer": all_user_applications.filter(
            status=JobApplication.Status.OFFER
        ).count(),

        # Added for the Applications pipeline
        "accepted": all_user_applications.filter(
            status=JobApplication.Status.ACCEPTED
        ).count(),

    }

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {

        "applications":
            applications,

        "total_applications":
            total_applications,

        "active_opportunities":
            active_opportunities,

        "interview_count":
            interview_count,

        "offer_count":
            offer_count,

        "pipeline_counts":
            pipeline_counts,

        "search_query":
            search_query,

        "selected_status":
            selected_status,

        "selected_job_type":
            selected_job_type,

        "selected_work_mode":
            selected_work_mode,

        "selected_sort":
            selected_sort,

        "status_choices":
            JobApplication.Status.choices,

        "job_type_choices":
            JobApplication.JobType.choices,

        "work_mode_choices":
            JobApplication.WorkMode.choices,

    }

    return render(
        request,
        "applications/application_list.html",
        context,
    )


# =========================================================
# CREATE APPLICATION
# =========================================================

@login_required
def application_create(request):

    if request.method == "POST":

        form = JobApplicationForm(
            request.POST
        )

        if form.is_valid():

            application = form.save(
                commit=False
            )

            application.user = request.user

            application.save()

            messages.success(
                request,
                "Job application added successfully.",
            )

            return redirect(
                "applications:list"
            )

    else:

        form = JobApplicationForm()

    return render(
        request,
        "applications/application_form.html",
        {
            "form": form,
        },
    )


# =========================================================
# APPLICATION DETAIL
# =========================================================

@login_required
def application_detail(request, pk):

    application = get_object_or_404(

        JobApplication.objects.select_related(
            "company"
        ).prefetch_related(
            "interviews",
            "follow_ups",
        ),

        pk=pk,

        user=request.user,

    )

    return render(
        request,
        "applications/application_detail.html",
        {
            "application": application,
        },
    )


# =========================================================
# UPDATE APPLICATION
# =========================================================

@login_required
def application_update(request, pk):

    application = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":

        form = JobApplicationForm(
            request.POST,
            instance=application,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Job application updated successfully.",
            )

            return redirect(
                "applications:detail",
                pk=application.pk,
            )

    else:

        form = JobApplicationForm(
            instance=application,
        )

    return render(
        request,
        "applications/application_form.html",
        {
            "form": form,
            "application": application,
        },
    )


# =========================================================
# DELETE APPLICATION
# =========================================================

@login_required
def application_delete(request, pk):

    application = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":

        application.delete()

        messages.success(
            request,
            "Job application deleted successfully.",
        )

        return redirect(
            "applications:list"
        )

    return render(
        request,
        "applications/application_confirm_delete.html",
        {
            "application": application,
        },
    )


# =========================================================
# CREATE COMPANY
# =========================================================

@login_required
def company_create(request):

    if request.method == "POST":

        form = CompanyForm(
            request.POST
        )

        if form.is_valid():

            company = form.save()

            messages.success(
                request,
                f"{company.name} added successfully.",
            )

            return redirect(
                "applications:create"
            )

    else:

        form = CompanyForm()

    return render(
        request,
        "applications/company_form.html",
        {
            "form": form,
        },
    )


# =========================================================
# CREATE INTERVIEW
# =========================================================

@login_required
def interview_create(request, application_id):

    application = get_object_or_404(
        JobApplication,
        pk=application_id,
        user=request.user,
    )

    if request.method == "POST":

        form = InterviewForm(
            request.POST
        )

        if form.is_valid():

            interview = form.save(
                commit=False
            )

            interview.application = application

            interview.save()

            messages.success(
                request,
                "Interview added successfully.",
            )

            return redirect(
                "applications:detail",
                pk=application.pk,
            )

    else:

        form = InterviewForm()

    return render(
        request,
        "applications/interview_form.html",
        {
            "form": form,
            "application": application,
        },
    )


# =========================================================
# INTERVIEW WORKSPACE
# =========================================================

@login_required
def interview_list(request):

    today = timezone.localdate()

    interviews = Interview.objects.filter(
        application__user=request.user
    ).select_related(
        "application",
        "application__company",
    )

    todays_interviews = interviews.filter(
        interview_date=today
    ).order_by(
        "interview_time"
    )

    upcoming_interviews = interviews.filter(
        interview_date__gt=today
    ).order_by(
        "interview_date",
        "interview_time"
    )

    completed_interviews = interviews.filter(
        interview_date__lt=today
    ).order_by(
        "-interview_date",
        "-interview_time"
    )

    context = {

        "todays_interviews":
            todays_interviews,

        "upcoming_interviews":
            upcoming_interviews,

        "completed_interviews":
            completed_interviews,

        "total_interviews":
            interviews.count(),

        "today_count":
            todays_interviews.count(),

        "upcoming_count":
            upcoming_interviews.count(),

        "completed_count":
            completed_interviews.count(),

    }

    return render(
        request,
        "applications/interview_list.html",
        context,
    )


# =========================================================
# FOLLOW-UP WORKSPACE
# =========================================================

@login_required
def follow_up_list(request):

    today = timezone.localdate()

    follow_ups = FollowUp.objects.filter(
        application__user=request.user
    ).select_related(
        "application",
        "application__company",
    )

    overdue_follow_ups = follow_ups.filter(
        completed=False,
        follow_up_date__lt=today,
    ).order_by(
        "follow_up_date"
    )

    todays_follow_ups = follow_ups.filter(
        completed=False,
        follow_up_date=today,
    ).order_by(
        "follow_up_date"
    )

    upcoming_follow_ups = follow_ups.filter(
        completed=False,
        follow_up_date__gt=today,
    ).order_by(
        "follow_up_date"
    )

    completed_follow_ups = follow_ups.filter(
        completed=True
    ).order_by(
        "-follow_up_date",
        "-created_at",
    )

    context = {

        "total_follow_ups":
            follow_ups.count(),

        "overdue_count":
            overdue_follow_ups.count(),

        "today_count":
            todays_follow_ups.count(),

        "upcoming_count":
            upcoming_follow_ups.count(),

        "overdue_follow_ups":
            overdue_follow_ups,

        "todays_follow_ups":
            todays_follow_ups,

        "upcoming_follow_ups":
            upcoming_follow_ups,

        "completed_follow_ups":
            completed_follow_ups,

    }

    return render(
        request,
        "applications/follow_up_list.html",
        context,
    )


# =========================================================
# CREATE FOLLOW-UP
# =========================================================

@login_required
def follow_up_create(request, application_id):

    application = get_object_or_404(
        JobApplication,
        pk=application_id,
        user=request.user,
    )

    if request.method == "POST":

        form = FollowUpForm(
            request.POST
        )

        if form.is_valid():

            follow_up = form.save(
                commit=False
            )

            follow_up.application = application

            follow_up.save()

            messages.success(
                request,
                "Follow-up added successfully.",
            )

            return redirect(
                "applications:follow_up_list"
            )

    else:

        form = FollowUpForm()

    return render(
        request,
        "applications/follow_up_form.html",
        {
            "form": form,
            "application": application,
        },
    )


# =========================================================
# COMPLETE FOLLOW-UP
# =========================================================

@login_required
def follow_up_complete(request, pk):

    follow_up = get_object_or_404(
        FollowUp,
        pk=pk,
        application__user=request.user,
    )

    if request.method == "POST":

        follow_up.completed = True

        follow_up.save(
            update_fields=[
                "completed",
            ]
        )

        messages.success(
            request,
            "Follow-up marked as completed.",
        )

    return redirect(
        "applications:follow_up_list"
    )