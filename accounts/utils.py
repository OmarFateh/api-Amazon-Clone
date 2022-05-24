from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.text import slugify
from django.utils.encoding import smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site

from rest_framework_simplejwt.tokens import RefreshToken


# def send_activation_reset_email(request, user, is_activation=False, is_reset=False):
#     """
#     Take request and user.
#     if is activation, send activation email to the user.
#     if is reset, send reset email to the user.
#     """
#     current_site = get_current_site(request).domain
#     uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#     # activation email
#     if is_activation:
#         subject = 'Verfiy your Email'
#         token = str(RefreshToken.for_user(user).access_token)
#         absurl = f"http://localhost:3000/activate?token={token}" #"users-api:verfiy-email-confirm"
#         params = {"token": token}
#     # reset email
#     elif is_reset:    
#         subject = 'Reset your Password'
#         reverse_url = "users-api:password-reset-confirm"
#         token = str(PasswordResetTokenGenerator().make_token(user))
#         params = {"uidb64": uidb64, "token": token}
#         relative_link = reverse(reverse_url, kwargs=params)
#         absurl = f"http://{current_site}{relative_link}"
#     message = f"""Hello {user.first_name} {user.last_name}, 
#                 \nplease click on the link below to {subject}
#                 \n{absurl}"""
#     user.email_user(subject=subject, message=message)          


def send_activation_reset_email(request, user, is_activation=False, is_reset=False):
    """
    Take request and user.
    if is activation, send activation email to the user.
    if is reset, send reset email to the user.
    """
    # activation email
    if is_activation:
        subject = 'Verfiy your Email'
        token = str(RefreshToken.for_user(user).access_token)
        absurl = f"http://localhost:3000/activate?token={token}" #"users-api:verfiy-email-confirm"
        params = {"token": token}
    # reset email
    elif is_reset:    
        subject = 'Reset your Password'
        token = str(RefreshToken.for_user(user).access_token)
        absurl = f"http://localhost:3000/password/reset/confirm?token={token}"
    message = f"""Hello {user.first_name} {user.last_name}, 
                \nplease click on the link below to {subject}
                \n{absurl}"""
    user.email_user(subject=subject, message=message)     