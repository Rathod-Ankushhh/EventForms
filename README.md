# EventForms

EventForms is a Django-based event management platform that allows users to discover events, register for them, and manage event submissions through organizer accounts.

## Features

- Browse and search events by name and venue
- View detailed event information
- Register for events
- Track available seats
- Prevent duplicate registrations
- Organizer signup and login
- Dedicated organizer dashboard
- Create and submit events for approval
- Admin approval and rejection of events
- Trusted organizer functionality
- Export registrations as CSV through Django Admin

## Technologies Used

- Python
- Django
- SQLite (local development)
- PostgreSQL (production deployment)
- HTML5
- CSS3
- Bootstrap
- Gunicorn
- WhiteNoise

## Local Setup

1. Clone the repository:

   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   cd EventForms-main
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment (Windows):

   ```powershell
   .\venv\Scripts\Activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

7. Open your browser:

   http://127.0.0.1:8000/

## Project Structure

```text
EventForms/
├── eventforms/
├── registrations/
├── manage.py
├── requirements.txt
├── build.sh
└── README.md
```

## Project Status

Core development completed. Deployment preparation in progress.
