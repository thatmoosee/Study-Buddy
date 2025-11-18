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

### Layer 1 — Presentation Layer  
Consists of HTML pages and frontend assets. Sends requests to controllers and displays returned data.

### Layer 2 — Application Layer  
Controllers (in `app.py`) handle routes and serve as the "C" in MVC.  
Services perform business logic.  
Validators enforce input structure and rules.

### Layer 3 — Data Layer  
Models represent database entities.  
Repositories abstract data operations.

Communication Example:  
- `GroupController` → calls `group_service`  
- `group_service` → uses `GroupRepository`  
- `GroupRepository` → returns `Group` model data to service → controller → HTML view

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
