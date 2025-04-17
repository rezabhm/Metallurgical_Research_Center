from datetime import timedelta

from corsheaders.defaults import default_headers

# Rest Framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'configs.authentication.HTTPOnlyCookieJWTAuthentication',
    ),
}

SIMPLE_JWT = {

    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
    'BLACKLIST_AFTER_ROTATION': True,
    'ROTATE_REFRESH_TOKENS': False,

}

# ================== CORS HEADERS ==================
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [

    "http://localhost:3001",

]

# فقط در حالت توسعه فعال باشه
CORS_ALLOW_HEADERS = list(default_headers) + [
    'X-CSRFToken',
]

# ================== CSRF ==================
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3001",
]

# ================== SESSION / COOKIE CONFIG ==================
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Lax'
