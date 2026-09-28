# JobTrack — Job Application Tracker

A professional Django-based job application tracking platform designed to help job seekers organize applications, interviews, follow-ups, and their overall job-search workflow in one place.

## Overview

JobTrack is a full-stack web application built with Django and PostgreSQL.

It provides a centralized workspace where users can:

- Track job applications
- Monitor application status
- Search and filter applications
- Manage interviews
- Schedule follow-ups
- Track completed follow-ups
- View application activity timelines
- Monitor their job-search progress through a dashboard

The project focuses on a clean, responsive, and practical user experience rather than a basic CRUD interface.

---

## Features

### 📊 Smart Dashboard

The dashboard provides a quick overview of the current job search.

It includes:

- Total applications
- Application status overview
- Application pipeline
- Upcoming interviews
- Today's interview alerts
- Recent applications
- Applications requiring attention

---

### 📋 Application Management

Users can create and manage job applications with details such as:

- Company
- Job title
- Job type
- Work mode
- Location
- Salary
- Application date
- Application status
- Job posting URL
- Notes

Supported application statuses include:

- Applied
- Shortlisted
- Assessment
- Interview
- Offer
- Rejected
- Withdrawn
- Accepted

---

### 🔎 Search, Filtering & Sorting

Applications can be organized using:

- Keyword search
- Company search
- Job title search
- Location search
- Status filtering
- Job type filtering
- Work mode filtering
- Sorting by date
- Sorting by job title
- Sorting by company
- Sorting by status

---

### 🎯 Application Pipeline

JobTrack provides a visual application pipeline to understand where applications currently stand.

```text
Applied
   ↓
Shortlisted
   ↓
Assessment
   ↓
Interview
   ↓
Offer
   ↓
Accepted