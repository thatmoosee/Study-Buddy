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

This project uses a hybrid **MVC + N-Tier Architecture** following industry best practices.

## System Architecture

Study Buddy implements a 6-layer N-Tier architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    Layer 1: Presentation                     │
│              (HTML, CSS, JavaScript - Frontend)              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Layer 2: Controller Layer                  │
│           (Flask Routes in app.py - Request Handlers)        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Layer 3: Service Layer                     │
│         (Business Logic - AuthService, GroupService,         │
│      FriendService, ChatService, ProfileService, etc.)       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  Layer 4: Repository Layer                   │
│          (Data Access - UserRepository, GroupRepository,     │
│         FriendRepository, ChatRepository, etc.)              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Layer 5: Model Layer                      │
│        (Domain Entities - User, Group, Friend, Chat,         │
│           Profile, Notification, StudyScheduler)             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  Layer 6: Data Storage Layer                 │
│              (JSON Files - users.json, groups.json,          │
│          friends.json, chats.json, notifications.json)       │
└─────────────────────────────────────────────────────────────┘
```

## Architecture Diagram

<img width="1310" height="873" alt="grpex7" src="https://github.com/user-attachments/assets/a3bd4668-504d-497c-bb44-9ceb54d9c1a5" />

## Architecture Overview

### Communication Flow

The application follows strict separation of concerns with unidirectional data flow:

1. **Frontend → Controller:** User interactions trigger HTTP requests from JavaScript to Flask endpoints
2. **Controller → Service:** Controllers delegate all business logic to service layer
3. **Service → Repository:** Services use repositories for all data operations
4. **Repository → Model:** Repositories create and return model objects
5. **Model → Storage:** Models are serialized to JSON files

**Example Flow (Creating a Study Group):**
```
header.js (Frontend)
    ↓ POST /api/group/create
app.py (Controller)
    ↓ group_service.create_group()
group_service.py (Service)
    ↓ group_repo.add(group)
group_repository.py (Repository)
    ↓ save to groups.json
