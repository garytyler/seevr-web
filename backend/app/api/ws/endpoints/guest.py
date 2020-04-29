import asyncio
import logging
from typing import Any

from app.api.dependencies.publish import publish_feature
from app.core.redis import ChannelReader, redis
from app.crud.features import crud_features
from app.utils.endpoints import APIWebSocketEndpoint
from fastapi import APIRouter, WebSocket, status

logger = logging.getLogger(__name__)
router = APIRouter()


@router.websocket("/guest/{slug}")
class GuestWebSocket(APIWebSocketEndpoint):
    async def on_connect(self, ws: WebSocket) -> None:
        # TODO Pass both feature id and guest id in route path and handle adding
        # guest to feature guest list here, and use another endpoint for non-guest
        # visitors.
        feature_slug = ws.scope["path_params"].get("slug")
        feature = await crud_features.get_by_slug(slug=feature_slug)
        if not feature:
            return await ws.close(code=status.HTTP_404_NOT_FOUND)
        await ws.accept()
        self.presenter_ch_name = str(feature.presenter_channel_name)
        self.interactor_ch = (
            await redis.subscribe(str(feature.interactor_channel_name))
        )[0]
        await publish_feature(id=feature.id)
        self.worker_task = asyncio.create_task(self.forward_channel_to_client(ws))

    async def forward_channel_to_client(self, ws):
        async for msg in ChannelReader(self.interactor_ch):
            await ws.send_text(msg.decode())

    async def on_receive(self, ws: WebSocket, data: Any) -> None:
        await redis.publish(self.presenter_ch_name, data)

    async def on_disconnect(self, ws: WebSocket, close_code: int) -> None:
        worker_task = getattr(self, "worker_task", None)
        if worker_task:
            self.worker_task.cancel()
        interactor_ch = getattr(self, "interactor_ch", None)
        if interactor_ch:
            await redis.unsubscribe(interactor_ch)
