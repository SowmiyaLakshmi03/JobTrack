from django.contrib import admin
from django.urls import include, path

from applications import views


urlpatterns = [

    # =====================================================
    # ADMIN
    # =====================================================

    path(
        "admin/",
        admin.site.urls,
    ),


    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        "",
        views.dashboard,
        name="dashboard",
    ),


    # =====================================================
    # REGISTRATION
    # =====================================================

    path(
        "register/",
        views.register,
        name="register",
    ),


    # =====================================================
    # AUTHENTICATION
    # =====================================================

    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),


    # =====================================================
    # APPLICATIONS
    # =====================================================

    path(
        "applications/",
        include("applications.urls"),
    ),

]