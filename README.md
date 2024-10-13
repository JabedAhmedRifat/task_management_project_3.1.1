
# Team Management Project

This project is a **team management platform** built using Django and Django REST Framework. It allows for task and user management, including task history, notifications, quality control (QC) task tracking, and role-based permissions.

## Features

- **User Management:** User registration, login, password reset, and profile management.
- **Task Management:** Create, view, update, and delete tasks with detailed tracking.
- **Task History:** Logs and manages the task history to keep a record of all task-related activities.
- **Notifications & Notices:** Create and view notifications for team communication.
- **Quality Control (QC):** Dedicated views and actions for QC tasks, including status updates, user filtering, and status history.
- **Target Management:** Set, view, and track progress toward team targets.
- **Filtering & Search:** Advanced search and filtering for tasks, QC status, and users.
- **Authentication & Authorization:** Secure user authentication with Knox tokens, role-based access, and permissions for different views.

## Installation

### Prerequisites

- **Python 3.8+**
- **Django 4.2.6**
- **SQLite3** (default database)

### Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd team_management_project
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Migration:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server:**
   ```bash
   python manage.py runserver
   ```

The project will be accessible at `http://127.0.0.1:8000/`.

## API Endpoints

### Authentication Endpoints

- `POST /register/` - User registration
- `POST /login/` - User login
- `POST /logout/` - User logout
- `POST /reset-password/` - Request password reset
- `POST /set-new-password/` - Set a new password using reset link

### Task Endpoints

- `POST /task-create/` - Create a new task
- `GET /task-list/` - View all tasks
- `GET /task-detail/<int:pk>/` - View task details
- `PUT /task-update/<int:pk>/` - Update task
- `DELETE /task-delete/<int:pk>/` - Delete task

### Task History Endpoints

- `POST /task-history-create/` - Log a task history entry
- `GET /task-history-list/` - View task history
- `GET /task-history-detail/<int:pk>/` - View task history detail
- `PUT /task-history-update/<int:pk>/` - Update task history
- `DELETE /task-history-delete/<int:pk>/` - Delete task history entry

### Notification Endpoints

- `POST /notice-create/` - Create a notice
- `GET /notice-list/` - List all notices
- `GET /notice-detail/<int:pk>/` - Notice details
- `PUT /notice-update/<int:pk>/` - Update notice
- `DELETE /notice-delete/<int:pk>/` - Delete notice

### QC Task Endpoints

- `GET /qc-task-list/` - List all QC tasks
- `POST /qc-task-create/` - Create a QC task
- `GET /qc-task-detail/<int:pk>/` - QC task detail
- `PUT /qc-task-update/<int:pk>/` - Update QC task
- `DELETE /qc-task-delete/<int:pk>/` - Delete QC task

### User Management Endpoints

- `GET /list-user/` - List all users
- `GET /user-detail/<int:pk>/` - User detail
- `PUT /user-update/<int:pk>/` - Update user
- `DELETE /delete-user/<int:pk>/` - Delete user

For a full list of endpoints, refer to the project’s `urls.py`.

## Technology Stack

- **Backend Framework:** Django, Django REST Framework
- **Authentication:** Knox tokens
- **Database:** SQLite3
- **Others:** Django Filters, CORS headers

## Configuration

### Environment Variables

Update the following environment variables in your settings for email backend and security:

- `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` for SMTP email configuration.
- `SECRET_KEY` for Django project security.

### Static and Media Files

- **Static Files:** Collected at `BASE_DIR/staticfiles`
- **Media Files:** Served from `BASE_DIR/media`

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Contributing

If you would like to contribute to this project, please submit a pull request or open an issue for any bugs or feature requests.