from flask import Flask
from flask_mail import Message
from tasks import celery_app
from app.extensions import mail, db
from app.models import User


@celery_app.task
def send_email_async(subject, recipients, body, html=None):
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    with app.app_context():
        mail.init_app(app)
        db.init_app(app)
        msg = Message(
            subject=subject,
            recipients=recipients,
            body=body,
            html=html
        )
        mail.send(msg)
    
    return f'Email sent to {recipients}'


@celery_app.task
def send_daily_reminder():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    with app.app_context():
        mail.init_app(app)
        db.init_app(app)
        
        users = User.query.all()
        recipient_emails = [user.email for user in users]
        
        if not recipient_emails:
            return 'No users to send reminder to'
        
        msg = Message(
            subject='Daily Reminder',
            recipients=recipient_emails,
            body='This is your daily reminder! Have a great day!',
            html='<h1>Daily Reminder</h1><p>This is your daily reminder! Have a great day!</p>'
        )
        mail.send(msg)
    
    return f'Daily reminder sent to {len(recipient_emails)} users'


@celery_app.task
def process_async_job(data):
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    with app.app_context():
        result = f'Processed: {data}'
        return result
