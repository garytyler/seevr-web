import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Feature

log = logging.getLogger(__name__)


class GuestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Initialize guest connections"""
        guest_name = self.scope["session"]["guest_name"]
        self.feature = await database_sync_to_async(
            lambda: Feature.objects.get(slug=self.scope["session"]["feature_slug"])
        )()
        assert guest_name and self.feature
        self.feature.guest_queue.add(session_key=self.scope["session"].session_key)
        await self.accept()

    async def disconnect(self, close_code):
        self.feature.guest_queue.remove(self.scope["session"].session_key)


class PresenterConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        feature_slug = self.scope["url_route"]["kwargs"]["feature_slug"]
        await database_sync_to_async(
            lambda: Feature.objects.get(slug=feature_slug).title
        )()

        await database_sync_to_async(
            lambda: Feature.objects.filter(slug=feature_slug).update(
                channel_name=self.channel_name
            )
        )()
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        log.debug(f"{self.__class__.__name__} received text: {text_data}")
        log.debug(f"{self.__class__.__name__} received bytes: {bytes_data}")
