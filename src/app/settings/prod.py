from app.settings.base import * # noqa

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'HOST': os.environ['DB_HOST'],
        'USER': os.environ['DB_USER'],
        'PORT': os.environ['DB_PORT'],
        'PASSWORD': os.environ['DB_PASSWORD'],
    }
}


MEDIA_ROOT = '/var/www/quiz/media'
STATIC_ROOT = '/var/www/quiz/static'