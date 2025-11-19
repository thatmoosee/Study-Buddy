# Study Buddy App

## Table of Contents
- [Overview](#overview)
- [Purpose](#purpose)
- [Scope](#scope)
- [Definitions & Acronyms](#definitions--acronyms)
- [System Overview](#system-overview)
- [Software Architecture](#software-architecture)
- [Functional Requirements](#functional-requirements)
- [Non-Functional Requirements](#non-functional-requirements)
- [Design & Development](#design--development)
- [Testing](#testing)
- [References](#references)
- [Screenshots / Demo](#screenshots--demo)
- [License](#license)

---

## Overview
Study Buddy is a mobile and web application designed to connect students for study sessions.

## Purpose
The purpose of Study Buddy is to provide a centralized platform for academic collaboration.

## Scope
- iOS, Android, and Web
- Core features: accounts, profiles, groups, chat, scheduling

## Definitions & Acronyms
| Term | Definition |
|------|-----------|
| SRS | Software Requirements Specification |
| UI | User Interface |
| DB | Database |

---

# Software Architecture

This project uses a hybrid **MVC + N-Tier Architecture**.

## Architecture Diagram 

<img width="1310" height="873" alt="grpex7" src="https://github.com/user-attachments/assets/a3bd4668-504d-497c-bb44-9ceb54d9c1a5" />

## Architecture Explanation

- Arrow A: header.js → app.py (HTTP request from frontend to controller)

- Arrow B: app.py → profile.py (routing dispatch)

- Arrow C: profile.py → group_service.py (controller calling service)

- Arrow D: group_service.py → group_repository.py (service reading DB)

- Arrow E: group_repository.py → Main DB (SQL query execution)

### Layer 1: Frontend 
Consists of header.js, HTML pages and css. Sends requests to controllers and displays returned data.

HTML Templates:
- add_notifications.html
- chats.html
- filter_by_class.html
- filter_free_time.html
- index.html
- profile.html
- search.html

Javascript:

- header.js

CSS:
- style.css

### Layer 2: Backend
Controllers (in `app.py`) profile.py and user.py handle routes and serve as the "C" in MVC.  
Services perform business logic.  
Validators enforce input structure and rules.

Services:
- auth_service.py
- group_service.py
- profile_service.py

Validators:
- base_validator.py
- user_validator.py

### Layer 3: Database 
Models represent database entities.  
Repositories abstract data operations.

Communication Example:  
- `GroupController` → calls `group_service`  
- `group_service` → uses `GroupRepository`  
- `GroupRepository` → returns `Group` model data to service → controller → HTML view

Models:
- base_models.py
- course.py
- group.py
- profile.py
- user.py

Repositories:
- base_repository.py
- group_repository.py
- user_repository.py


---

## Functional Requirements
(details omitted for brevity)

## Non-Functional Requirements
(details omitted for brevity)

## Design & Development
(details omitted for brevity)

## Testing
(details omitted for brevity)

## References
IEEE Guide to SRS

## Screenshots / Demo
(Insert screenshots)

## License
MIT or other license.
