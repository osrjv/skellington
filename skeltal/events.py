import logging
from skeltal.protocol import clientbound

LOGGER = logging.getLogger(__name__)


class EventsHandler:
    def __init__(self):
        self._seen = set()

    def publish(self, message):
        if message._type not in self._seen:
            self._seen.add(message._type)

        if message._type is clientbound.Play.JoinGame:
            LOGGER.info(
                "Joined game:\n%s",
                "\n".join(
                    f"{k}: {v}" for k, v in message.items() if not k.startswith("_")
                ),
            )

    def subscribe(self, event, callback):
        pass
