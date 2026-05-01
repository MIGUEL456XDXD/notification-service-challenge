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
class ConsoleChannel(NotificationChannel):
    pass

    def send(self, message: str) -> None:
        try:
            print(f"[console] {message}")
        except Exception as e:

            raise DeliveryError(self.get_channel_name(), e)

    def get_channel_name(self) -> str:
        return "console"

    def is_available(self) -> bool:
        return True
import os


class FileChannel(NotificationChannel):
    pass

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_channel_name(self) -> str:
        return f"file ({self.file_path})"

    def is_available(self) -> bool:
        directory = os.path.dirname(self.file_path) or "."


        if os.path.exists(self.file_path):
            return os.access(self.file_path, os.W_OK)


        return os.path.isdir(directory) and os.access(directory, os.W_OK)

    def send(self, message: str) -> None:
        if not self.is_available():
            raise ChannelUnavailableError(self.get_channel_name())

        try:
            with open(self.file_path, "a", encoding="utf-8") as file:
                file.write(f"{message}\n")
        except Exception as e:
            raise DeliveryError(self.get_channel_name(),e)