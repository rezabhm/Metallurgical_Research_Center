from .base import *
from .rest_api import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # استفاده از PostgreSQL
        'NAME': 'Metallurgical_Research_Center',  # نام دیتابیس PostgreSQL
        'USER': 'postgres',  # نام کاربری دیتابیس
        'PASSWORD': 'rezabhm:1290',  # رمز عبور دیتابیس
        'HOST': 'localhost',  # آدرس سرور دیتابیس (localhost برای دیتابیس محلی)
        'PORT': '5432',  # پورت دیتابیس (پورت پیش‌فرض PostgreSQL)
    }
}

connect(
    db="configs",
    host="mongodb://localhost:27017/configs"
)

