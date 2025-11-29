import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Category, CustomArg

class EmailService:
    """Email service using SendGrid"""
    