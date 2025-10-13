# Study Buddy App

## Table of Contents
- [Overview](#overview)
- [Purpose](#purpose)
- [Scope](#scope)
- [Definitions & Acronyms](#definitions--acronyms)
- [System Overview](#system-overview)
- [Functional Requirements](#functional-requirements)
- [Non-Functional Requirements](#non-functional-requirements)
- [Design & Development](#design--development)
  - [Process Model](#process-model)
  - [Deliverable 1 Highlights](#deliverable-1-highlights)
  - [Class Diagrams](#class-diagrams)
  - [Sequence Diagrams](#sequence-diagrams)
  - [Development Progress](#development-progress)
- [Testing](#testing)
- [References](#references)
- [Screenshots / Demo](#screenshots--demo)
- [License](#license)

---

## Overview

**Study Buddy** is a mobile and web application designed to connect students in a class for collaboration and study sessions. The app enables users to create accounts, manage profiles, search for classmates, form and join study groups, chat, and schedule study sessions. Unlike generic social media apps, Study Buddy is exclusively focused on academic collaboration.

This repository contains the Software Requirements Specification (SRS) document, design artifacts, and development updates for the first deliverable of the project.

## Purpose

The purpose of this project is to develop a tool that fosters collaboration among students by providing a centralized platform for:

- Account management (sign-up, login/logout, profile management)
- Finding and connecting with classmates
- Creating, joining, and managing study groups
- Scheduling study sessions
- Chatting with individuals and groups
- Receiving notifications and reminders for scheduled activities

The intended audience includes project stakeholders, developers, testers, and course instructors evaluating the project.

## Scope

- **Supported Platforms:** iOS, Android, and Web browsers (Chrome, Firefox, Edge)
- **Core Features:** User accounts, profile management, group formation and management, chat functionality, scheduling, notifications
- **Exclusions:** Unrelated social media features, third-party integrations beyond basic notifications

## Definitions & Acronyms

| Term | Definition |
|------|-----------|
| SRS  | Software Requirements Specification |
| UI   | User Interface |
| DB   | Database |
| App  | Application |

## System Overview

- **Product Perspective:** Standalone application focused on academic collaboration with group scheduling, class-based filtering, and study-specific matching.
- **User Characteristics:** University students with basic technical skills.
- **System Environment:** Mobile devices (iOS, Android) and web browsers, with cloud-based backend services.
- **Assumptions & Dependencies:** Users have internet access, register using school emails. Dependencies include mobile OS updates, cloud hosting, and notification services.

## Functional Requirements

### User Account Management

- **Create Account:** Users can register with email and password.
- **Sign In / Log Out:** Users can log in and out securely.
- **Profile Management:** Upload and update profile info including name, major, and availability.

### Classmate Search & Group Management

- Search classmates by name or email
- Filter by class or free time
- Match with or create study groups
- Join or leave groups

### Study & Communication Features

- Schedule study sessions within groups
- Chat with individuals or groups
- Set study preferences (time/location)
- Receive notifications for sessions and updates
- Maintain friends list and send reminders
- Rate groups after study sessions
- Reset password functionality

## Non-Functional Requirements

- **Performance:** Support multiple concurrent users; chat and group updates under 5 seconds
- **Reliability:** Minimal errors; retry requests in case of failure
- **Availability:** 90% uptime
- **Security:** Encapsulated data access, role-based permissions
- **Maintainability:** Bug fixes addressed within 1 week
- **Portability:** Works on Chrome, Firefox, Edge; mobile and desktop

## Design & Development

### Process Model

- **Scrum Model:** Iterative and incremental development through 2-week sprints
- **Daily Stand-ups:** 6:30–7:30 PM for progress tracking and collaboration
- **Justification:** Allows frequent stakeholder feedback, adaptability to requirement changes, and team accountability

### Deliverable 1 Highlights

- Finalized process design
- Implemented foundational features:
  - User account creation and login/logout
  - Profile upload and update
  - Search and filter classmates by class and availability

### Class Diagrams

- **Group Class Diagram:** Manages members, courses, and group relationships
- **Profile Class Diagram:** Distinguishes between private and public user information

### Sequence Diagrams

- Illustrate messages exchanged between user and system for account and profile management

### Development Progress

- Class and sequence diagrams completed for user/profile interactions
- Screenshots and explanations included in Section 4.2.2.1 & 4.2.2.3 of SRS

## Testing

| Test # | Requirement | Test Format | Technique | Notes |
|--------|------------|------------|----------|-------|
| T1     | 3.2.1      | Demonstration | - | Android tablet demo |
| T2     | 3.1.2      | Testing | Unit Testing (Blackbox) | Login verification |
| T3     | 3.1.3      | Testing | Unit Testing (Whitebox) | Logout verification |
| T4     | 3.1.4      | Testing | Smoke Testing | Profile upload & update |

**Example Test Case: User Login**

- Input:  
  - username: rsaripa@ilstu.edu  
  - password: test123  
  - Role: Faculty  
- Output: Successful login confirmation  
- Result: Pass

## References

- IEEE Guide to Software Requirements Specifications
- Course Materials and Lecture Notes

## Screenshots / Demo

*(Include images or links to the application if available)*

## License

Specify license (MIT, GPL, etc.) here.

