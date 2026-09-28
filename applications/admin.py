from django.contrib import admin

from .models import Company, JobApplication, Interview, FollowUp


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
        "industry",
        "created_at",
    )

    search_fields = (
        "name",
        "location",
        "industry",
    )


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "job_title",
        "company",
        "user",
        "status",
        "job_type",
        "work_mode",
        "application_date",
    )

    list_filter = (
        "status",
        "job_type",
        "work_mode",
        "application_date",
    )

    search_fields = (
        "job_title",
        "company__name",
        "user__username",
    )

    date_hierarchy = "application_date"


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = (
        "round_name",
        "application",
        "interview_date",
        "interview_time",
        "interview_type",
        "result",
    )

    list_filter = (
        "interview_type",
        "result",
        "interview_date",
    )

    search_fields = (
        "round_name",
        "application__job_title",
        "application__company__name",
    )


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "application",
        "follow_up_date",
        "completed",
    )

    list_filter = (
        "completed",
        "follow_up_date",
    )

    search_fields = (
        "title",
        "application__job_title",
        "application__company__name",
    )