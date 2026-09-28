from django.urls import path

from . import views

app_name = "applications"


urlpatterns = [

    # =====================================================
    # APPLICATIONS
    # =====================================================

    path(
        "",
        views.application_list,
        name="list",
    ),

    path(
        "add/",
        views.application_create,
        name="create",
    ),

    path(
        "<int:pk>/",
        views.application_detail,
        name="detail",
    ),

    path(
        "<int:pk>/edit/",
        views.application_update,
        name="update",
    ),

    path(
        "<int:pk>/delete/",
        views.application_delete,
        name="delete",
    ),


    # =====================================================
    # COMPANIES
    # =====================================================

    path(
        "companies/add/",
        views.company_create,
        name="company_create",
    ),


    # =====================================================
    # INTERVIEWS
    # =====================================================

    path(
        "interviews/",
        views.interview_list,
        name="interview_list",
    ),

    path(
        "<int:application_id>/interview/add/",
        views.interview_create,
        name="interview_create",
    ),


    # =====================================================
    # FOLLOW-UPS
    # =====================================================

    path(
        "follow-ups/",
        views.follow_up_list,
        name="follow_up_list",
    ),

    path(
        "<int:application_id>/follow-up/add/",
        views.follow_up_create,
        name="follow_up_create",
    ),

    path(
        "follow-ups/<int:pk>/complete/",
        views.follow_up_complete,
        name="follow_up_complete",
    ),

]