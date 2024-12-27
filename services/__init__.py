# ruff: noqa: F403,F405
from fabric.audio import Audio
from fabric.notifications import Notifications

from .brightness import *
from .mpris import *
from .notification import *
from .powerprofile import *
from .screenrecord import *
from .weather import *

brightness_service = Brightness()
audio_service = Audio()
weather_service = WeatherService()
power_profile_service = PowerProfiles()
notify_cache_service = NotificationCacheService()
notification_service = Notifications()
