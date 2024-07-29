"""
Django settings for base_framework project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
import sys
from pathlib import Path
#项目名称（自定义参数）
PROJECT_NAME = '业务基础代码框架'

#manage.py所在目录
BASE_DIR = Path(__file__).resolve().parent.parent
# 本地数据库的目录（自定义参数）
LOC_DB_DIR = os.path.join(BASE_DIR, 'db')
# 本地固化数据目录（自定义参数）
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
# 本地配置目录
CONF_DIR = os.path.join(BASE_DIR, 'conf')
# 日志目录
LOG_ROOT = os.path.join(BASE_DIR, 'logs')

# 用于加密密码、会话等，初始化是随机生成的字符串
SECRET_KEY = 'django-insecure-!^bltzueq+kr#uatj64!p=p=v$)lc%dq#)s9zzolfep%rsyd3m'

# 运行模式 True调试模式
DEBUG = True
# 允许访问的主机，生产环境需要配置
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'drf_spectacular_sidecar',

    #本地应用
    'app.api.demo',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 路由的入口
ROOT_URLCONF = 'app.urls'
#asgi 这里采用Daphne部署
ASGI_APPLICATION = 'app.asgi.application'
#wsgi
#WSGI_APPLICATION = 'app.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
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

REST_FRAMEWORK = {
    # 权限认证
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
        # 自定义的权限
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #自定义token
    ],

    # 限流 TODO 导致swagger异常
    # 'DEFAULT_THROTTLE_CLASSES': (
    #     'rest_framework.throttling.UserRateThrottle'
    # ),
    'DEFAULT_THROTTLE_RATES': {
        # 限流策略
        'user': '60/min',
    },

    # 自定义默认的分页类
    #'DEFAULT_PAGINATION_CLASS': 'app.pkg.django.XXPagination',
    #'PAGE_SIZE': 10
}

#drf-spectacular 参数配置
SPECTACULAR_SETTINGS = {
    'TITLE': f'{PROJECT_NAME} API',
    "DESCRIPTION": 'API Schema',
    "VERSION": '0.0.1',
    # UI
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "SWAGGER_UI_SETTINGS": {
            "deepLinking": True,
            "filter": True,
            # "requestSnippetsEnabled": True,
            # "pluginsOptions": {"pluginLoadType": "chain"},
            # "displayOperationId": False,
            # "showExtensions": True,
    },
    # OTHER SETTINGS，支持表单文件上传
    "COMPONENT_SPLIT_REQUEST": True,
}


# 使用auth的密码校验器，自定义的认证流程可以忽略AUTH_PASSWORD_VALIDATORS配置
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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
# 配置地区属性、时区等
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(LOC_DB_DIR, 'db.sqlite3'),
    }
}

REDIS_CACHE_CONF = {
    "host": "127.0.0.1",
    "port": "6679",
    #ssl配置
    #"SSL": True,
    #"SSL_CERT_REQS": "required",
    #"SSL_CA_CERTS": f"{CONF_DIR}/ca.crt",
    #"SSL_CERTFILE": f"{CONF_DIR}/client.crt",
    #"SSL_KEYFILE":  f"{CONF_DIR}/client.key",
}

REDIS_URL = f'redis://{REDIS_CACHE_CONF["host"]}:{REDIS_CACHE_CONF["port"]}'
if REDIS_CACHE_CONF.get("SSL"):
    REDIS_URL = f'rediss://{REDIS_CACHE_CONF["host"]}:{REDIS_CACHE_CONF["port"]}'

REDIS_DB_WEB_USED = 0
REDIS_DB_CHANNEL_LAYERS = 1
REDIS_DB_CELERY_BROKER = 2
REDIS_DB_CELERY_RESULT = 3

# Django CACHE 配置
CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'{REDIS_URL}/{REDIS_DB_WEB_USED}',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,  # seconds
            "SOCKET_TIMEOUT": 5,  # seconds
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 100,
                #ssl连接配置
                #'ssl_cert_reqs': REDIS_CACHE_CONF["SSL_CERT_REQS"],
                #'ssl_ca_certs': REDIS_CACHE_CONF["SSL_CA_CERTS"],
                #'ssl_certfile': REDIS_CACHE_CONF["SSL_CERTFILE"],
                #'ssl_keyfile': REDIS_CACHE_CONF["SSL_KEYFILE"],
            },
            #"PASSWORD": "mysecret"
        }
    },
    'celery': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'{REDIS_URL}/{REDIS_DB_CELERY_BROKER}',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,  # seconds
            "SOCKET_TIMEOUT": 5,  # seconds
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 100,
            },
        }
    }
}
#Channel 配置
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [{
                'address': f'{REDIS_URL}/{REDIS_DB_WEB_USED}',
                # ssl配置
                #'ssl_cert_reqs': REDIS_CACHE_CONF["SSL_CERT_REQS"],
                #'ssl_ca_certs': REDIS_CACHE_CONF["SSL_CA_CERTS"],
                #'ssl_certfile': REDIS_CACHE_CONF["SSL_CERTFILE"],
                #'ssl_keyfile': REDIS_CACHE_CONF["SSL_KEYFILE"],
            }],
        },
    },
}

#任务队列的连接配置
CELERY_BROKER_URL = f'{REDIS_URL}/{REDIS_DB_CELERY_BROKER}'
CELERY_RESULT_BACKEND = f'{REDIS_URL}/{REDIS_DB_CELERY_RESULT}'
# 可接收格式
CELERY_ACCEPT_CONTENT = ['json']
# 任务序列化格式
CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_SOFT_TIME_LIMIT = 100
CELERY_TASK_TIME_LIMIT = 100
CELERY_TIMEZONE = TIME_ZONE
# 任务路由(进程)
CELERY_TASK_ROUTES = {
    #'app.base_data.tasks.*': {'queue': 'data_sync'},
}
# 默认任务队列
CELERY_TASK_DEFAULT_QUEUE = 'celery_default'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'task_default'
#导入指定的任务模块
CELERY_IMPORTS = (
    #'app.base_data.tasks',
)

# 定时任务
CELERY_BEAT_SCHEDULE = {
    # "omAutoBackup": {
    #     "task": "app.operation_maintenance.tasks.omBackupAutoCreate",
    #     'schedule': timedelta(hours=1),
    # },
    # "websocketTask": {
    #     "task": "app.device_manage.tasks.clearWebsocketConnect",
    #     'schedule': timedelta(minutes=10),
    # },
}

# 日志相关配置
# 日志文件大小 限制，单位MB，默认50MB
LOGGING_FILE_MAX_SIZE = 50
# 日志文件保存时长，单位天
LOGGING_FILE_MAX_AGE = 7
LOG_FORMAT="{time:YYYY-MM-DD HH:mm:ss:SSS} | {level} | {module}:{function}:{line} {process}:{thread} {message}"
# 以下日志等级可以调整
LOGGING = {
    'version' : 1,
    'disable_existing_loggers':False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(module)s:%(funcName)s:%(lineno)d] [%(process)d:%(thread)d] '
                      '%(message)s',
            'style': '%',
        },
        'default': {
            'format': '%(asctime)s %(levelname)s %(message)s',
        },
    },
    'handlers':{
        'servers':{
            'class': 'app.pkg.utils.log.handler.InterceptTimedRotatingFileHandler',
            #'class': 'logging.StreamHandler',
            'filename': os.path.join(LOG_ROOT, 'webapi_log.log'),
            'encoding': 'utf-8',
        },
        'console':{
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers':{
        'django': {
            'level': 'WARNING',
            'handlers': ['servers', 'console'],
            'propagate': False,
        },
        'django.db.backends':{
            'level':'DEBUG',
            'handlers':['servers', 'console'],
            'propagate':False,
        },
        'django.request':{
            'level':'INFO',
            'handlers':['servers', 'console'],
            'propagate':False,
        },
        'celery': {
            'level':'DEBUG',
            'handlers':['servers', 'console'],
            'propagate':False,
        }
    },
    'root': {
        'level':'DEBUG',
        'handlers':['servers', 'console'],
    }
}