from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# =========================================================
# COMPANY
# =========================================================

class Company(models.Model):

    name = models.CharField(
        max_length=200
    )

    website = models.URLField(
        blank=True
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    industry = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "name"
        ]

    def __str__(self):

        return self.name


# =========================================================
# JOB APPLICATION
# =========================================================

class JobApplication(models.Model):

    class JobType(models.TextChoices):

        FULL_TIME = "FULL_TIME", "Full-time"

        PART_TIME = "PART_TIME", "Part-time"

        INTERNSHIP = "INTERNSHIP", "Internship"

        CONTRACT = "CONTRACT", "Contract"


    class WorkMode(models.TextChoices):

        REMOTE = "REMOTE", "Remote"

        HYBRID = "HYBRID", "Hybrid"

        ON_SITE = "ON_SITE", "On-site"


    class Status(models.TextChoices):

        APPLIED = "APPLIED", "Applied"

        SHORTLISTED = "SHORTLISTED", "Shortlisted"

        INTERVIEW = "INTERVIEW", "Interview"

        ASSESSMENT = "ASSESSMENT", "Assessment"

        OFFER = "OFFER", "Offer"

        REJECTED = "REJECTED", "Rejected"

        WITHDRAWN = "WITHDRAWN", "Withdrawn"

        ACCEPTED = "ACCEPTED", "Accepted"


    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="job_applications"

    )


    company = models.ForeignKey(

        Company,

        on_delete=models.CASCADE,

        related_name="job_applications"

    )


    job_title = models.CharField(

        max_length=200

    )


    job_type = models.CharField(

        max_length=20,

        choices=JobType.choices,

        default=JobType.FULL_TIME

    )


    work_mode = models.CharField(

        max_length=20,

        choices=WorkMode.choices,

        default=WorkMode.ON_SITE

    )


    location = models.CharField(

        max_length=200,

        blank=True

    )


    salary = models.DecimalField(

        max_digits=12,

        decimal_places=2,

        null=True,

        blank=True

    )


    application_date = models.DateField()


    status = models.CharField(

        max_length=20,

        choices=Status.choices,

        default=Status.APPLIED

    )


    job_url = models.URLField(

        blank=True

    )


    notes = models.TextField(

        blank=True

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )


    updated_at = models.DateTimeField(

        auto_now=True

    )


    class Meta:

        ordering = [

            "-application_date",

            "-created_at"

        ]


    # =====================================================
    # APPLICATION AGE
    # =====================================================

    @property
    def days_since_application(self):

        return (
            timezone.localdate()
            - self.application_date
        ).days


    # =====================================================
    # APPLICATION AGE LABEL
    # =====================================================

    @property
    def application_age_label(self):

        days = self.days_since_application

        if days == 0:

            return "Applied today"

        if days == 1:

            return "1 day ago"

        return f"{days} days ago"


    # =====================================================
    # ACTIVE APPLICATION
    # =====================================================

    @property
    def is_active_application(self):

        return self.status in [

            self.Status.APPLIED,

            self.Status.SHORTLISTED,

            self.Status.ASSESSMENT,

            self.Status.INTERVIEW,

            self.Status.OFFER,

        ]


    # =====================================================
    # STRING REPRESENTATION
    # =====================================================

    def __str__(self):

        return (
            f"{self.job_title} - "
            f"{self.company.name}"
        )


# =========================================================
# INTERVIEW
# =========================================================

class Interview(models.Model):

    class InterviewType(models.TextChoices):

        ONLINE = "ONLINE", "Online"

        PHONE = "PHONE", "Phone"

        IN_PERSON = "IN_PERSON", "In-person"


    class Result(models.TextChoices):

        PENDING = "PENDING", "Pending"

        PASSED = "PASSED", "Passed"

        FAILED = "FAILED", "Failed"


    application = models.ForeignKey(

        JobApplication,

        on_delete=models.CASCADE,

        related_name="interviews"

    )


    round_name = models.CharField(

        max_length=100

    )


    interview_date = models.DateField()


    interview_time = models.TimeField(

        null=True,

        blank=True

    )


    interview_type = models.CharField(

        max_length=20,

        choices=InterviewType.choices,

        default=InterviewType.ONLINE

    )


    meeting_link = models.URLField(

        blank=True

    )


    interviewer = models.CharField(

        max_length=200,

        blank=True

    )


    notes = models.TextField(

        blank=True

    )


    result = models.CharField(

        max_length=20,

        choices=Result.choices,

        default=Result.PENDING

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )


    class Meta:

        ordering = [

            "interview_date",

            "interview_time"

        ]


    def __str__(self):

        return (
            f"{self.round_name} - "
            f"{self.application.job_title}"
        )


# =========================================================
# FOLLOW-UP
# =========================================================

class FollowUp(models.Model):

    application = models.ForeignKey(

        JobApplication,

        on_delete=models.CASCADE,

        related_name="follow_ups"

    )


    follow_up_date = models.DateField()


    title = models.CharField(

        max_length=200

    )


    notes = models.TextField(

        blank=True

    )


    completed = models.BooleanField(

        default=False

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )


    class Meta:

        ordering = [

            "completed",

            "follow_up_date"

        ]


    def __str__(self):

        return self.title