# ruff: noqa: F403,F405
from fabric.audio import Audio

from .brightness import *
from .mpris import *
from .notification import *
from .screenrecord import *
from .weather import *

brightness_service = Brightness()
audio_service = Audio()
notif_cache_service = NotificationCacheService()
weather_service = WeatherService()
