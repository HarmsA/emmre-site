"""
Django settings for emmre project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os, json, sys
import django_heroku


def get_environment_variable(name, default=None):
    if not hasattr(os, 'environ'):
        return default
    if name.lower() in os.environ:
        return os.environ[name.lower()]
    elif name.upper() in os.environ:
        return os.environ[name.upper()]
    else:
        return default


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environment_variables_path = str(BASE_DIR).rstrip("/") + "/environment_variables.json"
if os.path.exists(environment_variables_path):
    with open(environment_variables_path) as environment_variables_file:
        environment_variables_dict = json.load(environment_variables_file)
        for key, value in environment_variables_dict.items():
            os.environ[key] = value

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

STAGE = get_environment_variable('stage', 'live')

if not STAGE:
    print("Stage not set.")
    sys.exit()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vk2in43)9ukh5qjl_*)7hgsm5q_(z1_*-ke(8f#zt)$)#3)l4g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if STAGE in ['local', 'dev']:
    DEBUG = True

ALLOWED_HOSTS = [
    # ".writersdigestconference.com",
    # "writersdigestconference.us-east-1.elasticbeanstalk.com",
]

SITE_ID = 2
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'emmre_main.apps.EmmreConfig',
    'media.apps.MediaConfig',
    'config.apps.ConfigConfig',
    'fontawesome-free',
    'tinymce',
    # 'cachalot',
]

django_heroku.settings(locals())

if STAGE == 'live':
    INSTALLED_APPS += ['cachalot']

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.sites.SimpleMiddleware',
]

Z_INDEX_PRIORITIES = [
    'accessibility',
]

# if DEBUG:
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']


ROOT_URLCONF = 'emmre.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'emmre_main.context_processors.ContextProcessor',
                'config.context_processors.configuration_context_processor',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'emmre.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# if STAGE == 'local':
# 	DATABASES = {
# 		'default': {
# 			'ENGINE': 'django.db.backends.mysql',
# 			'NAME': get_environment_variable('database_name'),
# 			'USER': get_environment_variable('database_user'),
# 			'PASSWORD': get_environment_variable('database_password'),
# 			'HOST': get_environment_variable('database_host'),
# 			'PORT': '3306',
# 		},
# 	}
# 	# DATABASES = {
# 	# 	'default': {
# 	# 		'ENGINE': 'django.db.backends.sqlite3',
# 	# 		'NAME': BASE_DIR / 'db.sqlite3',
# 	# 	}
# 	# }
# elif STAGE == "live":
# 	DATABASES = {
# 		'default': {
# 			'ENGINE': 'django.db.backends.mysql',
# 			'NAME': get_environment_variable('database_name'),
# 			'USER': get_environment_variable('database_user'),
# 			'PASSWORD': get_environment_variable('database_password'),
# 			'HOST': get_environment_variable('database_host'),
# 			'PORT': '3306',
# 		},
# 	}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = get_environment_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_environment_variable('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_environment_variable('AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_AUTH = False

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = False

USE_L10N = False

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/assets/'
STATIC_ROOT = str(BASE_DIR).rstrip("/") + "/static/"
STATICFILES_DIRS = [
    os.path.join(str(BASE_DIR), "assets"),
]

if STAGE == 'live':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

# SERVER_EMAIL = get_environment_variable('SERVER_EMAIL', "server@writersdigestconference.com")
# DEFAULT_FROM_EMAIL = get_environment_variable('DEFAULT_FROM_EMAIL', "webmaster@writersdigestconference.com")

# if STAGE == 'local':
# 	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# else:
# 	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 	EMAIL_HOST = get_environment_variable('SMTP_HOST', 'localhost')
# 	EMAIL_HOST_USER = get_environment_variable('SMTP_USER', '')
# 	EMAIL_HOST_PASSWORD = get_environment_variable('SMTP_PASSWORD', '')
# 	EMAIL_PORT = 587
# 	EMAIL_USE_TLS = True
# 	EMAIL_USE_SSL = False
# 	EMAIL_TIMEOUT = 5

ADMINS = [
    ["Adam Harms", "aharms@aimmedia.com"],
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'filesystem': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': str(BASE_DIR).rstrip('/') + '/cache/',
    }
}

CACHE_MIDDLEWARE_SECONDS = 3600

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Stores cache in db for local to not kick you out of admin when server is restarted
if STAGE == 'local':
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
else:
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

SCRIPT_CACHE_TIME = 10 if DEBUG else 40  # minutes
STYLE_CACHE_TIME = 10 if DEBUG else 40  # minutes

TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, "../assets/tinymce/tinymce.js")
TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
               "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
               "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
               "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
               "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
               "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    "language": "es_ES",  # To force a specific language instead of the Django current language.
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True
TINYMCE_EXTRA_MEDIA = {
    'css': {
        'all': [
            ...
        ],
    },
    'js': [
        ...
    ],
}

INTERNAL_IPS = [
    '127.0.0.1',  # localhost
    '104.166.252.133',  # Adam's House

]
ALLOWED_HOSTS = ['*', '104.166.252.133']

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
    'cachalot.panels.CachalotPanel',
]

CACHALOT_ENABLED = not DEBUG
CACHALOT_UNCACHABLE_TABLES = [
    'auth_group',
    'auth_group_permissions',
    'auth_permission',
    'auth_user',
    'auth_user_groups',
    'auth_user_user_permissions',
    'django_admin_log',
    'django_content_type',
    'django_migrations',
    'django_session',
]
