class NotificationError(Exception):
    """Error base para problemas relacionados con notificaciones."""
    pass


class ChannelUnavailableError(NotificationError):
    def __init__(self, channel_name: str, message: str = None):
        self.channel_name = channel_name
        message = message or "No se puede usar el canal en este momento"
        super().__init__(f"{message} ({channel_name})")


class DeliveryError(NotificationError):
    def __init__(self, channel_name: str, original_exception: Exception = None):
        self.channel_name = channel_name
        self.original_exception = original_exception

        if original_exception:
            msg = (
                f"No se pudo enviar la notificación por '{channel_name}"
                f"Detalle: {original_exception}"
            )
        else:
            msg = f"No se pudo enviar la notificación por '{channel_name}"

        super().__init__(msg)
from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass

    @abstractmethod
    def get_channel_name(self) -> str:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass