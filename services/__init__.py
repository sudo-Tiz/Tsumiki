# ruff: noqa: F403,F405
from .brightness import *
from .mpris import *
from .notification import *
from .screenrecord import *
from .weather import *
from fabric.audio import Audio

brightness_service = Brightness()
audio_service = Audio()
notif_cache_service = NotificationCacheService()
weather_service = WeatherService()
