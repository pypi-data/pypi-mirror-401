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
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Index, String

from discord_shared_db.base import Base


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)

    refresh_token_hash = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="sessions")

    __table_args__ = (
        Index("ix_user_sessions_refresh_hash", "refresh_token_hash"),
        Index("ix_user_sessions_user_id", "user_id"),
    )


