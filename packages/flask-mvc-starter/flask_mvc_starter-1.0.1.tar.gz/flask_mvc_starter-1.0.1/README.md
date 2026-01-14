# Flask MVC Starter

A simple Flask boilerplate generator with MVC architecture, JWT authentication, caching, and async tasks.

## About

Flask MVC Starter helps you quickly bootstrap Flask applications with a clean MVC structure. It generates a production-ready boilerplate with:

- **MVC Architecture** - Models, Controllers, and Utils
- **JWT Authentication** - Secure token-based auth
- **SQLAlchemy ORM** - Database models and queries
- **Redis Caching** - Fast response caching
- **Celery Tasks** - Async and scheduled tasks
- **Flask-Mail** - Email integration

## Installation

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install flask-mvc-starter
```

## Quick Start

```bash
flask-mvc-starter init myproject
cd myproject
pip install -r requirements.txt
cp .env.example .env
python run.py
```

See [full documentation](templates/README.md) for detailed setup instructions.

## Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## Contact

- Email: contact.rajnishk@gmail.com
- LinkedIn: [0rajnishk](https://linkedin.com/in/0rajnishk)

## License

MIT License
