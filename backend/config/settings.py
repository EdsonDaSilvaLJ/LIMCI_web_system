from pathlib import Path

from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    "DJANGO_SECRET_KEY",
    default="django-insecure-development-only",
)
DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = [
    host.strip()
    for host in config(
        "DJANGO_ALLOWED_HOSTS",
        default="localhost,127.0.0.1",
    ).split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ninja",
    "apps.core",
    "apps.leukemia",
    "apps.renal",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Fortaleza"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

LEUKEMIA_MODEL_PATH = Path(
    config(
        "LEUKEMIA_MODEL_PATH",
        default=str(
            BASE_DIR.parent
            / "model_weights"
            / "leukemia"
            / "leukemia_efficientnet_b0.keras"
        ),
    )
)
LEUKEMIA_INFERENCE_CONFIG_PATH = Path(
    config(
        "LEUKEMIA_INFERENCE_CONFIG_PATH",
        default=str(
            BASE_DIR.parent
            / "docs"
            / "results"
            / "leukemia"
            / "inference_config.json"
        ),
    )
)
RENAL_MODEL_PATH = Path(
    config(
        "RENAL_MODEL_PATH",
        default=str(
            BASE_DIR.parent
            / "model_weights"
            / "renal"
            / "modelo_fold1.h5"
        ),
    )
)
RENAL_MODEL_FOLD = config("RENAL_MODEL_FOLD", default=1, cast=int)
RENAL_THRESHOLD = config("RENAL_THRESHOLD", default=0.5, cast=float)
MAX_IMAGE_UPLOAD_BYTES = (
    config("MAX_IMAGE_UPLOAD_MB", default=10, cast=int)
    * 1024
    * 1024
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
