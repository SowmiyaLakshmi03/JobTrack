from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import (
    Company,
    JobApplication,
    Interview,
    FollowUp,
)


# =========================================================
# COMPANY FORM
# =========================================================

class CompanyForm(forms.ModelForm):

    class Meta:

        model = Company

        fields = [
            "name",
            "website",
            "location",
            "industry",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Google",
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "placeholder": "https://example.com",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Chennai, India",
                }
            ),

            "industry": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Technology",
                }
            ),
        }

    def clean_name(self):

        name = self.cleaned_data["name"].strip()

        if not name:
            raise ValidationError(
                "Company name is required."
            )

        return name

    def clean_website(self):

        website = self.cleaned_data.get("website", "").strip()

        return website

    def clean_location(self):

        return self.cleaned_data.get(
            "location",
            ""
        ).strip()

    def clean_industry(self):

        return self.cleaned_data.get(
            "industry",
            ""
        ).strip()


# =========================================================
# JOB APPLICATION FORM
# =========================================================

class JobApplicationForm(forms.ModelForm):

    class Meta:

        model = JobApplication

        fields = [
            "company",
            "job_title",
            "job_type",
            "work_mode",
            "location",
            "salary",
            "application_date",
            "status",
            "job_url",
            "notes",
        ]

        widgets = {

            "company": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "job_title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Python Developer",
                }
            ),

            "job_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "work_mode": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Chennai, India",
                }
            ),

            "salary": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 600000",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "application_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "job_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://...",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Add useful notes about this application...",
                    "rows": 5,
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["company"].empty_label = "Select a company"

        self.fields["job_title"].label = "Job Title"

        self.fields["job_type"].label = "Job Type"

        self.fields["work_mode"].label = "Work Mode"

        self.fields["application_date"].label = "Application Date"

        self.fields["job_url"].label = "Job Posting URL"

        self.fields["notes"].label = "Notes"

    def clean_job_title(self):

        job_title = self.cleaned_data["job_title"].strip()

        if not job_title:
            raise ValidationError(
                "Job title is required."
            )

        return job_title

    def clean_location(self):

        return self.cleaned_data.get(
            "location",
            ""
        ).strip()

    def clean_salary(self):

        salary = self.cleaned_data.get("salary")

        if salary is not None and salary < 0:

            raise ValidationError(
                "Salary cannot be negative."
            )

        return salary

    def clean_application_date(self):

        application_date = self.cleaned_data.get(
            "application_date"
        )

        if (
            application_date
            and application_date > timezone.localdate()
        ):

            raise ValidationError(
                "Application date cannot be in the future."
            )

        return application_date

    def clean_job_url(self):

        return self.cleaned_data.get(
            "job_url",
            ""
        ).strip()

    def clean_notes(self):

        return self.cleaned_data.get(
            "notes",
            ""
        ).strip()


# =========================================================
# INTERVIEW FORM
# =========================================================

class InterviewForm(forms.ModelForm):

    class Meta:

        model = Interview

        fields = [
            "round_name",
            "interview_date",
            "interview_time",
            "interview_type",
            "meeting_link",
            "interviewer",
            "result",
            "notes",
        ]

        widgets = {

            "round_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Technical Interview",
                }
            ),

            "interview_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "interview_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            "interview_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "meeting_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://meet.google.com/...",
                }
            ),

            "interviewer": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Hiring Manager",
                }
            ),

            "result": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Interview preparation notes, questions, feedback...",
                    "rows": 5,
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["round_name"].label = "Interview Round"

        self.fields["interview_date"].label = "Interview Date"

        self.fields["interview_time"].label = "Interview Time"

        self.fields["interview_type"].label = "Interview Type"

        self.fields["meeting_link"].label = "Meeting Link"

        self.fields["interviewer"].label = "Interviewer"

        self.fields["result"].label = "Result"

        self.fields["notes"].label = "Interview Notes"

    def clean_round_name(self):

        round_name = self.cleaned_data[
            "round_name"
        ].strip()

        if not round_name:

            raise ValidationError(
                "Interview round is required."
            )

        return round_name

    def clean_meeting_link(self):

        return self.cleaned_data.get(
            "meeting_link",
            ""
        ).strip()

    def clean_interviewer(self):

        return self.cleaned_data.get(
            "interviewer",
            ""
        ).strip()

    def clean_notes(self):

        return self.cleaned_data.get(
            "notes",
            ""
        ).strip()


# =========================================================
# FOLLOW-UP FORM
# =========================================================

class FollowUpForm(forms.ModelForm):

    class Meta:

        model = FollowUp

        fields = [
            "follow_up_date",
            "title",
            "notes",
        ]

        widgets = {

            "follow_up_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Follow up with recruiter",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Add follow-up details or reminders...",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["follow_up_date"].label = "Follow-up Date"

        self.fields["title"].label = "Follow-up Title"

        self.fields["notes"].label = "Notes"

    def clean_title(self):

        title = self.cleaned_data["title"].strip()

        if not title:

            raise ValidationError(
                "Follow-up title is required."
            )

        return title

    def clean_notes(self):

        return self.cleaned_data.get(
            "notes",
            ""
        ).strip()