from fabric.audio import Audio
from gi.repository import GLib
from services import Brightness, NotificationCacheService


# constants

NOTIFICATION_WIDTH = 400
NOTIFICATION_IMAGE_SIZE = 64
NOTIFICATION_TIMEOUT = 5  # 5 seconds


APPLICATION_NAME = "hydepanel"
SYSTEM_CACHE_DIR = GLib.get_user_cache_dir()
APP_CACHE_DIRECTORY = f"{SYSTEM_CACHE_DIR}/{APPLICATION_NAME}"

brightness_service = Brightness()
audio_service = Audio()
notif_cache_service = NotificationCacheService()
