#Study-Buddy
Study Buddy App
Overview
Study Buddy is a mobile and web application designed to connect students in a class for collaboration and study sessions. This application allows users to create accounts, manage profiles, search for classmates, form and join study groups, chat, and schedule study sessions. Unlike generic social media apps, Study Buddy is exclusively focused on academic collaboration, enabling students to maximize productivity and peer learning.
This repository contains the Software Requirements Specification (SRS) document, design artifacts, and development updates for the first deliverable of the project.
________________________________________
Purpose
The purpose of this project is to develop a tool that fosters collaboration among students by providing a centralized platform for:
•	Account management (sign-up, login/logout, profile management)
•	Finding and connecting with classmates
•	Creating, joining, and managing study groups
•	Scheduling study sessions
•	Chatting with individuals and groups
•	Receiving notifications and reminders for scheduled activities
The intended audience includes project stakeholders, developers, testers, and course instructors evaluating the project.
________________________________________
Scope
•	Supported Platforms: iOS, Android, and Web browsers (Chrome, Firefox, Edge)
•	Core Features: User accounts, profile management, group formation and management, chat functionality, scheduling, notifications
•	Exclusions: Unrelated social media features, third-party integrations beyond basic notifications
________________________________________
Definitions & Acronyms
Term	Definition
SRS	Software Requirements Specification
UI	User Interface
DB	Database
App	Application
________________________________________
System Overview
•	Product Perspective: Study Buddy is a standalone application that differentiates itself by focusing exclusively on academic collaboration. It offers group scheduling, class-based filtering, and study-specific matching, unlike typical chat apps.
•	User Characteristics: Target users are university students with basic technical skills required to use web and mobile applications.
•	System Environment: Mobile devices (iOS, Android) and web browsers, with cloud-based backend services for authentication, data storage, and group management.
•	Assumptions & Dependencies: Users have internet access and register using school emails. Dependencies include mobile OS updates, cloud hosting, and notification services.
________________________________________
Functional Requirements
User Account Management
•	Create Account: Users can register with email and password.
•	Sign In / Log Out: Users can log in and out securely.
•	Profile Management: Upload and update profile info including name, major, and availability.
Classmate Search & Group Management
•	Search classmates by name or email
•	Filter by class or free time
•	Match with or create study groups
•	Join or leave groups
Study & Communication Features
•	Schedule study sessions within groups
•	Chat with individuals or groups
•	Set study preferences (time/location)
•	Receive notifications for sessions and updates
•	Maintain friends list and send reminders
•	Rate groups after study sessions
•	Reset password functionality
________________________________________
Non-Functional Requirements
•	Performance: Support multiple concurrent users; chat and group updates under 5 seconds
•	Reliability: Minimal errors; retry requests in case of failure
•	Availability: 90% uptime
•	Security: Encapsulated data access, role-based permissions
•	Maintainability: Bug fixes addressed within 1 week
•	Portability: Works on Chrome, Firefox, Edge; mobile and desktop
________________________________________
Design & Development
Process Model
•	Scrum Model: Iterative and incremental development through 2-week sprints
•	Daily Stand-ups: 6:30–7:30 PM for progress tracking and collaboration
•	Justification: Allows frequent stakeholder feedback, adaptability to requirement changes, and team accountability
Deliverable 1 Highlights
•	Finalized process design
•	Implemented foundational features:
o	User account creation and login/logout
o	Profile upload and update
o	Search and filter classmates by class and availability
Class Diagrams
•	Group Class Diagram: Manages members, courses, and group relationships
•	Profile Class Diagram: Distinguishes between private and public user information
Sequence Diagrams
•	Illustrate messages exchanged between user and system for account and profile management
Development Progress
•	Class and sequence diagrams completed for user/profile interactions
•	Screenshots and explanations included in Section 4.2.2.1 & 4.2.2.3 of SRS

