import asyncio
from typing import Any

from app.api.dependencies.publish import publish_feature
from app.core.redis import ChannelReader, redis
from app.crud.features import crud_features
from app.crud.presenters import crud_presenters
from app.schemas.presenters import PresenterCreate
from app.utils.endpoints import APIWebSocketEndpoint
from fastapi import APIRouter, WebSocket, status

router = APIRouter()


@router.websocket("/presenter/{slug}")
class PresenterWebSocket(APIWebSocketEndpoint):
    async def on_connect(self, websockets: WebSocket) -> None:
        feature_slug = websockets.scope["path_params"].get("slug")
        feature = await crud_features.get_by_slug(slug=feature_slug)
        if not feature:
            return await websockets.close(code=status.HTTP_404_NOT_FOUND)
        presenter = await crud_presenters.create(
            obj_in=PresenterCreate(feature_id=feature.id)
        )
        await presenter.save()
        await websockets.accept()
        self.presenter_ch_name = str(feature.presenter_channel_name)
        self.presenter_ch = (
            await redis.subscribe(str(feature.presenter_channel_name))
        )[0]
        await publish_feature(id=feature.id)
        self.worker_tasks = [
            asyncio.create_task(self.forward_channel_to_client(websockets=websockets))
        ]

    async def forward_channel_to_client(self, websockets):
        async for msg in ChannelReader(self.presenter_ch):
            await websockets.send_bytes(msg)

    async def on_receive(self, websockets: WebSocket, data: Any) -> None:
        await redis.publish(self.presenter_ch.name, data)

    async def on_disconnect(self, websockets: WebSocket, close_code: int) -> None:
        for task in getattr(self, "worker_tasks", []):
            task.cancel()
        presenter_ch = getattr(self, "worker_tasks", [])
        if presenter_ch:
            await redis.unsubscribe(presenter_ch)
