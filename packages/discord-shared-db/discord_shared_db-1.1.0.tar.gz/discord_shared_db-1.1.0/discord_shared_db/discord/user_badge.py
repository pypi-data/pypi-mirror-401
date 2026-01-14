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
from sqlalchemy import BigInteger, Column, ForeignKey, String

from discord_shared_db.base import Base

class UserBadge(Base):
    __tablename__ = "user_badges"

    discord_user_id = Column(
        BigInteger,
        ForeignKey("discord_users.discord_user_id"),
        primary_key=True
    )
    badge_id = Column(String, ForeignKey("badges.id"), primary_key=True)

    image_path = Column(String, nullable=False)

    user = relationship("DiscordUser", back_populates="badges")
