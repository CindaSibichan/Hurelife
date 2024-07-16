from twilio.rest import Client
from django.conf import settings
import random

def generate_otp():
    return random.randint(100000, 999999)


def send_otp_num(number):
    """Send OTP to the specified mobile number using Twilio"""
    otp = generate_otp()
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'Your OTP is {otp}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=number
    )
    return otp
