# ruff: noqa: F403,F405
from fabric.audio import Audio
from fabric.notifications import Notifications

from .brightness import *
from .mpris import *
from .notification import *
from .powerprofile import *
from .screenrecord import *
from .weather import *

# Custom services
brightness_service = Brightness().get_initial()
notify_cache_service = NotificationCacheService().get_initial()
weather_service = WeatherService().get_initial()
power_profile_service = PowerProfiles().get_initial()


# Fabric services
audio_service = Audio()
notification_service = Notifications()
