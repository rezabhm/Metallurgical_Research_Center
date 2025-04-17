from datetime import timedelta


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

# Cors Config
CORS_ALLOW_ALL_ORIGINS = True
CSRF_COOKIE_SECURE = False
