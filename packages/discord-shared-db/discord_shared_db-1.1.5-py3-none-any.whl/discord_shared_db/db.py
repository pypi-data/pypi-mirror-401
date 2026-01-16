# This file is part of discord-shared-db
#
# Copyright (C) 2026 CouchComfy
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
import logging
from typing import AsyncGenerator
from datetime import date, datetime, timedelta, timezone
from warnings import deprecated

from sqlalchemy import delete, select
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from discord_shared_db.user import User, Base
from discord_shared_db.user_auth import UserAuth
from discord_shared_db.auth_enums import AuthProviders
from discord_shared_db.discord.discord_user import DiscordUser
from discord_shared_db.user_session import UserSession

load_dotenv()

class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return  # Prevent reinitialization on multiple calls
        
        POSTGRES_USER = os.getenv("POSTGRES_USER")
        POSTGRES_PASS = os.getenv("POSTGRES_PASS")
        POSTGRES_ADDY = os.getenv("POSTGRES_ADDY")
        POSTGRES_NAME = os.getenv("POSTGRES_NAME")
        POSTGRES_PORT = os.getenv("POSTGRES_PORT", '5432')

        if not POSTGRES_USER:
            raise Exception("Postgres User not Defined")
        if not POSTGRES_PASS:
            raise Exception("Postgres Password not Defined")
        if not POSTGRES_ADDY:
            raise Exception("Postgres Address not Defined")
        if not POSTGRES_NAME:
            raise Exception("Postgres Database Name not Defined")
        if not POSTGRES_PORT:
            raise Exception("Postgres Port not Defined. How did you manage this!!")

        database_url = (
            f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}'
            f'@{POSTGRES_ADDY}:{POSTGRES_PORT}/{POSTGRES_NAME}'
        )
        
        self.engine = create_async_engine(database_url, echo=False)
        self.async_session = async_sessionmaker(
            self.engine, 
            class_=AsyncSession,
            expire_on_commit=False
        )

        self._initialized = True 
    
    async def init_database(self):
        """Create all tables"""
        logging.info(f'Initializing the Database with the models')
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def get_db(self):
        async with self.get_session() as session:
            yield session
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Context manager for database sessions - one per command"""
        logging.debug(f'Get database Session')
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
           
    @deprecated("This method will be removed SOON. Use `get_user_by_id, get_user_by_username or get_user_by_email` instead.")
    async def get_or_create_user(self, username: str = None, email: str = None, hashed_password: str = None, dob: date = None,  session: AsyncSession = None):
        """
        Fetch existing Lyko user by username/email.
        If user does not exist, create a new one.
        Only fills fields (hashed_password, dob, email) if creating a new account.
        """

        owns_session = False
        if session is None:
            session = self.async_session()
            owns_session = True

        try:
            # Try to find user first
            result = await session.execute(
                select(User).where((User.username == username) | (User.email == email))
            )
            user = result.scalar_one_or_none()

            if user:
                # Existing user, just return it
                return user

            # Only create a new user if it does not exist
            if not (email and hashed_password and dob):
                raise ValueError("Missing required fields to create a new user")

            user = User(
                username=username,
                email=email,
                hashed_password=hashed_password,
                dob=dob,
                is_claimed=True,
                disabled=False
            )
            session.add(user)
            await session.flush()
            return user

        finally:
            if owns_session:
                await session.commit()
                await session.close()

    async def get_user_by_id(
        self,
        user_id: int,
        session: AsyncSession
    ) -> User | None:
        
        if not user_id:
            raise ValueError("username is required")
        if session is None:
            raise RuntimeError("Session must be provided")
        
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_username(
        self,
        username: str,
        session: AsyncSession
    ) -> User | None:
        
        if not username:
            raise ValueError("username is required")
        if session is None:
            raise RuntimeError("Session must be provided")

        result = await session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_user_by_email(
        self,
        email: str,
        session: AsyncSession
    ) -> User | None:
        
        if not email:
            raise ValueError("username is required")
        if session is None:
            raise RuntimeError("Session must be provided")

        result = await session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_all_users(self, session=None):
        owns_session = False
        if session is None:
            session = self.async_session()
            owns_session = True

        try:
            async with session.begin():
                result = await session.execute(select(User))
                users = result.scalars().all()
        finally:
            if owns_session:
                await session.close()

        return users
    
    async def create_user(
        self,
        username: str,
        email: str | None,
        hashed_password: str | None,
        dob: date | None,
        session: AsyncSession
    ) -> User:
        
        if not username:
            raise ValueError("Missing required fields")
        if session is None:
            raise RuntimeError("Session must be provided")

        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            dob=dob,
            is_claimed=True,
            disabled=False
        )

        session.add(user)
        await session.flush()
        return user
    

    async def get_discord_user(
        self,
        discord_user_id: int,
        session: AsyncSession
    ) -> DiscordUser | None:
        result = await session.execute(
            select(DiscordUser).where(
                DiscordUser.discord_user_id == discord_user_id
            )
        )
        return result.scalar_one_or_none()

    async def get_or_create_discord_user(self, discord_user_id: int, discord_username: str, session=None):
        """
        Fetches or creates a Discord user (soft account) and associated Lyko User.
        """
        owns_session = False
        if session is None:
            session = self.async_session()
            owns_session = True

        try:
            # Check if Discord user exists
            result = await session.execute(
                select(DiscordUser).where(DiscordUser.discord_user_id == discord_user_id)
            )
            discord_user = result.scalar_one_or_none()
            if discord_user:
                return discord_user

            # Create soft User
            user = User(
                username=f"discord_{discord_user_id}",  # placeholder username
                is_claimed=False
            )
            session.add(user)
            await session.flush()  # assigns user_id

            # Create DiscordUser profile
            discord_user = DiscordUser(
                user_id=user.user_id,
                discord_user_id=discord_user_id,
                discord_username=discord_username
            )
            session.add(discord_user)

            # Create auth link
            auth_link = UserAuth(
                user_id=user.user_id,
                provider=AuthProviders.DISCORD,
                provider_account_id=str(discord_user_id),
                linked_date=datetime.now(datetime.timezone.utc)
            )
            session.add(auth_link)

            await session.flush()
            return discord_user
        finally:
            if owns_session:
                await session.commit()
                await session.close()
        
    async def claim_discord_user(self, discord_user: DiscordUser, username: str, email: str, hashed_password: str, dob: date, session=None):
        """
        Converts a soft Discord user into a claimed Lyko account.
        """
        owns_session = False
        if session is None:
            session = self.async_session()
            owns_session = True

        try:
            user: User = discord_user.user
            user.username = username
            user.email = email
            user.hashed_password = hashed_password
            user.dob = dob
            user.is_claimed = True

            session.add(user)
            await session.flush()
            return user
        finally:
            if owns_session:
                await session.commit()
                await session.close()

    async def ensure_user_stats(self, user: User, relation_name, session, stat_cls):
        '''
        Pass in the stat class that needs to be initallized
        '''
        await session.refresh(user, attribute_names=[relation_name])
        if getattr(user, relation_name) is None:
            setattr(user, relation_name, stat_cls())
            session.add(user)
            await session.commit()
            await session.refresh(user, attribute_names=[relation_name])


    async def get_valid_user_token_session(
        self,
        user_id: int,
        refresh_token_hash: str,
        session: AsyncSession
    ) -> UserSession | None:
        result = await session.execute(
            select(UserSession).where(
                UserSession.user_id == user_id,
                UserSession.refresh_token_hash == refresh_token_hash,
                UserSession.revoked == False,
                UserSession.expires_at > datetime.now(timezone.utc)
            )
        )
        return result.scalar_one_or_none()

    async def get_valid_user_token_session_by_token(
        self,
        refresh_token_hash: str,
        session: AsyncSession
    ) -> UserSession | None:
        result = await session.execute(
            select(UserSession)
            .where(
                UserSession.refresh_token_hash == refresh_token_hash,
                UserSession.revoked == False,
                UserSession.expires_at > datetime.now(timezone.utc)
            )
        )
        return result.scalar_one_or_none()

    async def create_user_session(
        self,
        user_id: int,
        refresh_token_hash: str,
        expires_at: datetime,
        session: AsyncSession | None = None
    ):
        owns_session = False
        if session is None:
            logging.warning("🚨🚨🚨 NO SESSION was provided to create_user_session()! Make sure to pass in a session! 🚨🚨🚨")
            session = self.async_session()
            owns_session = True

        try:
            session_obj = UserSession(
                user_id=user_id,
                refresh_token_hash=refresh_token_hash,
                created_at=datetime.now(timezone.utc),
                expires_at=expires_at,
                revoked=False
            )
            session.add(session_obj)
            await session.flush()
            return session_obj
        finally:
            if owns_session:
                await session.commit()
                await session.close()

    async def revoke_user_token_session(
        self,
        session_obj: UserSession,
        session: AsyncSession
    ):
        session_obj.revoked = True
        session.add(session_obj)
    
    async def revoke_user_sessions(self, user_id: int, session: AsyncSession):
        result = await session.execute(
            select(UserSession).where(
                UserSession.user_id == user_id,
                UserSession.revoked == False
            )
        )
        sessions = result.scalars().all()

        for s in sessions:
            s.revoked = True

    async def delete_expired_sessions(self) -> int:
        async with self.session() as db:
            result = await db.execute(
                delete(UserSession).where(
                    UserSession.expires_at < datetime.now(timezone.utc)
                )
            )
            await db.commit()
            return result.rowcount or 0

