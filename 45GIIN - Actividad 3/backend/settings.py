"""
Django settings for consultorio project.

Configuración generada automáticamente por 'django-admin startproject'.
Más información:
https://docs.djangoproject.com/en/5.1/topics/settings/
"""

from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta del proyecto (mantener confidencial en producción)
SECRET_KEY = 'django-insecure-4si566o_x=2t(02*#7=-84^at*iqjqgeq(h#8)4j7vq8k4c&ij'

# Modo de depuración (deshabilitar en producción)
DEBUG = True  # Cambiar a False en producción

# Hosts permitidos para el proyecto
ALLOWED_HOSTS = []

# Aplicaciones instaladas en el proyecto
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Framework para APIs REST
    'consultorio',  # Aplicación principal
    'corsheaders', # Permite que el frontend interacúe con el backend
]

# Middleware del proyecto
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# Permite el acceso desde el frontend (localhost:8080)
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',  # Puerto del servidor Vue.js
    'http://127.0.01:8080',  # Puerto del servidor Vue.js
]

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'POST',
    'PUT',
)


# Configuración de las URLs principales
ROOT_URLCONF = 'consultorio.urls'

# Configuración de las plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Rutas adicionales para cargar plantillas personalizadas
        'APP_DIRS': True,  # Busca plantillas en los directorios de las apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuración para WSGI
WSGI_APPLICATION = 'consultorio.wsgi.application'

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Motor de base de datos PostgreSQL
        'NAME': 'consultorio',  # Nombre de la base de datos
        'USER': 'postgres',  # Usuario de la base de datos
        'PASSWORD': '1234',  # Contraseña del usuario
        'HOST': 'localhost',  # Dirección del servidor
        'PORT': '5432',  # Puerto del servidor
    }
}

# Validadores de contraseñas
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

# Configuración de internacionalización
LANGUAGE_CODE = 'es-es'  # Idioma predeterminado
TIME_ZONE = 'Europe/Madrid'  # Zona horaria predeterminada
USE_I18N = True  # Habilitar la internacionalización
USE_TZ = True  # Activar soporte para zonas horarias

# Configuración de archivos estáticos
STATIC_URL = 'static/'  # URL base para los archivos estáticos

# Tipo de campo de clave primaria predeterminado
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de seguridad para iframes
X_FRAME_OPTIONS = 'SAMEORIGIN'  # Permitir carga en iframes del mismo origen

# Formato de entrada de fecha
DATE_INPUT_FORMATS = ["%d-%m-%Y"]

# Configuración del Django REST Framework
REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%d-%m-%Y",
    'DATE_FORMAT': "%d-%m-%Y",
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Respuesta por defecto en JSON
    ],

    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',  # Controlador de errores de DRF

}

"""
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'EXCEPTION_HANDLER': ['django_filters.rest_framework.DjangoFilterBackend'],
}
"""