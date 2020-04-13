import pytest
from app.crud.features import crud_features
from app.schemas.features import FeatureCreate
from async_asgi_testclient import TestClient
from tests._utils.features import (
    create_random_feature,
    create_random_feature_slug,
    create_random_feature_title,
)
from tests._utils.guests import create_random_guest


@pytest.mark.asyncio
async def test_feature_crud_create(app):
    async with TestClient(app):
        params = {
            "title": create_random_feature_title(),
            "slug": create_random_feature_slug(),
            "turn_duration": 90,
        }
        feature_in = FeatureCreate(**params)
        feature = await crud_features.create(obj_in=feature_in)
        assert feature.title == params["title"]
        assert feature.turn_duration == params["turn_duration"]


@pytest.mark.asyncio
async def test_feature_crud_get(app):
    async with TestClient(app):
        created_feature = await create_random_feature()
        gotten_feature = await crud_features.get(id=created_feature.id)
        assert gotten_feature.id == created_feature.id
        assert gotten_feature.title == created_feature.title
        assert gotten_feature.slug == created_feature.slug
        assert gotten_feature.turn_duration == created_feature.turn_duration


@pytest.mark.asyncio
async def test_feature_crud_get_all(app):
    async with TestClient(app):
        created_features = [await create_random_feature() for _ in range(5)]
        gotten_features = await crud_features.get_all()
        assert gotten_features == created_features


@pytest.mark.asyncio
async def test_feature_crud_delete(app):
    async with TestClient(app):
        created_features = [await create_random_feature() for _ in range(5)]
        rem_id = created_features[3].id
        deleted_count = await crud_features.delete(id=rem_id)
        assert deleted_count == 1
        deleted_count = await crud_features.get(id=created_features[3].id)
        assert deleted_count is None


@pytest.mark.skip
@pytest.mark.asyncio
async def test_feature_crud_get_guests(app):
    async with TestClient(app):
        created_feature = await create_random_feature()
        created_guests = [
            await create_random_guest(feature=created_feature) for _ in range(3)
        ]
        gotten_guests = await crud_features.get_guests(id=created_feature.id)
        assert gotten_guests == created_guests