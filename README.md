# Study Buddy App

## Table of Contents

-   [Overview](#overview)
-   [Purpose](#purpose)
-   [Scope](#scope)
-   [Definitions & Acronyms](#definitions--acronyms)
-   [System Overview](#system-overview)
-   [Functional Requirements](#functional-requirements)
-   [Non-Functional Requirements](#non-functional-requirements)
-   [Design & Development](#design--development)
    -   [Process Model](#process-model)
    -   [Deliverable 1 Highlights](#deliverable-1-highlights)
    -   [Class Diagrams](#class-diagrams)
    -   [Sequence Diagrams](#sequence-diagrams)
    -   [Development Progress](#development-progress)
-   [Testing](#testing)
-   [References](#references)
-   [Screenshots / Demo](#screenshots--demo)
-   [License](#license)

------------------------------------------------------------------------

## Overview

**Study Buddy** is a mobile and web application designed to connect
students in a class for collaboration and study sessions. The app
enables users to create accounts, manage profiles, search for
classmates, form and join study groups, chat, and schedule study
sessions. Unlike generic social media apps, Study Buddy is exclusively
focused on academic collaboration.

This repository contains the Software Requirements Specification (SRS)
document, design artifacts, and development updates for the first
deliverable of the project.

## Purpose

The purpose of this project is to develop a tool that fosters
collaboration among students by providing a centralized platform for:

-   Account management (sign-up, login/logout, profile management)
-   Finding and connecting with classmates
-   Creating, joining, and managing study groups
-   Scheduling study sessions
-   Chatting with individuals or groups
-   Setting preferences (time/location)
-   Notifications, reminders, and group ratings

The intended audience includes project stakeholders, developers,
testers, and course instructors evaluating the project.

## Scope

-   **Supported Platforms:** iOS, Android, and major browsers\
-   **Core Features:** Accounts, profiles, searching, groups, chat,
    scheduling\
-   **Not Included:** Full social-media features or unrelated
    integrations

## Definitions & Acronyms

  Term   Definition
  ------ -------------------------------------
  SRS    Software Requirements Specification
  UI     User Interface
  DB     Database
  App    Application

## System Overview

-   **Perspective:** Standalone academic collaboration tool\
-   **Users:** College students with basic technology skills\
-   **Environment:** Mobile + Web with cloud backend\
-   **Dependencies:** Internet access, school email sign-up

## Functional Requirements

### User Account Management

-   Account creation\
-   Login/logout\
-   Profile edits

### Classmate Search & Groups

-   Search by name/email\
-   Filter by class or availability\
-   Create/join/leave groups

### Study & Communication

-   Schedule sessions\
-   Chat (1:1 or group)\
-   Preferences & reminders\
-   Notifications\
-   Group ratings\
-   Password reset

## Non-Functional Requirements

-   **Performance:** Updates under 5 seconds\
-   **Reliability:** Error handling + retries\
-   **Availability:** 90% uptime\
-   **Security:** Access control\
-   **Maintainability:** Bug fixes within 1 week\
-   **Portability:** Works on Chrome/Firefox/Edge

## Design & Development

### Process Model -- Scrum

-   2‑week sprints, daily standups\
-   Adaptable, feedback-driven

### Deliverable 1

-   Login/logout complete\
-   Profile editing complete\
-   Classmate search + filtering complete

### Diagrams

-   Class diagrams for Group/Profile\
-   Sequence diagrams for account workflows

## Testing

  Test \#   Requirement   Format      Technique   Notes
  --------- ------------- ----------- ----------- -----------------
  T1        3.2.1         Demo        ---         Android demo
  T2        3.1.2         Unit Test   Blackbox    Login
  T3        3.1.3         Unit Test   Whitebox    Logout
  T4        3.1.4         Smoke       ---         Profile updates

### Example Test

-   Input: username + password\
-   Output: successful login\
-   Result: **Pass**

## References

-   IEEE SRS Guidelines\
-   Course lecture materials

## Screenshots / Demo

*(Add screenshots here)*

## License

Specify your license (MIT, GPL, etc.) here.
