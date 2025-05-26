from django.core.mail import send_mail
import random

def send_verification_email(to_email, subject, message):
    send_mail(
        subject,
        message,
        'your_email@gmail.com',
        [to_email],
        fail_silently=False,
    )
    

def generate_code(length=6):
    return ''.join(random.choices('0123456789', k=length))