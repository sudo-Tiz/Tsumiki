# ruff: noqa: F403,F405
from fabric.audio import Audio
from fabric.bluetooth import BluetoothClient
from fabric.notifications import Notifications

from .brightness import *
from .cache_notification import *
from .mpris import *
from .power_profile import *
from .screen_record import *
from .weather import *

cache_notification_service = NotificationCacheService().get_initial()
weather_service = WeatherService().get_initial()
power_profile_service = PowerProfiles().get_initial()

# Fabric services
audio_service = Audio()
notification_service = Notifications()
bluetooth_service = BluetoothClient()
