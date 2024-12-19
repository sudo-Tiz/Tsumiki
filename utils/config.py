from fabric.audio import Audio

from services import Brightness, NotificationCacheService

brightness_service = Brightness()
audio_service = Audio()
notif_cache_service = NotificationCacheService()
