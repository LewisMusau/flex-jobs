 # Create your views here.
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages
from django.core.signing import TimestampSigner
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .models import User
from django.http import HttpResponse
from django.core.signing import BadSignature
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from django.forms.models import model_to_dict
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime
from django.contrib.auth import authenticate, login
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required





class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            # Check if passwords match
            if password1 == password2:
                try:
                    # Check if the email already exists in the database
                    existing_user = User.objects.get(email=email)
                    return render(request, 'register.html', {'error': 'Email already exists'})
                except User.DoesNotExist:
                    try:
                        # Check if user already exists
                        user = User.objects.get(username=username)
                        return render(request, 'register.html', {'error': 'Username already taken'})
                    except User.DoesNotExist:
                        # Create a new user account
                        user = User.objects.create_user(username=username, email=email, password=password1)
                        # Set the user as inactive until they activate their account
                        user.is_active = False
                        user.save()
                        messages.success(request, f'Account created for {username}!')

                        # Now you can use the user object and its datetime fields as needed
                        user_data = model_to_dict(user)

                        # Serialize user_data as JSON using the custom encoder
                        user_json = json.dumps(user_data, cls=CustomJSONEncoder)

                        # Continue with the rest of your code...
                        # Send the activation email
                        #send_activation_email(user)

        # Render the registration successful template with the username
                        return render(request, 'register_success.html', {'username': username})



            else:
                # Passwords don't match, handle the error
                return render(request, 'register.html', {'error': 'Passwords do not match'})
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})










def register_success(request):
    return render(request, 'register_success.html')

import random
import string
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User


import random
import time

# This dictionary will store the verification codes
verification_codes = {}

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings

def send_verification_code(email):
    code = random.randint(100000, 999999)
    verification_codes[email] = {
        'code': code,
        'timestamp': time.time()
    }

    subject = 'Verification Code'
    message = f'Your verification code is: {code}'

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = email
    msg['Subject'] = subject

    # Add the message body
    body = f"""
    <html>
    <body>
        <h2>Verification Code</h2>
        <p>Your verification code is: {code}</p>
    </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    # Send the email
    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        # Handle any errors that occur during sending
        print(f"Failed to send verification code email: {e}")


def resend_verification_code(email):
    # Check if the user has requested a code within the last 5 minutes
    if email in verification_codes:
        current_timestamp = time.time()
        last_timestamp = verification_codes[email]['timestamp']
        elapsed_time = current_timestamp - last_timestamp
        
        if elapsed_time < 300:  # 300 seconds = 5 minutes
            # The user needs to wait before requesting another code
            remaining_time = 300 - elapsed_time
            raise Exception(f"Please wait {remaining_time} seconds before requesting another code.")
    
    # If the user can request a new code, call the send_verification_code() function
    send_verification_code(email)


def myprofile(request):
    return render(request, 'profile.html')


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib import messages


from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is valid, log them in
            login(request, user)
            # Display success message
            messages.success(request, 'Login successful!')
            # Redirect to the dashboard
            return redirect('writers:dashboard')
        else:
            # User credentials are invalid, display error message
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error': error_message})
    else:
        return render(request, 'login.html')





from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

def password_reset(request):
    return render(request, 'password_reset.html')
def password_reset_success(request):
    return render(request, 'password_reset_success.html')


from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import get_user_model

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        repeat_password = request.POST.get('repeat_password')
        
        if new_password != repeat_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'forgot.html')
        
        User = get_user_model()
        try:
            # Retrieve the user with the provided email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email')
            return render(request, 'forgot.html')
        
        # Update user's password
        user.set_password(new_password)
        user.save()
        
        messages.success(request, 'Password updated successfully')
        return render(request, 'password_reset_success.html')
    else:
        return render(request, 'forgot.html')












def activate_account(request, token):
    signer = TimestampSigner()
    try:
        username = signer.unsign(token, max_age=86400)  # Verify token within 24 hours
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                user.is_active = True
                user.save()
                return redirect('account_activated')  #  'account_activated' with your desired URL name for successful activation
            else:
                return redirect('login')  #  'account_already_activated' with your desired URL name if the account is already activated
        except User.DoesNotExist:
            return redirect('login')  # 'invalid_token' with your desired URL name for invalid tokens
    except BadSignature:
        return redirect('login')  #'invalid_token' with your desired URL name for invalid tokens


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.shortcuts import render
from django.contrib.auth.models import User

def viewusers(request):
    user_list = User.objects.all()
    context = {'user_list': user_list}
    return render(request, 'viewusers.html', context)

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import uuid
# Import required modules
import random
import string

# Define the generate_activation_token function
def generate_activation_token():
    # Generate a random token using alphanumeric characters
    chars = string.ascii_letters + string.digits
    token = ''.join(random.choice(chars) for _ in range(32))

    return token


# Generate an activation token
activation_token = generate_activation_token()






from google.oauth2 import credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from google.oauth2 import credentials
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.conf import settings

def send_activation_email(email, activation_link):
    credentials = Credentials.from_authorized_user_file(os.path.join(settings.BASE_DIR, 'tokens.json'))
    service = build('gmail', 'v1', credentials=credentials)

    message = create_message(email, activation_link)
    send_message(service, 'me', message)

def create_message(to, activation_link):
    subject = 'Account Activation'
    message_text = f'''
    Hello,

    Please activate your account by clicking on the following link:
    {activation_link}

    Best regards,
    Your Application
    '''
    message = {
        'raw': base64.urlsafe_b64encode(message_text.encode()).decode(),
        'payload': {
            'headers': {'Subject': subject, 'To': to},
            'body': {'data': base64.urlsafe_b64encode(message_text.encode()).decode()}
        }
    }
    return message

def send_message(service, user_id, message):
    sent_message = service.users().messages().send(userId=user_id, body=message).execute()
    return sent_message

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.http import HttpResponse

def send_email(request):
    # Load credentials from JSON file
    credentials = service_account.Credentials.from_service_account_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json'))


    # Create a service object for the Gmail API
    service = build('gmail', 'v1', credentials=credentials)

    # Create the email message
    sender = 'employed.com@example.com'
    recipient = 'lewismusau2@example.com'
    subject = 'Test Email'
    message_text = 'This is a test email.'
    message = create_message(sender, recipient, subject, message_text)

    # Send the email message
    result = send_message(service, 'me', message)

    return result

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        return HttpResponse('Message sent successfully.')
    except Exception as e:
        return HttpResponse('An error occurred while sending the message: ' + str(e))
