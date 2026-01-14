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

from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, BigInteger, Date, String

from discord_shared_db.base import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(BigInteger, primary_key=True)

    username = Column(String, unique= True, nullable=False)
    email = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)
    dob = Column(Date, nullable=True)
    disabled = Column(Boolean, default=False, nullable=False)

    is_claimed = Column(Boolean, default=False, nullable=False)

    sessions = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    auth_methods = relationship(
        "UserAuth",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    discord_user = relationship(
        "DiscordUser",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    cards = relationship(
        "UserCard",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    decks = relationship(
        "Deck",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    






