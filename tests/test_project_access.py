import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import types

stub_session = types.ModuleType("session")

async def dummy_get_db():
    pass

stub_session.get_db = dummy_get_db
sys.modules["app.db.session"] = stub_session

import pytest
from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient

from app.api.v1.endpoints import projects as projects_endpoint
from app.core.security import get_current_user

from app.models import Base, User, Project, ProjectAccess
from app.db.repository.project import grant_project_access


app = FastAPI()
app.include_router(projects_endpoint.router, prefix="/api/v1/projects", tags=["projects"])

pytest.importorskip("aiosqlite")


@pytest.mark.asyncio
async def test_grant_project_access():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        user1 = User(google_id="1", email="user1@example.com")
        user2 = User(google_id="2", email="user2@example.com")
        session.add_all([user1, user2])
        await session.flush()
        project = Project(name="proj", user_id=user1.id)
        session.add(project)
        await session.flush()

        access = await grant_project_access(
            session, project_id=str(project.id), user_id=str(user2.id)
        )
        await session.commit()

        assert access.project_id == project.id
        assert access.user_id == user2.id

        result = await session.execute(
            select(ProjectAccess).where(
                ProjectAccess.project_id == project.id,
                ProjectAccess.user_id == user2.id,
            )
        )
        assert result.scalar_one() is not None


@pytest.mark.asyncio
async def test_share_project_endpoint():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[projects_endpoint.get_db] = override_get_db

    async with async_session() as session:
        owner = User(google_id="1", email="owner@example.com")
        other = User(google_id="2", email="other@example.com")
        session.add_all([owner, other])
        await session.flush()
        project = Project(name="proj", user_id=owner.id)
        session.add(project)
        await session.commit()

    async def override_get_current_user():
        return owner

    app.dependency_overrides[get_current_user] = override_get_current_user

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post(
            "/api/v1/projects/proj/share", params={"user_email": "other@example.com"}
        )

    assert resp.status_code == 200

    async with async_session() as session:
        result = await session.execute(
            select(ProjectAccess).where(
                ProjectAccess.project_id == project.id,
                ProjectAccess.user_id == other.id,
            )
        )
        assert result.scalars().first() is not None


@pytest.mark.asyncio
async def test_share_project_user_not_found():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[projects_endpoint.get_db] = override_get_db

    async with async_session() as session:
        owner = User(google_id="1", email="owner@example.com")
        session.add(owner)
        await session.flush()
        project = Project(name="proj", user_id=owner.id)
        session.add(project)
        await session.commit()

    async def override_get_current_user():
        return owner

    app.dependency_overrides[get_current_user] = override_get_current_user

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post(
            "/api/v1/projects/proj/share",
            params={"user_email": "missing@example.com"},
        )

    assert resp.status_code == 404
    assert resp.json()["detail"] == "User not found"