groups.json (Storage)
```

### Design Patterns Used

1. **Service Pattern:** All business logic encapsulated in service classes (demonstrates SRP)
2. **Repository Pattern:** Data access abstracted through repository interfaces
3. **Singleton Pattern:** Service classes instantiated once via Flask dependency injection
4. **Template Method Pattern:** BaseRepository defines common CRUD operations
5. **Validator Pattern:** Input validation separated into dedicated validator classes

### SOLID Principles Compliance

- **Single Responsibility Principle (SRP):**
  - Controllers: Only handle HTTP requests/responses
  - Services: Only contain business logic
  - Repositories: Only handle data persistence
  - Models: Only represent domain entities

- **Open/Closed Principle (OCP):**
  - BaseRepository allows extension without modification
  - BaseValidator provides extensible validation framework

- **Liskov Substitution Principle (LSP):**
  - All repositories implement BaseRepository interface
  - All validators implement BaseValidator interface

- **Interface Segregation Principle (ISP):**
  - Each service has focused, minimal interface
  - Repositories expose only necessary methods

- **Dependency Inversion Principle (DIP):**
  - Services depend on repository abstractions, not concrete implementations
  - Controllers depend on service abstractions

---

## Package & Class Descriptions

### Frontend Package (`frontend/`)

**Purpose:** User interface and client-side logic

**Files:**
- `index.html`, `login.html`, `register.html` - Authentication pages
- `profile.html`, `editProfile.html` - User profile management
- `groups.html` - Study group management
- `friends_list.html`, `search_student.html` - Friend system
- `chats.html`, `chat.html` - Messaging interface
- `notifications.html`, `add_notifications.html` - Notification system
- `filter_by_class.html`, `filter_free_time.html` - Group filtering
- `header.js` - Navigation and session management
- `style.css`, `profile.css` - Styling

### Controller Package (`backend/app.py`)

**Purpose:** HTTP request handling and routing

**Key Route Groups:**
- **Authentication Routes (7):** `/api/auth/*` - Registration, login, logout, password reset
- **Group Routes (6):** `/api/group/*` - Create, join, leave, list, filter groups
- **Friend Routes (6):** `/api/friend/*` - Send, accept, reject requests, list friends
- **Chat Routes (8):** `/api/chat/*` - Create, join, send messages, list chats
- **Notification Routes (3):** `/api/notifications/*` - Get, mark read, delete
- **Schedule Routes (3):** `/api/study_schedule/*` - Create, get, delete sessions
- **Profile Routes (2):** `/api/profile/*` - Upload/update profiles

**Total: 35+ API endpoints**

### Service Package (`backend/services/`)

**Purpose:** Business logic and workflow orchestration

**Classes:**

1. **AuthService** (`auth_service.py`)
   - Methods: `register()`, `login()`, `logout()`, `request_password_reset()`, `reset_password()`
   - Responsibilities: User authentication, password management, token validation

2. **GroupService** (`group_service.py`)
   - Methods: `create_group()`, `join_group()`, `leave_group()`, `list_all_groups()`, `get_user_groups()`, `filter_by_specified_class()`, `filter_by_study_times()`
   - Responsibilities: Study group lifecycle, membership management, filtering

3. **FriendService** (`friend_service.py`)
   - Methods: `send_friend_request()`, `accept_friend_request()`, `reject_friend_request()`, `remove_friend()`, `get_pending_requests()`, `get_friends_list()`
   - Responsibilities: Friendship workflow, request handling, status management

4. **ChatService** (`chat_service.py`)
   - Methods: `create_chat()`, `join_chat()`, `leave_chat()`, `send_message()`, `create_DM()`, `list_all_chats()`
   - Responsibilities: Chat room management, messaging, DM handling

5. **ProfileService** (`profile_service.py`)
   - Methods: `create_profile()`, `update_profile()`, `get_profile_by_user_id()`, `upload_profile()`
   - Responsibilities: User profile CRUD operations

6. **NotificationService** (`notification_service.py`)
   - Methods: `send_notification()`, `get_notifications()`, `mark_notifications_as_read()`, `delete_notification()`
   - Responsibilities: Notification lifecycle and delivery

7. **SchedulerService** (`scheduler_services.py`)
   - Methods: `create_study_scheduler()`, `get_sessions()`, `get_user_sessions()`, `delete_session()`
   - Responsibilities: Study session scheduling and time management

### Repository Package (`backend/repositories/`)

**Purpose:** Data persistence and retrieval abstraction

**Classes:**

1. **BaseRepository** (`base_repository.py`) - Abstract base class
   - Methods: `create()`, `find_by_id()`, `find_all()`, `update()`, `delete()`

2. **UserRepository** (`user_repository.py`)
   - Storage: `users.json`
   - Additional: `find_by_email()`

3. **GroupRepository** (`group_repository.py`)
   - Storage: `groups.json`
   - Additional: `get_groups_for_user()`, `filter_by()`, `find_by_name()`

4. **FriendRepository** (`friend_repository.py`)
   - Storage: `friends.json`
   - Additional: `find_friendship()`, `send_friend_request()`, `accept_friend_request()`

5. **ChatRepository** (`chat_repository.py`)
   - Storage: `chat.json`
   - Additional: `get()`, `add()`

6. **ProfileRepository** (`profile_repository.py`)
   - Storage: `profiles.json`
   - Additional: `find_by_user_id()`

7. **NotificationRepository** (`notification_repository.py`)
   - Storage: `notifications.json`
   - Additional: `find_by_user_id()`, `mark_as_read()`

8. **StudySchedulerRepository** (`study_scheduler_repository.py`)
   - Storage: `schedule.json`
   - Additional: `find_by_user_id()`, `get_sessions_by_user()`

9. **PasswordResetTokenRepository** (`password_reset_token_repository.py`)
   - Storage: `password_reset_tokens.json`
   - Additional: `find_by_token()`, `delete_expired_tokens()`

### Model Package (`backend/models/`)

**Purpose:** Domain entities and business objects

**Classes:**

1. **BaseModel** (`base_model.py`) - Abstract base class
   - Properties: `id`, `created_at`
   - Methods: `to_dict()`, `validate()`

2. **User** (`user.py`)
   - Properties: `email`, `password_hash`, `is_active`
   - Methods: `verify_password()`, password hashing

3. **Group** (`group.py`)
   - Properties: `name`, `owner_id`, `members`, `study_times`, `specified_class`
   - Methods: `add_member()`, `remove_member()`

4. **Friend** (`friend.py`)
   - Properties: `user_id`, `friend_id`, `status` (pending/accepted/blocked)

5. **Chat** (`chat.py`)
   - Properties: `chat_id`, `name`, `members`, `messages`

6. **Profile** (`profile.py`)
   - Properties: `user_id`, `name`, `major`, `availability`, `preferences`

7. **Notification** (`notification.py`)
   - Properties: `user_id`, `message`, `read`, `created_at`

8. **StudyScheduler** (`study_scheduler.py`)
   - Properties: `user_id`, `title`, `start_time`, `end_time`

9. **PasswordResetToken** (`password_reset.py`)
   - Properties: `user_id`, `token`, `expires_at`, `is_used`
   - Methods: `is_valid()`

### Validator Package (`backend/validators/`)

**Purpose:** Input validation and data sanitization

**Classes:**

1. **BaseValidator** (`base_validator.py`) - Abstract base class
   - Methods: `validate()`, `_validate_required()`, `_validate_email()`

2. **UserValidator** (`user_validator.py`)
   - Validates: Email format, password strength

3. **ProfileValidator** (`profile_validator.py`)
   - Validates: User ID existence, profile data format

4. **PasswordResetValidator** (`password_reset_validator.py`)
   - Validates: Email format, token format, password requirements


---

## Functional Requirements

Study Buddy provides the following core functionalities:

1. **User Account Management**
   - User registration with email validation
   - Secure login with password hashing (bcrypt)
   - Password reset with token-based verification
   - Session management

2. **User Profile System**
   - Profile creation and editing
   - Display major, availability, and preferences
   - Profile search by email

3. **Study Group Management**
   - Create study groups with class and time specifications
   - Join/leave groups
   - Filter groups by class or study times
   - View all groups or user-specific groups

4. **Friend System**
   - Send friend requests by email
   - Accept/reject friend requests
   - View pending requests
   - Remove friends
   - Bidirectional friendship support

5. **Chat & Messaging**
   - Create group chats
   - Direct messaging (DM) between friends
   - Join/leave chat rooms
   - Send and receive messages
   - View chat history

6. **Notification System**
   - Receive notifications for friend requests, group invites, etc.
   - Mark notifications as read
   - Delete notifications

7. **Study Scheduler**
   - Create study sessions with start/end times
   - View user's study schedule
   - Delete scheduled sessions
   - Optional group association

## Non-Functional Requirements

1. **Security**
   - Password hashing using bcrypt
   - Input validation and sanitization
   - Token-based password reset
   - Session-based authentication

2. **Performance**
   - JSON-based storage for lightweight operations
   - Efficient data retrieval through repository pattern

3. **Maintainability**
   - Clean architecture with separation of concerns
   - Comprehensive unit tests (100+ test cases)
   - Well-documented code with docstrings
   - Consistent coding standards

4. **Scalability**
   - Modular design allows easy feature addition
   - Repository pattern enables database migration
   - Service layer abstracts business logic

5. **Usability**
   - RESTful API design
   - Clear error messages
   - Intuitive frontend interface

## Testing


## References
IEEE Guide to SRS

## Screenshots / Demo
(Insert screenshots)

## License
MIT or other license.
