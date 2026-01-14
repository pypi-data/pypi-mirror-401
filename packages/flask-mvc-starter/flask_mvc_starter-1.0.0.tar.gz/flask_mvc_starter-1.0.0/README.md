# Flask MVC Starter

A simple Flask boilerplate generator with MVC architecture, JWT authentication, caching, and async tasks.

## Installation

```bash
pip install flask-mvc-starter
```

## Quick Start

Create a new Flask MVC project:

```bash
flask-mvc-starter init myproject
cd myproject
```

## Setup Your Project

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Redis

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis
```

**macOS:**
```bash
brew install redis
brew services start redis
```

**Windows:** Download from https://redis.io/download

### 4. Setup Environment

```bash
cp .env.example .env
```

Edit `.env` and set:
- `SECRET_KEY` - Any random string
- `JWT_SECRET_KEY` - Any random string
- `MAIL_USERNAME` - Your Gmail address
- `MAIL_PASSWORD` - Gmail app password (get from https://myaccount.google.com/apppasswords)

### 5. Run the Application

**Start Flask server:**
```bash
python run.py
```

**Terminal 2 - Celery Worker:**
```bash
celery -A tasks worker --loglevel=info
```

**Terminal 3 - Celery Beat (for scheduled tasks):**
```bash
celery -A tasks beat --loglevel=info
```

## API Endpoints

- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login
- `GET /api/cache/time` - Cached time example
- `POST /api/cache/clear` - Clear cache
- `POST /api/tasks/email` - Trigger async email
- `POST /api/tasks/async` - Trigger async job

## Scheduled Tasks

Daily reminder email sent to all users at 8 AM (runs automatically when Celery Beat is running).

## Features

- MVC architecture (Models, Controllers, Utils)
- Flask-RESTful API endpoints
- JWT authentication
- SQLAlchemy ORM
- Redis caching
- Celery async tasks
- Scheduled tasks (Celery Beat)
- Flask-Mail integration

## Notes

- Redis must be running for caching and Celery
- All three terminals (Flask, Worker, Beat) need to be running
- Database: SQLite (`app.db`)

## Development

To contribute or modify this package:

```bash
git clone <repository-url>
cd flask-mvc-starter
pip install -e .
```

## License

MIT License
