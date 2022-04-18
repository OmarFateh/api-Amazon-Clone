from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^z)ob+-6059siv!otfou91*l%r9rfx6xegdo5$81q#!+n1s-26'
# SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'amazon_clone',
#         'USER': 'rootuser',
#         'HOST': 'localhost',
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'PORT': '3306',
#     }
# }

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'fatehomar0@gmail.com'
EMAIL_HOST_PASSWORD = 'ltpopqfqbdoweugo'
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')